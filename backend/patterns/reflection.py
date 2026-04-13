"""
Reflection Pattern Implementation

The agent critically evaluates its own output and suggests improvements
before finalizing. This reduces hallucinations and improves quality.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class ReflectionAgent:
    """
    Agent that implements the Reflection pattern.
    
    Process:
    1. Generate initial output
    2. Reflect on the output (self-critique)
    3. Revise based on reflection
    4. Return final output with reflection log
    """
    
    def __init__(self, model: str = "default"):
        self.model = model
        self.max_reflection_iterations = 2
    
    async def execute(
        self,
        goal: str,
        messages: List[Dict[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the reflection pattern.
        
        Args:
            goal: The task goal
            messages: Conversation history
            config: Configuration options
            
        Returns:
            Dictionary with output, logs, and reflection
        """
        config = config or {}
        logs = []
        
        # Step 1: Generate initial output
        logs.append({
            "type": "info",
            "message": "Generating initial output...",
            "timestamp": datetime.now().isoformat()
        })
        
        initial_output = await self._generate_initial_response(goal, messages)
        
        logs.append({
            "type": "initial_output",
            "content": initial_output,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Reflect on the output
        logs.append({
            "type": "info",
            "message": "Starting reflection phase...",
            "timestamp": datetime.now().isoformat()
        })
        
        reflection = await self._reflect(goal, initial_output, messages)
        
        logs.append({
            "type": "reflection",
            "content": reflection,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 3: Revise based on reflection
        logs.append({
            "type": "info",
            "message": "Revising output based on reflection...",
            "timestamp": datetime.now().isoformat()
        })
        
        revised_output = await self._revise(initial_output, reflection, goal)
        
        logs.append({
            "type": "revised_output",
            "content": revised_output,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "output": revised_output,
            "logs": logs,
            "reflection": reflection,
            "initial_output": initial_output
        }
    
    async def _generate_initial_response(
        self,
        goal: str,
        messages: List[Dict[str, str]]
    ) -> str:
        """Generate initial response to the goal."""
        # In production, this would call an LLM API
        # For now, simulate with a placeholder
        context = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        return f"""Initial solution for: {goal}

Context from conversation:
{context if context else "No additional context"}

[Initial implementation would be generated here by LLM]

This is a simulated initial output. In production, this would contain
the actual LLM-generated response to the user's goal."""
    
    async def _reflect(
        self,
        goal: str,
        output: str,
        messages: List[Dict[str, str]]
    ) -> str:
        """
        Reflect on the initial output.
        
        Questions to consider:
        - Is the output complete?
        - Does it handle edge cases?
        - Are there any errors or issues?
        - Can it be improved?
        """
        reflection_prompt = f"""
Reflect on the following output for the goal: "{goal}"

Output:
{output}

Consider:
1. Is this output complete and accurate?
2. Are there any errors, bugs, or issues?
3. Does it handle edge cases?
4. What improvements can be made?
5. Is anything missing?

Provide a detailed critique and specific improvement suggestions.
"""
        # In production, this would call an LLM API
        return """REFLECTION:

Thought: Let me critically evaluate the initial output...

Strengths:
- The general approach appears sound
- Basic structure is in place

Issues Identified:
1. Missing error handling for edge cases
2. No input validation present
3. Could benefit from additional documentation
4. Performance considerations not addressed

Suggestions for Improvement:
- Add try-catch blocks for robustness
- Include input validation at function boundaries
- Add docstrings and comments
- Consider optimization opportunities

Confidence Level: Medium - requires revision"""
    
    async def _revise(
        self,
        initial_output: str,
        reflection: str,
        goal: str
    ) -> str:
        """Revise the output based on reflection."""
        # In production, this would call an LLM API
        return f"""REVISED SOLUTION

Goal: {goal}

Based on the reflection feedback, here is the improved output:

[Revised implementation incorporating all feedback from reflection]

Changes Made:
1. Added comprehensive error handling
2. Implemented input validation
3. Added detailed documentation
4. Optimized performance-critical sections
5. Included example usage

This revised version addresses all concerns raised during reflection
and should be more robust and complete."""
