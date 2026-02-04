# Step 2: Two Agents (Sequential Pipeline)

**Duration:** 15 minutes (25-40 min of workshop)

## Learning Objectives
- Understand **agent chaining**: one agent's output → next agent's input
- Learn **division of labor**: specialized agents for distinct tasks
- Introduce **sequential workflows**: Critic → Fixer pattern

## Key Concept
**Agent Pipeline:** Connect multiple agents where each specializes in one task. The Critic identifies problems, the Fixer solves them. This is the foundation of multi-agent systems.

## What's New from Step 1
- Added a second agent (Fixer)
- Critic output feeds into Fixer input
- Shows how to compose agent results

## Prerequisites

Ensure you've completed the setup from Step 1:
- Virtual environment created and activated
- Dependencies installed (`pip install -r requirements.txt`)
- `.env` configured with your model provider (Azure OpenAI, OpenAI, Ollama, etc.)

See [Step 1 README](../step1_single_agent/README.md) for detailed setup instructions.

## Run This Step

From the repository root (with venv activated):

```bash
source .venv/bin/activate
python workshop/step2_two_agents/agentcon_demo.py
```

## Expected Output
1. **Critic Analysis**: Bullet points of architecture problems (public IPs, no encryption, etc.)
2. **Fixer Improvements**: Revised architecture using Azure App Service, Private Endpoints, managed identities

## What's Happening

### Agent Creation
```python
# Agent 1: Find problems
critic = ChatAgent(instructions="Review for security issues...")

# Agent 2: Fix problems
fixer = ChatAgent(instructions="Improve the architecture...")
```

### Sequential Execution
```python
critique = await critic.run(architecture)           # Step 1
improved = await fixer.run(f"Original: {architecture}\nCritique: {critique}")  # Step 2
```

The Fixer receives **both** the original architecture **and** the critique. This context helps it make targeted improvements.

## Discussion Points
- Why separate Critic and Fixer? (Specialized instructions, clearer reasoning)
- What other agents could we add? (Reviewer, Tester, Documenter)
- How to handle failures in the pipeline?

## 📖 Detailed Learning

For a comprehensive walkthrough of this step including:
- Understanding sequential pipelines in depth
- Passing context between agents
- Explanation of each code line and "why"
- Error handling between steps
- How providers work with two agents

👉 See the **[TUTORIAL.md](../../TUTORIAL.md#part-2-sequential-pipeline--critic--fixer)** file!

It covers Step 2 in detail with full explanations.

## Next: [Step 3 - Factory Pattern →](../step3_factory_pattern/)
