# Quick Reference: From Zero to Full Pipeline in 30 Minutes

## ⚡ Super Quick Start

### 1. Install & Setup (5 min)

```bash
# Clone
git clone https://github.com/your-repo/agentcon-cloud-repo.git
cd agentcon-cloud-repo

# Python env
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Ollama (3 min)

```bash
# Download from https://ollama.ai and install

# Terminal 1: Start server
ollama serve

# Terminal 2: Pull model
ollama pull gpt-oss:20b
```

### 3. Configure (1 min)

```bash
cp .env.example .env
# Already configured for Ollama by default
```

### 4. Run Pipeline (1 min)

```bash
python agentcon_demo.py
```

**Total: ~10 minutes to working system! ⚡**

---

## 📖 Step-by-Step Code Building

### Step 1: Single Agent (10 lines)

```python
import asyncio, os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

# Create client
client = OpenAIChatClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_id="gpt-4o-mini"
)

# Create agent
agent = ChatAgent(
    chat_client=client,
    instructions="Critique Azure architectures for security issues",
    name="critic"
)

# Run
async def main():
    response = await agent.run("VMs with public IPs, no encryption")
    print(response.text)

asyncio.run(main())
```

**Concepts:**
- `ChatAgent` = AI agent with specific role
- `instructions` = system prompt (personality)
- `await` = wait for async operation

---

### Step 2: Two Agents (20 lines)

```python
# Previous code...

async def main():
    # Agent 1: Identify problems
    critic = ChatAgent(
        chat_client=client,
        instructions="Identify architecture issues",
        name="critic"
    )
    critique = await critic.run(architecture)
    print("Critique:", critique.text)
    
    # Agent 2: Fix problems
    fixer = ChatAgent(
        chat_client=client,
        instructions="Improve architectures",
        name="fixer"
    )
    # Pass both original AND critique to fixer
    fixer_input = f"Original:\n{architecture}\nIssues:\n{critique.text}"
    improved = await fixer.run(fixer_input)
    print("Improved:", improved.text)
```

**Key Concept:** Pass context between agents for better results.

---

### Step 3: Factory Pattern (30 lines)

```python
class AgentFactory:
    def __init__(self, chat_client):
        self.chat_client = chat_client
        self.prompts = {
            "critic": "Identify issues...",
            "fixer": "Improve architectures...",
            "visualizer": "Create diagrams..."
        }
    
    def create_agent(self, role: str):
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],
            name=role
        )

# Usage
factory = AgentFactory(client)
critic = factory.create_agent("critic")
fixer = factory.create_agent("fixer")
visualizer = factory.create_agent("visualizer")
```

**Why?** Central place to manage all agents and prompts.

---

### Step 4: MCP Grounding (40 lines)

```python
from agent_framework import MCPStreamableHTTPTool

async def main():
    print("Connecting to Microsoft Learn...")
    
    async with MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000"
    ) as mcp_tool:
        factory = AgentFactory(client, mcp_tool)
        
        # Agents can now use MCP tool to verify info
        critic = factory.create_agent("critic")
        # Critic now cites official docs!
```

**Why MCP?** Prevent hallucinations — ground answers in real documentation.

---

### Step 5-7: Full Pipeline

See [TUTORIAL.md](./TUTORIAL.md) for complete walkthrough of:
- Step 5: Diagram generation (Mermaid)
- Step 6: Infrastructure as code (Bicep)
- Step 7: Image processing (photo → architecture)

---

## 🔧 Common Customizations

### Change Prompts

```python
self.prompts["critic"] = """Your custom prompt here.
Be very specific about what you want."""
```

### Add New Agent Role

```python
self.prompts["new_role"] = """Role instructions..."""

# Use it
agent = factory.create_agent("new_role")
```

### Switch Model Provider

```env
# In .env, uncomment ONE of these:

# OpenAI
USE_OPENAI=true
OPENAI_API_KEY=sk-...

# OR Ollama (default)
USE_OLLAMA=true
OLLAMA_MODEL=gpt-oss:20b

# OR Foundry Local
USE_FOUNDRY_LOCAL=true
LOCAL_BASE_URL=http://foundry:56238/v1
```

### Stream Responses Instead of Waiting

```python
async for chunk in agent.run_stream(text):
    if chunk.text:
        print(chunk.text, end="", flush=True)  # See responses in real-time
```

---

## 🐛 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| `Connection refused localhost:11434` | Start Ollama: `ollama serve` |
| `No such file: .env` | Create it: `cp .env.example .env` |
| `Invalid API key` | Check `.env` has correct OpenAI key |
| Empty agent response | Use helper: `text = get_text(response)` |
| "Model not found" | Pull it: `ollama pull gpt-oss:20b` |

---

## 📊 Architecture Comparison

### Single Agent (Step 1)
```
Input → Critic → Critique
```
Fast, but limited depth.

### Two Agents (Step 2)
```
Input → Critic → Critique → Fixer → Improved Architecture
```
Better results via multi-step reasoning.

### Full Pipeline (Steps 3-7)
```
Input
  ↓
Critic (MCP) → Issues with citations
  ↓
Fixer (MCP) → Improved architecture
  ↓
Visualizer → Mermaid diagram
  ↓
IaC Generator (MCP) → Bicep code
```
Production-grade output with documentation.

---

## 💡 Key Insights

1. **Async matters** - Agents stream responses, so use `async/await`
2. **Factory scales** - Managing 1 agent vs 10 is same complexity
3. **MCP prevents hallucinations** - Always ground in documentation
4. **Sequential pipelines work** - Each agent builds on previous
5. **Tools + prompting** - Use tools when model supports, fall back to prompting

---

## 🚀 Next Level

### Add Error Handling
```python
try:
    response = await agent.run(text)
except Exception as e:
    print(f"Error: {e}")
    # Fallback logic
```

### Add Caching
```python
@lru_cache(maxsize=100)
def get_critique(architecture: str):
    # Cache results to avoid reprocessing
```

### Add Web UI
```bash
pip install streamlit
# Create streamlit app for interactive use
```

### Deploy to Cloud
```bash
# Deploy to Azure Functions
func azure functionapp publish myapp
```

---

## 📚 Full Documentation

- **Detailed walkthrough:** [TUTORIAL.md](./TUTORIAL.md)
- **API reference:** Microsoft Agent Framework docs
- **Workshop examples:** `workshop/step*/agentcon_demo.py`
- **Configuration:** `.env.example`

---

**Start with Step 1, understand the concepts, then build up to the full pipeline!** 🎓
