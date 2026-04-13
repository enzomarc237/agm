"""
Multi-Agent Pattern Implementation

Multiple AI agents with specific roles collaborate and communicate to solve
complex problems. Each agent has distinct capabilities and responsibilities.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class Agent:
    """Represents a single agent with a specific role."""
    
    def __init__(
        self,
        id: str,
        name: str,
        role: str,
        system_prompt: str,
        tools: List[str] = None
    ):
        self.id = id
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.message_history: List[Dict[str, str]] = []
    
    async def process(self, message: str, context: Dict[str, Any]) -> str:
        """Process a message and return response."""
        # In production, this would call an LLM API with the agent's system prompt
        self.message_history.append({"role": "user", "content": message})
        
        response = f"""[{self.name} - {self.role}]

Context: I am acting in my role as {self.role}.

Task/Message: {message[:200]}...

[This would contain the actual LLM-generated response based on my role,
system prompt, and the current context of the collaboration]

My expertise as {self.role} allows me to contribute:"""
        
        self.message_history.append({"role": "assistant", "content": response})
        return response
    
    def get_summary(self) -> Dict[str, Any]:
        """Get agent summary."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "tools": self.tools,
            "messages_exchanged": len(self.message_history)
        }


class MultiAgentOrchestrator:
    """
    Orchestrates collaboration between multiple agents.
    
    Process:
    1. Analyze the goal and determine which agents are needed
    2. Create a collaboration workflow
    3. Facilitate communication between agents
    4. Synthesize contributions into final output
    """
    
    def __init__(
        self,
        agents: List[Agent],
        tool_registry=None,
        model: str = "default"
    ):
        self.agents = {agent.id: agent for agent in agents}
        self.tool_registry = tool_registry
        self.model = model
        self.collaboration_log: List[Dict[str, Any]] = []
    
    async def execute(
        self,
        goal: str,
        messages: List[Dict[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the multi-agent pattern.
        
        Args:
            goal: The task goal
            messages: Conversation history
            config: Configuration options
            
        Returns:
            Dictionary with output and logs
        """
        config = config or {}
        logs = []
        
        # If no agents are configured, create default ones
        if not self.agents:
            await self._create_default_agents()
        
        # Step 1: Determine agent workflow
        logs.append({
            "type": "info",
            "message": "Setting up multi-agent collaboration...",
            "timestamp": datetime.now().isoformat()
        })
        
        workflow = await self._plan_workflow(goal, messages)
        
        logs.append({
            "type": "workflow_planned",
            "workflow": workflow,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Execute collaboration
        agent_contributions = []
        
        for step in workflow["steps"]:
            agent_id = step["agent_id"]
            task = step["task"]
            
            if agent_id not in self.agents:
                logs.append({
                    "type": "error",
                    "message": f"Agent {agent_id} not found",
                    "timestamp": datetime.now().isoformat()
                })
                continue
            
            agent = self.agents[agent_id]
            
            logs.append({
                "type": "agent_task_start",
                "agent": agent.name,
                "role": agent.role,
                "task": task,
                "timestamp": datetime.now().isoformat()
            })
            
            # Build context from previous contributions
            context = {
                "goal": goal,
                "previous_contributions": agent_contributions,
                "current_step": step
            }
            
            contribution = await agent.process(task, context)
            
            agent_contributions.append({
                "agent_id": agent_id,
                "agent_name": agent.name,
                "agent_role": agent.role,
                "task": task,
                "contribution": contribution
            })
            
            logs.append({
                "type": "agent_task_complete",
                "agent": agent.name,
                "role": agent.role,
                "contribution_preview": contribution[:200] + "...",
                "timestamp": datetime.now().isoformat()
            })
            
            self.collaboration_log.append({
                "step": step,
                "contribution": contribution,
                "timestamp": datetime.now().isoformat()
            })
        
        # Step 3: Synthesize final output
        logs.append({
            "type": "info",
            "message": "Synthesizing multi-agent contributions...",
            "timestamp": datetime.now().isoformat()
        })
        
        final_output = await self._synthesize_collaboration(goal, agent_contributions)
        
        return {
            "output": final_output,
            "logs": logs,
            "agent_contributions": agent_contributions,
            "workflow": workflow
        }
    
    async def _create_default_agents(self):
        """Create default set of agents."""
        default_agents = [
            Agent(
                id="agent_1",
                name="Researcher",
                role="Research Analyst",
                system_prompt="You are a research analyst who gathers and analyzes information.",
                tools=["web_search"]
            ),
            Agent(
                id="agent_2",
                name="Coder",
                role="Software Developer",
                system_prompt="You are an expert software developer who writes clean, efficient code.",
                tools=["code_interpreter"]
            ),
            Agent(
                id="agent_3",
                name="Reviewer",
                role="Quality Assurance",
                system_prompt="You are a QA specialist who reviews work for quality and correctness.",
                tools=[]
            ),
            Agent(
                id="agent_4",
                name="Coordinator",
                role="Project Manager",
                system_prompt="You coordinate tasks and ensure smooth collaboration between team members.",
                tools=[]
            )
        ]
        
        for agent in default_agents:
            self.agents[agent.id] = agent
    
    async def _plan_workflow(
        self,
        goal: str,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Plan the collaboration workflow."""
        # In production, this would use LLM to plan optimal agent workflow
        # For simulation, use heuristics
        
        goal_lower = goal.lower()
        
        # Default workflow
        workflow = {
            "steps": [
                {
                    "agent_id": "agent_4",  # Coordinator
                    "task": f"Analyze the goal and break it down: {goal}"
                },
                {
                    "agent_id": "agent_1",  # Researcher
                    "task": f"Gather relevant information for: {goal}"
                },
                {
                    "agent_id": "agent_2",  # Coder
                    "task": f"Implement solution based on research for: {goal}"
                },
                {
                    "agent_id": "agent_3",  # Reviewer
                    "task": f"Review and validate the implementation for: {goal}"
                }
            ]
        }
        
        # Customize workflow based on goal type
        if any(word in goal_lower for word in ["design", "visual", "creative"]):
            workflow["steps"] = [
                {
                    "agent_id": "agent_4",
                    "task": f"Understand design requirements: {goal}"
                },
                {
                    "agent_id": "agent_1",
                    "task": f"Research design trends and inspiration: {goal}"
                },
                {
                    "agent_id": "agent_2",
                    "task": f"Create initial design concepts: {goal}"
                },
                {
                    "agent_id": "agent_3",
                    "task": f"Critique and refine designs: {goal}"
                }
            ]
        
        return workflow
    
    async def _synthesize_collaboration(
        self,
        goal: str,
        contributions: List[Dict[str, Any]]
    ) -> str:
        """Synthesize all agent contributions into final output."""
        # In production, this would call an LLM API
        
        contributions_text = "\n\n".join([
            f"""### {c['agent_name']} ({c['agent_role']})
Task: {c['task']}
Contribution: {c['contribution'][:300]}..."""
            for c in contributions
        ])
        
        agent_list = ", ".join([
            f"{c['agent_name']} ({c['agent_role']})"
            for c in contributions
        ])
        
        return f"""# Multi-Agent Collaboration Result

## Goal
{goal}

## Participating Agents
{agent_list}

## Individual Contributions

{contributions_text}

## Synthesized Solution

Based on the collaborative effort of all agents, here is the comprehensive solution:

[This would contain the actual LLM-generated synthesis that combines
all agent contributions into a coherent, complete answer]

## Collaboration Summary

The Multi-Agent pattern enabled:
1. **Specialization**: Each agent contributed their unique expertise
2. **Division of Labor**: Complex tasks distributed across specialized agents
3. **Quality Control**: Review and validation by dedicated agent
4. **Coordination**: Orchestrated workflow ensuring logical progression
5. **Comprehensive Coverage**: Multiple perspectives on the problem

Total agents involved: {len(contributions)}
Total contributions: {len(contributions)}"""
