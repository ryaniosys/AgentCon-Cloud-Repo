# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Public Repository

This is a **public fork**. Never commit sensitive information including API keys, credentials, tokens, or proprietary business data.

## Project Overview

AgentCon Cloud Repo is a production-ready demonstration of multi-agent AI for Azure cloud architecture analysis and generation. It showcases how agentic workflows can critique, fix, visualize, and generate Infrastructure-as-Code using the Microsoft Agent Framework and Model Context Protocol (MCP).

## Common Commands

### Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Demo
```bash
python agentcon_demo.py                        # Text mode
USE_IMAGE_MODE=true python agentcon_demo.py    # Image diagram mode
```

### Testing
```bash
pip install -r requirements-test.txt

# Unit tests only (no API key required)
pytest tests/test_agentcon_demo.py tests/test_agentcon_demo_refactored.py -v

# Run specific test marker
pytest -m unit -v                  # Unit tests only
pytest -m evaluation -v            # Evaluation tests (requires OPENAI_API_KEY)
pytest -m "not evaluation" -v      # Skip API-dependent tests

# With coverage
pytest tests/ -v --cov=agentcon_demo --cov-report=term-missing
```

### Workshop Steps
Each step is self-contained and can be run independently:
```bash
cd workshop/step1_single_agent && python agentcon_demo.py
cd workshop/step2_two_agents && python agentcon_demo.py
# ... through step7_image_mode
```

## Architecture

### Multi-Agent Pipeline
```
Input (text/image)
    ↓
[STEP 0] Diagram Interpreter (optional, image → text)
    ↓
[STEP 1] Critic Agent (MCP-grounded) → Identifies architectural issues
    ↓
[STEP 2] Fixer Agent (MCP-grounded) → Provides recommendations
    ↓
[STEP 3] Visualizer Agent → Generates Mermaid diagram
    ↓
[STEP 4] IaC Generator Agent (MCP-grounded) → Produces Bicep code
    ↓
Output saved to output/ directory
```

### Key Components

- **`AgentFactory`** - Centralizes agent creation with role-specific prompts and MCP tool injection
- **`AgentRole` enum** - Type-safe agent role specification (CRITIC, FIXER, VISUALIZER, IAC_GENERATOR, DIAGRAM_INTERPRETER)
- **`InputStrategy` protocol** (refactored version) - Abstracts text vs image input handling
- **`agent_prompts.yaml`** (refactored version) - Declarative agent configuration

### Model Provider Priority
Provider selection: OpenAI > Ollama > Foundry Local (configured via `.env`)

MCP tools are conditionally enabled based on model capabilities:
- OpenAI: Full tool support
- Ollama: No tool/function calling
- Foundry Local: Limited tool support

## Configuration

Copy `.env.example` to `.env` and configure your preferred model provider:

```env
# Option 1: OpenAI (recommended for full functionality)
USE_OPENAI=true
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o-mini

# Option 2: Ollama (local, free)
USE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gpt-oss:20b

# Option 3: Microsoft Foundry Local (enterprise)
USE_FOUNDRY_LOCAL=true
LOCAL_BASE_URL=http://localhost:56238/v1
LOCAL_MODEL=gpt-oss-20b-generic-cpu:1
```

## Key Files

| File | Purpose |
|------|---------|
| `agentcon_demo.py` | Main demo with factory pattern |
| `refactored/agentcon_demo_refactored.py` | Clean architecture version |
| `refactored/agent_prompts.yaml` | Declarative agent configurations |
| `workshop/` | 7-step progressive tutorial |
| `tests/` | Unit and evaluation test suite |

## Test Markers

- `@pytest.mark.unit` - Mocked tests, no API required
- `@pytest.mark.evaluation` - Real API calls, requires OPENAI_API_KEY
- `@pytest.mark.integration` - Integration tests without external APIs
- `@pytest.mark.slow` - Long-running tests
