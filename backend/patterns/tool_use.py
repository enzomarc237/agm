"""
Tool Use Pattern Implementation

The agent can access and utilize external tools (web search, code interpreter,
file system access, APIs) to gather real-world data or perform actions.
"""

from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import json


class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_builtin_tools()
    
    def _register_builtin_tools(self):
        """Register built-in tools."""
        
        # Web Search Tool
        self.register_tool({
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            },
            "handler": self._web_search_handler
        })
        
        # Code Interpreter Tool
        self.register_tool({
            "name": "code_interpreter",
            "description": "Execute Python code in a sandboxed environment",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"},
                    "timeout": {"type": "integer", "description": "Execution timeout in seconds"}
                },
                "required": ["code"]
            },
            "handler": self._code_interpreter_handler
        })
        
        # File Reader Tool
        self.register_tool({
            "name": "file_reader",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"]
            },
            "handler": self._file_reader_handler
        })
        
        # Calculator Tool
        self.register_tool({
            "name": "calculator",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Mathematical expression"}
                },
                "required": ["expression"]
            },
            "handler": self._calculator_handler
        })
    
    def register_tool(self, tool_def: Dict[str, Any]):
        """Register a new tool."""
        self.tools[tool_def["name"]] = tool_def
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools."""
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"]
            }
            for t in self.tools.values()
        ]
    
    async def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool with given parameters."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        handler = tool.get("handler")
        if not handler:
            raise ValueError(f"No handler for tool: {name}")
        
        return await handler(**kwargs)
    
    # Built-in tool handlers
    async def _web_search_handler(self, query: str) -> Dict[str, Any]:
        """Web search handler (simulated)."""
        # In production, this would call a real search API
        return {
            "results": [
                {"title": f"Result for: {query}", "url": "https://example.com", "snippet": "..."},
            ],
            "query": query
        }
    
    async def _code_interpreter_handler(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """Code interpreter handler (simulated)."""
        # In production, this would execute code in a sandboxed environment
        return {
            "output": f"Executed code: {code[:100]}...",
            "status": "success",
            "execution_time": 0.5
        }
    
    async def _file_reader_handler(self, path: str) -> Dict[str, Any]:
        """File reader handler."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            return {"content": content, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    async def _calculator_handler(self, expression: str) -> Dict[str, Any]:
        """Calculator handler."""
        try:
            # Safe evaluation of mathematical expressions
            result = eval(expression, {"__builtins__": {}}, {})
            return {"result": result, "expression": expression}
        except Exception as e:
            return {"error": str(e), "expression": expression}


class ToolUseAgent:
    """
    Agent that implements the Tool Use pattern.
    
    Process:
    1. Analyze the goal to determine if tools are needed
    2. Select appropriate tool(s)
    3. Execute tool(s) with proper parameters
    4. Integrate tool output into response
    """
    
    def __init__(self, tool_registry: ToolRegistry, model: str = "default"):
        self.tool_registry = tool_registry
        self.model = model
    
    async def execute(
        self,
        goal: str,
        messages: List[Dict[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the tool use pattern.
        
        Args:
            goal: The task goal
            messages: Conversation history
            config: Configuration options
            
        Returns:
            Dictionary with output and logs
        """
        config = config or {}
        logs = []
        
        # Step 1: Determine which tools to use
        logs.append({
            "type": "info",
            "message": "Analyzing goal to determine required tools...",
            "timestamp": datetime.now().isoformat()
        })
        
        tool_selection = await self._select_tools(goal, messages)
        
        logs.append({
            "type": "tool_selection",
            "tools": tool_selection,
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Execute selected tools
        tool_outputs = []
        for tool_info in tool_selection:
            tool_name = tool_info["name"]
            params = tool_info["parameters"]
            
            logs.append({
                "type": "tool_invocation_start",
                "tool": tool_name,
                "parameters": params,
                "timestamp": datetime.now().isoformat()
            })
            
            try:
                output = await self.tool_registry.execute_tool(tool_name, **params)
                
                logs.append({
                    "type": "tool_invocation_result",
                    "tool": tool_name,
                    "output": output,
                    "timestamp": datetime.now().isoformat()
                })
                
                tool_outputs.append({
                    "tool": tool_name,
                    "output": output,
                    "status": "success"
                })
            except Exception as e:
                logs.append({
                    "type": "tool_invocation_error",
                    "tool": tool_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                
                tool_outputs.append({
                    "tool": tool_name,
                    "error": str(e),
                    "status": "failed"
                })
        
        # Step 3: Generate final response integrating tool outputs
        logs.append({
            "type": "info",
            "message": "Generating response with tool outputs...",
            "timestamp": datetime.now().isoformat()
        })
        
        final_output = await self._generate_response(goal, tool_outputs, messages)
        
        return {
            "output": final_output,
            "logs": logs,
            "tool_outputs": tool_outputs
        }
    
    async def _select_tools(
        self,
        goal: str,
        messages: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Select appropriate tools for the task."""
        # In production, this would use LLM to decide which tools to use
        # For simulation, use simple keyword matching
        
        tools_to_use = []
        goal_lower = goal.lower()
        
        if any(word in goal_lower for word in ["search", "find", "look up"]):
            tools_to_use.append({
                "name": "web_search",
                "parameters": {"query": goal}
            })
        
        if any(word in goal_lower for word in ["calculate", "compute", "math"]):
            tools_to_use.append({
                "name": "calculator",
                "parameters": {"expression": "2 + 2"}  # Placeholder
            })
        
        if any(word in goal_lower for word in ["code", "execute", "run"]):
            tools_to_use.append({
                "name": "code_interpreter",
                "parameters": {"code": "print('Hello')"}  # Placeholder
            })
        
        # Default to no tools if nothing matched
        if not tools_to_use:
            # For demo purposes, show what tools are available
            return []
        
        return tools_to_use
    
    async def _generate_response(
        self,
        goal: str,
        tool_outputs: List[Dict[str, Any]],
        messages: List[Dict[str, str]]
    ) -> str:
        """Generate final response integrating tool outputs."""
        # In production, this would call an LLM API
        
        response = f"""Response to: {goal}

Tool Results:
"""
        
        for output in tool_outputs:
            response += f"\n--- Tool: {output['tool']} ---\n"
            if output['status'] == 'success':
                response += f"Output: {json.dumps(output['output'], indent=2)}"
            else:
                response += f"Error: {output.get('error', 'Unknown error')}"
        
        response += """

Based on the tool outputs above, here is my comprehensive answer:

[LLM would generate a natural language response that integrates
the tool results to answer the user's original goal]

This demonstrates the Tool Use pattern where the agent:
1. Identified relevant tools
2. Executed them with appropriate parameters
3. Integrated the results into a coherent response"""
        
        return response
