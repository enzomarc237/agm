# AgenticMind

**AgenticMind** is a macOS desktop application designed to empower users to solve complex problems across various domains by leveraging advanced agentic AI patterns.

## Overview

Unlike traditional LLM interfaces that rely on single-turn prompts, AgenticMind provides a structured environment where LLMs can plan, reflect, use tools, and collaborate as multiple agents, leading to more reliable, robust, and insightful solutions.

## Architecture

```
agm/
├── backend/                 # FastAPI backend service
│   ├── main.py             # API server and routes
│   ├── patterns/           # Agentic pattern implementations
│   │   ├── reflection.py   # Self-correction & refinement
│   │   ├── tool_use.py     # External tool integration
│   │   ├── react.py        # Reasoning + Acting loop
│   │   ├── planning.py     # Multi-step task management
│   │   └── multi_agent.py  # Collaborative problem solving
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
│
├── frontend/               # Flutter macOS application
│   ├── lib/
│   │   ├── main.dart       # App entry point
│   │   ├── models/         # Data models
│   │   ├── providers/      # State management
│   │   ├── screens/        # UI screens
│   │   ├── services/       # API services
│   │   └── widgets/        # Reusable widgets
│   ├── pubspec.yaml        # Flutter dependencies
│   └── assets/             # Images, fonts, icons
│
├── tools/                  # Custom tool definitions
├── agents/                 # Agent configurations
└── config/                 # Configuration files
```

## Five Agentic Patterns

### 1. Reflection
The AI agent critically evaluates its own output and suggests improvements before finalizing. This reduces hallucinations and improves quality.

**User Experience:**
- See initial output
- View agent's self-critique
- Review revised output with changes highlighted

### 2. Tool Use
The AI agent accesses and utilizes external tools (web search, code interpreter, file system, APIs) to gather real-world data or perform actions.

**Built-in Tools:**
- Web Search
- Code Interpreter (Python)
- File Reader
- Calculator

### 3. ReAct (Reasoning + Acting)
The agent operates in a loop of Thought and Action, allowing it to adapt and course-correct based on intermediate results.

**User Experience:**
- Step-by-step reasoning log
- Interactive pauses for feedback
- Contextual intervention points

### 4. Planning
For complex problems, the agent generates a detailed plan, breaking the goal into manageable sub-tasks before execution.

**User Experience:**
- Plan generation and display
- Plan review and editing
- Progress tracking per step

### 5. Multi-Agent
Multiple AI agents with specific roles collaborate to solve problems. Each agent has distinct capabilities and responsibilities.

**Default Agents:**
- Researcher (Research Analyst)
- Coder (Software Developer)
- Reviewer (Quality Assurance)
- Coordinator (Project Manager)

## Getting Started

### Prerequisites

- **Backend:** Python 3.10+
- **Frontend:** Flutter 3.0+
- **Platform:** macOS

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The API server will start at `http://localhost:8000`.

### Frontend Setup

```bash
cd frontend
flutter pub get
flutter run -d macos
```

## API Endpoints

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{task_id}` - Get task status

### Agents
- `POST /agents` - Create an agent
- `GET /agents` - List all agents

### Tools
- `GET /tools` - List available tools
- `POST /tools/register` - Register custom tool

## Example Usage

### Create a Reflection Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Write a Python function to calculate fibonacci numbers",
    "pattern": "reflection"
  }'
```

### Create a Planning Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API for a todo application",
    "pattern": "planning"
  }'
```

## Configuration

Set LLM API keys via environment variables:

```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

## Roadmap

- [ ] Cross-platform support (Windows, Linux)
- [ ] Advanced tooling integrations (IDEs, Figma, etc.)
- [ ] Custom agent marketplace
- [ ] Visual workflow builder
- [ ] Voice interface
- [ ] Local LLM integration (Ollama, LM Studio)

## License

MIT License

---

**Document Version:** 1.0  
**Date:** 2023-10-27
