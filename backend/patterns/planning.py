"""
Planning Pattern Implementation

For complex problems, the agent generates a detailed plan, breaking the overall
goal into smaller, manageable sub-tasks before attempting to execute.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class PlanningAgent:
    """
    Agent that implements the Planning pattern.
    
    Process:
    1. Analyze the goal and generate a step-by-step plan
    2. Present plan for review (optionally allow user editing)
    3. Execute each step in sequence
    4. Track progress and adapt plan if needed
    5. Synthesize results into final output
    """
    
    def __init__(self, model: str = "default"):
        self.model = model
    
    async def execute(
        self,
        goal: str,
        messages: List[Dict[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the planning pattern.
        
        Args:
            goal: The task goal
            messages: Conversation history
            config: Configuration options (may include 'user_edited_plan')
            
        Returns:
            Dictionary with output, logs, and plan
        """
        config = config or {}
        logs = []
        
        # Step 1: Generate initial plan
        logs.append({
            "type": "info",
            "message": "Generating plan for complex task...",
            "timestamp": datetime.now().isoformat()
        })
        
        plan = await self._generate_plan(goal, messages)
        
        logs.append({
            "type": "plan_generateda",
            "plan": plan,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check if user provided an edited plan
        user_edited_plan = config.get("user_edited_plan")
        if user_edited_plan:
            logs.append({
                "type": "info",
                "message": "Using user-edited plan",
                "timestamp": datetime.now().isoformat()
            })
            plan = user_edited_plan
        
        # Step 2: Execute each step in the plan
        logs.append({
            "type": "info",
            "message": f"Executing plan with {len(plan)} steps...",
            "timestamp": datetime.now().isoformat()
        })
        
        step_results = []
        for i, step in enumerate(plan):
            logs.append({
                "type": "step_start",
                "step_number": i + 1,
                "step_description": step,
                "timestamp": datetime.now().isoformat()
            })
            
            result = await self._execute_step(step, goal, messages, step_results)
            
            step_results.append({
                "step": step,
                "result": result,
                "status": "completed"
            })
            
            logs.append({
                "type": "step_complete",
                "step_number": i + 1,
                "result_summary": result[:200] + "..." if len(result) > 200 else result,
                "timestamp": datetime.now().isoformat()
            })
        
        # Step 3: Synthesize final output
        logs.append({
            "type": "info",
            "message": "Synthesizing final output from all steps...",
            "timestamp": datetime.now().isoformat()
        })
        
        final_output = await self._synthesize_output(goal, plan, step_results)
        
        return {
            "output": final_output,
            "logs": logs,
            "plan": plan,
            "step_results": step_results
        }
    
    async def _generate_plan(
        self,
        goal: str,
        messages: List[Dict[str, str]]
    ) -> List[str]:
        """Generate a step-by-step plan for achieving the goal."""
        # In production, this would call an LLM API
        # For simulation, use heuristics based on goal type
        
        goal_lower = goal.lower()
        
        # Detect task type and generate appropriate plan
        if any(word in goal_lower for word in ["code", "program", "script", "function"]):
            return [
                "Understand the requirements and constraints",
                "Design the solution architecture",
                "Implement core functionality",
                "Add error handling and edge cases",
                "Write tests and documentation",
                "Review and optimize code"
            ]
        elif any(word in goal_lower for word in ["research", "analyze", "study"]):
            return [
                "Define research questions and scope",
                "Gather relevant sources and data",
                "Analyze and synthesize information",
                "Identify patterns and insights",
                "Draft findings and conclusions",
                "Review and refine analysis"
            ]
        elif any(word in goal_lower for word in ["design", "create", "visual"]):
            return [
                "Understand design requirements and audience",
                "Research inspiration and best practices",
                "Generate initial concepts",
                "Refine selected concept",
                "Create detailed design",
                "Gather feedback and iterate"
            ]
        else:
            # Generic problem-solving plan
            return [
                "Understand and clarify the problem",
                "Break down into sub-problems",
                "Gather necessary information",
                "Develop potential solutions",
                "Evaluate and select best approach",
                "Implement and verify solution"
            ]
    
    async def _execute_step(
        self,
        step: str,
        goal: str,
        messages: List[Dict[str, str]],
        previous_results: List[Dict[str, Any]]
    ) -> str:
        """Execute a single step of the plan."""
        # In production, this would call an LLM API with context from previous steps
        
        context_from_previous = ""
        if previous_results:
            context_from_previous = "\n".join([
                f"Step {i+1} ({r['step']}): {r['result'][:100]}..."
                for i, r in enumerate(previous_results)
            ])
        
        return f"""Result for step: "{step}"

Context from previous steps:
{context_from_previous if context_from_previous else "No previous steps"}

[This would contain the actual LLM-generated output for this specific step,
building upon previous results and working toward the overall goal: {goal}]

The step has been completed successfully."""
    
    async def _synthesize_output(
        self,
        goal: str,
        plan: List[str],
        step_results: List[Dict[str, Any]]
    ) -> str:
        """Synthesize all step results into a coherent final output."""
        # In production, this would call an LLM API
        
        results_summary = "\n\n".join([
            f"### Step {i+1}: {r['step']}\n{r['result']}"
            for i, r in enumerate(step_results)
        ])
        
        return f"""# Complete Solution

## Goal
{goal}

## Execution Plan
{json.dumps([{"step": i+1, "description": s} for i, s in enumerate(plan)], indent=2)}

## Step-by-Step Results

{results_summary}

## Final Synthesis

Based on the systematic execution of all planned steps, here is the comprehensive solution:

[This would contain the actual LLM-generated synthesis that combines all step results
into a coherent, complete answer to the original goal]

## Summary

The Planning pattern enabled:
1. **Structured Approach**: Breaking a complex problem into manageable steps
2. **Progress Tracking**: Clear visibility into what's been completed
3. **Context Building**: Each step builds on previous results
4. **Adaptability**: Plan can be modified mid-execution if needed
5. **Completeness**: Ensures all aspects of the problem are addressed

Total steps executed: {len(plan)}"""
