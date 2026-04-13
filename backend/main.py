"""
AgenticMind Backend Service
A lightweight FastAPI backend for LLM orchestration, tool execution, and agent management.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
import uuid
import json
from datetime import datetime
import asyncio

# Import pattern implementations
from patterns.reflection import ReflectionAgent
from patterns.tool_use import ToolUseAgent, ToolRegistry
from patterns.react import ReActAgent
from patterns.planning import PlanningAgent
from patterns.multi_agent import MultiAgentOrchestrator, Agent

app = FastAPI(title="AgenticMind API", version="1.0.0")

# Enable CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, use proper database/persistence)
agents: Dict[str, Agent] = {}
tasks: Dict[str, Dict[str, Any]] = {}
tool_registry = ToolRegistry()


# ==================== Models ====================

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class TaskRequest(BaseModel):
    goal: str
    pattern: Literal["reflection", "tool_use", "react", "planning", "multi_agent"]
    messages: List[Message] = []
    config: Dict[str, Any] = {}


class TaskResponse(BaseModel):
    task_id: str
    status: Literal["pending", "running", "completed", "failed"]
    result: Optional[str] = None
    logs: List[Dict[str, Any]] = []
    plan: Optional[List[str]] = None
    reflection: Optional[str] = None


class AgentConfig(BaseModel):
    name: str
    role: str
    system_prompt: str
    tools: List[str] = []


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    handler: str  # Reference to tool handler function


# ==================== Routes ====================

@app.get("/")
async def root():
    return {
        "name": "AgenticMind API",
        "version": "1.0.0",
        "patterns": ["reflection", "tool_use", "react", "planning", "multi_agent"]
    }


@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """Create a new task using specified agentic pattern."""
    task_id = str(uuid.uuid4())
    
    task = {
        "task_id": task_id,
        "goal": request.goal,
        "pattern": request.pattern,
        "status": "pending",
        "messages": [m.dict() for m in request.messages],
        "config": request.config,
        "logs": [],
        "created_at": datetime.now().isoformat(),
        "result": None,
        "plan": None,
        "reflection": None
    }
    
    tasks[task_id] = task
    
    # Start task execution asynchronously
    asyncio.create_task(execute_task(task_id, request))
    
    return TaskResponse(
        task_id=task_id,
        status="pending",
        logs=[]
    )


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get task status and results."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    return TaskResponse(
        task_id=task["task_id"],
        status=task["status"],
        result=task.get("result"),
        logs=task.get("logs", []),
        plan=task.get("plan"),
        reflection=task.get("reflection")
    )


@app.post("/agents")
async def create_agent(config: AgentConfig):
    """Create a new agent with specific role and configuration."""
    agent_id = str(uuid.uuid4())
    
    agent = Agent(
        id=agent_id,
        name=config.name,
        role=config.role,
        system_prompt=config.system_prompt,
        tools=config.tools
    )
    
    agents[agent_id] = agent
    
    return {
        "agent_id": agent_id,
        "name": agent.name,
        "role": agent.role
    }


@app.get("/agents")
async def list_agents():
    """List all configured agents."""
    return [
        {
            "agent_id": aid,
            "name": agent.name,
            "role": agent.role,
            "tools": agent.tools
        }
        for aid, agent in agents.items()
    ]


@app.get("/tools")
async def list_tools():
    """List all available tools."""
    return tool_registry.list_tools()


@app.post("/tools/register")
async def register_tool(tool: ToolDefinition):
    """Register a custom tool."""
    tool_registry.register_tool(tool)
    return {"status": "success", "tool_name": tool.name}


# ==================== Task Execution ====================

async def execute_task(task_id: str, request: TaskRequest):
    """Execute task using the specified agentic pattern."""
    task = tasks[task_id]
    task["status"] = "running"
    
    try:
        if request.pattern == "reflection":
            result = await execute_reflection(task_id, request)
        elif request.pattern == "tool_use":
            result = await execute_tool_use(task_id, request)
        elif request.pattern == "react":
            result = await execute_react(task_id, request)
        elif request.pattern == "planning":
            result = await execute_planning(task_id, request)
        elif request.pattern == "multi_agent":
            result = await execute_multi_agent(task_id, request)
        else:
            raise ValueError(f"Unknown pattern: {request.pattern}")
        
        task["status"] = "completed"
        task["result"] = result
        
    except Exception as e:
        task["status"] = "failed"
        task["logs"].append({
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        })


async def execute_reflection(task_id: str, request: TaskRequest):
    """Execute reflection pattern."""
    agent = ReflectionAgent()
    result = await agent.execute(request.goal, request.messages)
    
    tasks[task_id]["logs"].extend(result["logs"])
    tasks[task_id]["reflection"] = result.get("reflection")
    
    return result["output"]


async def execute_tool_use(task_id: str, request: TaskRequest):
    """Execute tool use pattern."""
    agent = ToolUseAgent(tool_registry)
    result = await agent.execute(request.goal, request.messages, request.config)
    
    tasks[task_id]["logs"].extend(result["logs"])
    
    return result["output"]


async def execute_react(task_id: str, request: TaskRequest):
    """Execute ReAct pattern."""
    agent = ReActAgent(tool_registry)
    result = await agent.execute(request.goal, request.messages, request.config)
    
    tasks[task_id]["logs"].extend(result["logs"])
    
    return result["output"]


async def execute_planning(task_id: str, request: TaskRequest):
    """Execute planning pattern."""
    agent = PlanningAgent()
    result = await agent.execute(request.goal, request.messages, request.config)
    
    tasks[task_id]["logs"].extend(result["logs"])
    tasks[task_id]["plan"] = result.get("plan")
    
    return result["output"]


async def execute_multi_agent(task_id: str, request: TaskRequest):
    """Execute multi-agent pattern."""
    orchestrator = MultiAgentOrchestrator(list(agents.values()), tool_registry)
    result = await orchestrator.execute(request.goal, request.messages, request.config)
    
    tasks[task_id]["logs"].extend(result["logs"])
    
    return result["output"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
