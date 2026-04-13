"""
ReAct (Reasoning + Acting) Pattern Implementation

The agent operates in a loop of Thought (reasoning) and Action (tool use),
allowing it to adapt and course-correct based on intermediate results.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class ReActAgent:
    """
    Agent that implements the ReAct (Reasoning + Acting) pattern.
    
    Process (iterative loop):
    1. Thought: Reason about the current state and what to do next
    2. Action: Execute a tool or take an action
    3. Observation: Observe the result of the action
    4. Repeat until goal is achieved or max iterations reached
    """
    
    def __init__(self, tool_registry, model: str = "default", max_iterations: int = 10):
        self.tool_registry = tool_registry
        self.model = model
        self.max_iterations = max_iterations
    
    async def execute(
        self,
        goal: str,
        messages: List[Dict[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the ReAct pattern.
        
        Args:
            goal: The task goal
            messages: Conversation history
            config: Configuration options
            
        Returns:
            Dictionary with output and logs
        """
        config = config or {}
        logs = []
        iteration = 0
        
        # Initialize context
        context = {
            "goal": goal,
            "messages": messages,
            "observations": [],
            "thoughts": []
        }
        
        logs.append({
            "type": "info",
            "message": f"Starting ReAct loop (max iterations: {self.max_iterations})",
            "timestamp": datetime.now().isoformat()
        })
        
        while iteration < self.max_iterations:
            iteration += 1
            
            # Step 1: Thought - Reason about what to do
            logs.append({
                "type": "iteration_start",
                "iteration": iteration,
                "timestamp": datetime.now().isoformat()
            })
            
            thought = await self._generate_thought(context)
            
            context["thoughts"].append(thought)
            logs.append({
                "type": "thought",
                "iteration": iteration,
                "content": thought,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check if we should stop (goal achieved)
            if self._should_stop(thought):
                logs.append({
                    "type": "info",
                    "message": "Goal achieved, ending ReAct loop",
                    "timestamp": datetime.now().isoformat()
                })
                break
            
            # Step 2: Action - Decide and execute action
            action = await self._select_action(thought, context)
            
            if action["type"] == "final_answer":
                logs.append({
                    "type": "action",
                    "iteration": iteration,
                    "action": "final_answer",
                    "content": action.get("content", ""),
                    "timestamp": datetime.now().isoformat()
                })
                return {
                    "output": action.get("content", ""),
                    "logs": logs,
                    "iterations": iteration,
                    "thoughts": context["thoughts"],
                    "observations": context["observations"]
                }
            
            # Execute the action (tool use)
            logs.append({
                "type": "action",
                "iteration": iteration,
                "action": action["type"],
                "parameters": action.get("parameters", {}),
                "timestamp": datetime.now().isoformat()
            })
            
            try:
                observation = await self._execute_action(action)
                
                context["observations"].append(observation)
                logs.append({
                    "type": "observation",
                    "iteration": iteration,
                    "observation": observation,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                error_observation = {"error": str(e)}
                context["observations"].append(error_observation)
                logs.append({
                    "type": "observation_error",
                    "iteration": iteration,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        # Generate final answer after all iterations
        final_output = await self._generate_final_answer(context)
        
        return {
            "output": final_output,
            "logs": logs,
            "iterations": iteration,
            "thoughts": context["thoughts"],
            "observations": context["observations"]
        }
    
    async def _generate_thought(self, context: Dict[str, Any]) -> str:
        """Generate a thought based on current context."""
        # In production, this would call an LLM API
        goal = context["goal"]
        num_observations = len(context["observations"])
        
        if num_observations == 0:
            return f"""Thought: I need to solve the goal: "{goal}"
I should start by gathering relevant information.
Let me think about what tools or actions would be most helpful.
First, I need to understand what information I already have and what I need to find."""
        else:
            return f"""Thought: I've gathered {num_observations} pieces of information so far.
Based on my previous observations, I should now...
Let me analyze what I've learned and determine the next best step.
I'm making progress toward solving: {goal}"""
    
    async def _select_action(
        self,
        thought: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Select the next action based on thought and context."""
        # In production, this would use LLM to parse thought and select action
        # For simulation, use simple heuristics
        
        available_tools = self.tool_registry.list_tools()
        
        # Simple heuristic: alternate between search and final answer
        num_obs = len(context["observations"])
        
        if num_obs == 0:
            # First action: search for information
            return {
                "type": "web_search",
                "parameters": {"query": context["goal"]}
            }
        elif num_obs < 2:
            # Second action: another search or calculation
            return {
                "type": "calculator",
                "parameters": {"expression": "1 + 1"}
            }
        else:
            # Final action: provide answer
            return {
                "type": "final_answer",
                "content": "Placeholder final answer"
            }
    
    async def _execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action and return observation."""
        if action["type"] == "final_answer":
            return {"answer": action.get("content")}
        
        # Execute tool
        return await self.tool_registry.execute_tool(
            action["type"],
            **action.get("parameters", {})
        )
    
    def _should_stop(self, thought: str) -> bool:
        """Determine if the ReAct loop should stop."""
        # Check for stop indicators in thought
        stop_indicators = [
            "i have enough information",
            "i can now answer",
            "goal achieved",
            "task complete"
        ]
        thought_lower = thought.lower()
        return any(indicator in thought_lower for indicator in stop_indicators)
    
    async def _generate_final_answer(self, context: Dict[str, Any]) -> str:
        """Generate final answer based on all thoughts and observations."""
        # In production, this would call an LLM API
        
        thoughts_str = "\n".join([f"- {t[:100]}..." for t in context["thoughts"]])
        observations_str = "\n".join([
            f"- {json.dumps(o)[:100]}..." 
            for o in context["observations"]
        ])
        
        return f"""FINAL ANSWER

Goal: {context["goal"]}

Thought Process Summary:
{thoughts_str}

Observations Gathered:
{observations_str}

---

Based on my reasoning process and the information gathered through the ReAct loop,
here is my comprehensive answer:

[This would contain the actual LLM-generated response that synthesizes
all the thoughts and observations to provide a complete answer to the goal]

The ReAct pattern allowed me to:
1. Break down the problem iteratively
2. Take actions based on reasoning
3. Adapt my approach based on observations
4. Course-correct when needed

Total iterations: {len(context["thoughts"])}"""
