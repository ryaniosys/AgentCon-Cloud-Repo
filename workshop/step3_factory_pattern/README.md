# Step 3: Factory Pattern

**Duration:** 15 minutes (40-55 min of workshop)

## Learning Objectives
- Understand the **Factory design pattern** for agent creation
- Centralize **prompts and configuration** in one place
- Use **enums** for type-safe agent role selection
- Eliminate code duplication

## Key Concept
**Factory Pattern:** Instead of creating agents manually each time, use a factory class that knows how to build agents. Benefits:
- **Single source of truth** for prompts
- **Easier maintenance** (change prompt once, affects all)
- **Consistency** across agent creation
- **Scalability** (easy to add new agent types)

## What's New from Step 2
- Added `AgentRole` enum (type-safe role names)
- Created `AgentFactory` class
- Centralized all prompts in factory
- Simplified agent creation: `factory.create_agent(AgentRole.CRITIC)`

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
python workshop/step3_factory_pattern/agentcon_demo.py
```

## Expected Output
Same as Step 2, but code is now organized with factory pattern.

## What's Happening

### Before (Step 2)
```python
# Duplicated ChatAgent(...) calls
critic = ChatAgent(chat_client=..., instructions="...", name="critic")
fixer = ChatAgent(chat_client=..., instructions="...", name="fixer")
```

### After (Step 3)
```python
# Factory pattern
factory = AgentFactory(chat_client)
critic = factory.create_agent(AgentRole.CRITIC)
fixer = factory.create_agent(AgentRole.FIXER)
```

### Factory Benefits
```python
class AgentFactory:
    def __init__(self, chat_client):
        self.chat_client = chat_client  # Shared across all agents
        self.prompts = { ... }          # All prompts in one place
    
    def create_agent(self, role: AgentRole) -> ChatAgent:
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],  # Lookup by role
            name=role.value
        )
```

## Discussion Points
- Why use enum vs strings? (Type safety, autocomplete, refactoring)
- When to use factory pattern? (3+ similar objects, shared config)
- How to add a new agent? (Add enum value, add prompt to dict)

## Real-World Benefits
In production, you might:
- Load prompts from external JSON/YAML files
- Add role-based access control
- Inject different tools per role
- Add monitoring/logging per agent type

## 📖 Detailed Learning

For a comprehensive walkthrough of this step including:
- Understanding factory pattern design
- Why enum over strings
- Explanation of each code line and "why"
- How to extend the factory with new roles
- Integration with multi-provider support

👉 See the **[TUTORIAL.md](../../TUTORIAL.md#part-3-factory-pattern--scalability)** file!

It covers Step 3 in detail with full explanations.

## Next: [Step 4 - MCP Grounding →](../step4_mcp_grounding/)
