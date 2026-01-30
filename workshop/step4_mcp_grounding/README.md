# Step 4: MCP Grounding (Microsoft Learn)

**Duration:** 15 minutes (55-70 min of workshop)

## Learning Objectives
- Understand **Model Context Protocol (MCP)** for knowledge grounding
- Learn how to give agents **access to external knowledge bases**
- Configure **tool-based retrieval** from Microsoft Learn
- See agents **cite official documentation** in responses

## Key Concept
**MCP Grounding:** Connect agents to external knowledge sources (Microsoft Learn, GitHub, databases) so they provide **factually accurate, cited responses** instead of relying solely on LLM training data.

**Why MCP?**
- **Up-to-date information** (Learn docs are current)
- **Reduced hallucinations** (agents cite sources)
- **Domain expertise** (Azure-specific guidance)
- **Token budget control** (limit retrieval size)

## What's New from Step 3
- Added `MCPStreamableHTTPTool` initialization
- Connected to Microsoft Learn API: `https://learn.microsoft.com/api/mcp`
- Injected MCP tool into agents via factory: `tools=[self.mcp_tool]`
- Updated prompts to instruct agents to **use the tool**

## Run This Step
```bash
cd workshop\step4_mcp_grounding
python agentcon_demo.py
```

## Expected Output
1. **MCP Connection:** "🔌 Connecting to Microsoft Learn MCP..."
2. **Critic Output:** Now includes citations like "According to Microsoft Learn: [link]"
3. **Fixer Output:** References official Azure guidance with documentation URLs

## What's Happening

### MCP Tool Initialization
```python
mcp_tool = MCPStreamableHTTPTool(
    url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000",  # Token limit
    timeout=30
)
await mcp_tool.initialize()  # Connect before use
```

### Injecting Tool into Agents
```python
class AgentFactory:
    def __init__(self, chat_client, mcp_tool):
        self.mcp_tool = mcp_tool  # Store tool reference
    
    def create_agent(self, role):
        return ChatAgent(
            tools=[self.mcp_tool]  # Agent can now call Microsoft Learn
        )
```

### Prompt Updates
```python
instructions = """You are an Azure Architecture Critic.
**Use the Microsoft Learn MCP tool** to cite official documentation."""
```

The agent decides **when to call the tool** based on instructions. The framework handles:
- Tool invocation
- Response parsing
- Citation formatting

## Token Budget Control
`maxTokenBudget=3000` limits retrieval size per query. Why?
- **Cost control:** Large retrievals consume OpenAI tokens
- **Rate limits:** Avoid hitting 30k TPM limits
- **Latency:** Smaller retrievals = faster responses

## Discussion Points
- When to use MCP vs fine-tuning? (Dynamic knowledge vs static)
- Other MCP sources? (GitHub repos, Slack, databases, custom APIs)
- How agents decide when to use tools? (Instruction clarity)
- Security considerations? (Authentication, data access)

## Real-World MCP Use Cases
- **Customer support:** Ground on company knowledge base
- **Code review:** Ground on internal coding standards
- **Compliance:** Ground on regulatory documentation
- **Research:** Ground on scientific papers/databases

## Next: [Step 5 - Visualizer Agent →](../step5_visualizer/)
