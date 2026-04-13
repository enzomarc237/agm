# AgenticMind Backend

FastAPI-based backend service for AgenticMind, implementing the five agentic AI patterns.

## Features

- **Reflection Pattern**: Self-correction and refinement of outputs
- **Tool Use Pattern**: Integration with external tools (web search, code interpreter, etc.)
- **ReAct Pattern**: Iterative reasoning and acting loop
- **Planning Pattern**: Multi-step task breakdown and execution
- **Multi-Agent Pattern**: Collaborative problem solving with multiple specialized agents

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Tasks
- `POST /tasks` - Create a new task with specified agentic pattern
- `GET /tasks/{task_id}` - Get task status and results

### Agents
- `POST /agents` - Create a new agent
- `GET /agents` - List all agents

### Tools
- `GET /tools` - List available tools
- `POST /tools/register` - Register a custom tool

## Example Usage

### Create a Reflection Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Write a Python function to calculate fibonacci numbers",
    "pattern": "reflection",
    "messages": []
  }'
```

### Create a Planning Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API for a todo application",
    "pattern": "planning",
    "messages": []
  }'
```

### Check Task Status

```bash
curl "http://localhost:8000/tasks/{task_id}"
```

## Architecture

```
backend/
├── main.py              # FastAPI application and routes
├── patterns/
│   ├── __init__.py      # Pattern exports
│   ├── reflection.py    # Reflection pattern implementation
│   ├── tool_use.py      # Tool use pattern implementation
│   ├── react.py         # ReAct pattern implementation
│   ├── planning.py      # Planning pattern implementation
│   └── multi_agent.py   # Multi-agent pattern implementation
└── requirements.txt     # Python dependencies
```

## Configuration

API keys for LLM providers should be set via environment variables:

```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

## Security Notes

- Tool execution runs in a sandboxed environment
- API keys are stored securely (integrate with macOS Keychain in production)
- CORS is configured for local development; update for production
