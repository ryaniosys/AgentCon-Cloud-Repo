# AI Architecture Critic: How Agentic AI Designs, Fixes and Visualizes Cloud Systems

<div align="center">

![AgentCon Zürich](zurich-transparent-crop.png)

![Igor Iric](iric-igor-speaker.jpeg)

**AgentCon Zürich | Workshop Wed 1:30 pm - 3:00 pm**

**Igor Iric** | AI Architecture Critic Workshop

</div>

---

> **Conference-ready demonstration of Agentic AI with real-time documentation grounding using Microsoft Agent Framework**

## 📢 About This Workshop

In this session, I show how **Agentic AI** can radically change the way we design, evaluate and visualize cloud systems using the **Microsoft Agent Framework**.

I will demonstrate a lightweight multi-agent workflow, an **AI Architecture Critic & Fixer** and how it collaborates with my open-source project **Cloud Visualizer Pro**, which generates Azure-ready architectures directly from text or rough sketches.

**Attendees will learn:**
- ✅ How to build practical Agentic workflows in **<150 lines of code**
- ✅ How AI can detect architectural risks, security gaps and misconfigurations
- ✅ How agents can auto-improve designs using Azure best practices
- ✅ How to generate visual and deployable IaC (Bicep/Terraform) from text
- ✅ How enterprises can integrate this pattern into real engineering teams

This talk is perfect for developers, architects and engineering leaders who want to see Agentic AI applied to **real cloud problems, not theoretical demos**.

---

## 🎯 What This Demo Shows

**Key Concept**: Agentic AI is not just reasoning — it's **reasoning grounded in real documentation**.

This demo showcases how **Microsoft Agent Framework (MAF)** agents can analyze Azure architectures and ground their decisions in official Microsoft Learn documentation using the **Model Context Protocol (MCP)**.

### Microsoft Agent Framework

The **Microsoft Agent Framework** is a Python-based framework for building intelligent, multi-agent AI applications. It provides:

- **🤖 Agent Orchestration** - Coordinate multiple AI agents with different roles and capabilities
- **🔧 Tool Integration** - Built-in support for MCP, function calling, and external APIs
- **📊 Streaming Support** - Real-time streaming responses for live reasoning display
- **🛡️ Enterprise-Ready** - Production-grade error handling, observability, and security
- **🔗 Multi-Model Support** - Works with OpenAI, Azure OpenAI, and other LLM providers

The framework enables developers to build sophisticated AI workflows in minimal code while maintaining enterprise-grade reliability.

### Demo Capabilities

The demo demonstrates:
- 🤖 **Agent Factory Pattern** - Centralized agent creation with role-specific capabilities
- 📚 **Microsoft Learn MCP Integration** - Agents query official Azure documentation
- 🔍 **Architecture Analysis** - AI critiques and improves cloud architectures
- 🏗️ **IaC Generation** - Produces grounded Bicep code with validated resource types
- 🖼️ **Image Recognition** - Converts architecture diagrams to actionable insights
- ⚡ **Live Streaming** - Watch agents reason in real-time
- 💾 **File Output** - All responses saved to timestamped text files

## 🏗️ Architecture Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT                                                       │
│  • Text description OR diagram image                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 0: Diagram Interpreter (if image)                     │
│  • Converts image → structured text                        │
│  • No MCP needed                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Architecture Critic (MCP-grounded)                  │
│  • Identifies security gaps                                │
│  • Detects wrong service choices                           │
│  • Cites Microsoft Learn documentation                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Architecture Fixer (MCP-grounded)                   │
│  • Applies Well-Architected Framework                      │
│  • Prefers managed services over IaaS                      │
│  • Validates choices against Microsoft Learn               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Diagram Visualizer                                  │
│  • Generates Mermaid diagram syntax                         │
│  • No MCP needed                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: IaC Generator (MCP-grounded)                        │
│  • Produces Bicep code snippets                            │
│  • Confirms resource types via Microsoft Learn             │
│  • Validates API versions                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
                     ✅ OUTPUT
          • Critique + Improved Architecture
          • Mermaid Diagram (visualize on GitHub/Mermaid Live)
          • Grounded Bicep Code
          • All saved to output/*.txt files
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (3.12 recommended)
- **OpenAI API Key** (or Azure OpenAI credentials)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "AgentCon Cloud Repo"
```

### Step 2: Create Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv .venv
```

**macOS/Linux:**
```bash
python3 -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `agent-framework-core==1.0.0b251204` - Microsoft Agent Framework (stable version)
- `openai` - OpenAI Python SDK
- `python-dotenv` - Environment variable management
- `mcp` - Model Context Protocol client
- Additional dependencies (httpx, pydantic, etc.)

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy from template
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
OPENAI_MODEL=gpt-4o-mini

# Image Recognition Mode (Optional)
USE_IMAGE_MODE=false
ARCHITECTURE_IMAGE_PATH=
```

### Step 6: Run the Demo

**Text Mode (Default):**
```bash
python agentcon_demo.py
```

The demo will:
1. ✅ Connect to Microsoft Learn MCP
2. ✅ Analyze the built-in 3-tier architecture example
3. ✅ Stream live reasoning to console
4. ✅ Save all outputs to `output/*.txt` files

**Expected Output:**
```
🔌 Connecting to Microsoft Learn MCP...
🤖 Using model: gpt-4o-mini
📝 Text mode (default)

============================================================
🎯 INPUT ARCHITECTURE
============================================================
...
============================================================
🔍 STEP 1: Architecture Critic (MCP-grounded)
============================================================
[Live streaming text appears here...]
💾 Saved to: output/step1_critic_20260129_120345.txt
...
============================================================
✅ PIPELINE COMPLETE
============================================================
```

## 🖼️ Image Diagram Recognition

To analyze architecture diagrams (like `images/HubSpoke.png`):

### Step 1: Update `.env`

```env
USE_IMAGE_MODE=true
ARCHITECTURE_IMAGE_PATH=images/HubSpoke.png
```

### Step 2: Run the Demo

```bash
python agentcon_demo.py
```

The pipeline will now include:
- **STEP 0: Diagram Interpreter** - Converts image to structured text
- Then proceeds with critique, fixing, visualization, and IaC generation

**Supported Formats:**
- Local files: `images/HubSpoke.png`, `diagrams/my-arch.jpg`
- URLs: `https://example.com/diagram.png`
- Formats: PNG, JPG, JPEG

## 🔌 MCP Configuration

### Using Microsoft Learn MCP (Default)

The demo connects to Microsoft Learn MCP by default:

```python
MCPStreamableHTTPTool(
    name="microsoft_learn",
    url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000"
)
```

**Token Budget Control:**
- `maxTokenBudget=3000` limits MCP response tokens (prevents rate limits)
- Increase for more detailed documentation: `?maxTokenBudget=5000`
- Decrease for faster responses: `?maxTokenBudget=1500`

### Disabling MCP (Agents Without Grounding)

To run agents without MCP (faster but less grounded):

**Option 1: Modify Agent Factory**

Edit `agentcon_demo.py`:

```python
def create_agent(self, role: AgentRole) -> ChatAgent:
    # ...
    # Change this line:
    tools = [self.mcp_tool] if role != AgentRole.VISUALIZER else []
    
    # To (no MCP for any agent):
    tools = []
```

**Option 2: Comment Out MCP Initialization**

```python
async def main():
    # Comment out MCP section:
    # async with MCPStreamableHTTPTool(...) as mcp_tool:
    #     factory = AgentFactory(mcp_tool)
    
    # Use without MCP:
    factory = AgentFactory(None)
```

⚠️ **Note:** Without MCP, agents rely on training data and may produce less accurate or outdated recommendations.

## 📁 Output Files

All agent responses are automatically saved to the `output/` directory:

```
output/
├── step1_critic_20260129_120345.txt      # Architecture critique
├── step2_fixer_20260129_120412.txt       # Improved architecture
├── step3_mermaid_diagram_20260129_120438.txt  # Mermaid diagram
└── step4_bicep_20260129_120502.txt       # Bicep IaC code
```

**Viewing Mermaid Diagrams:**
1. Copy content from `step3_mermaid_diagram_*.txt`
2. Paste into [Mermaid Live Editor](https://mermaid.live/)
3. Or view directly on GitHub (supports Mermaid in markdown)

## ⚙️ Advanced Configuration

### Changing Models

Edit `.env` to use different OpenAI models:

```env
# Fast and cost-effective (recommended for demos)
OPENAI_MODEL=gpt-4o-mini

# More capable (better for complex architectures)
OPENAI_MODEL=gpt-4o

# Latest model (if available)
OPENAI_MODEL=gpt-5-mini
```

### Using Azure OpenAI

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

Update `agentcon_demo.py` to use Azure OpenAI client (see Microsoft Agent Framework docs).

### Customizing Agent Prompts

Edit the `prompts` dictionary in `agentcon_demo.py`:

```python
prompts = {
    AgentRole.CRITIC: """Your custom critic prompt here...""",
    AgentRole.FIXER: """Your custom fixer prompt here...""",
    # ...
}
```

## 🎨 Live Demo Tips

### For Conference Presentations

1. **Pre-warm the demo**: Run once before presenting to cache MCP responses
2. **Use image mode**: Shows diagram → critique flow (more visual)
3. **Explain streaming**: Point out live reasoning appearing in console
4. **Show saved files**: Open `output/` folder to show persistence
5. **Visualize Mermaid**: Have [Mermaid Live](https://mermaid.live/) open in browser

### Troubleshooting

**Rate Limits:**
- Reduce `maxTokenBudget` in MCP URL: `?maxTokenBudget=2000`
- Use `gpt-4o-mini` instead of `gpt-4o`
- Add delays between agent calls

**Image Recognition Issues:**
- Ensure image file exists and path is correct
- Check image format (PNG/JPG/JPEG only)
- For URLs, verify image is publicly accessible

**MCP Connection Errors:**
- Check internet connectivity
- Verify Microsoft Learn MCP endpoint: `https://learn.microsoft.com/api/mcp`
- Try without MCP (see "Disabling MCP" section above)

## 📚 Additional Resources

- **Microsoft Agent Framework Docs**: [Official Documentation](https://learn.microsoft.com/agent-framework)
- **MCP Specification**: [Model Context Protocol](https://modelcontextprotocol.io/)
- **Azure Well-Architected Framework**: [Learn More](https://learn.microsoft.com/azure/well-architected/)
- **Mermaid Diagram Syntax**: [Mermaid Documentation](https://mermaid.js.org/)

## 🤝 Contributing

This is a conference demo project. Feel free to fork and adapt for your own presentations!

## 📄 License

[Your License Here]

---

<div align="center">

**🎤 See you at AgentCon Zürich!**

**Workshop: Wednesday 1:30 pm - 3:00 pm**

</div>

# Optional: Use image mode
USE_IMAGE_MODE=false
ARCHITECTURE_IMAGE_PATH=

# Alternative: Azure OpenAI (if not using OpenAI)
# AZURE_OPENAI_API_KEY=your-azure-key-here
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
# AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

**Note**: The `.env` file is already configured. Just ensure your `OPENAI_API_KEY` is valid.

### 3. Run the Demo (Text Mode)

Default mode analyzes a text-based architecture description:

```powershell
python agentcon_demo.py
```

**Expected Output**:
```
🔌 Connecting to Microsoft Learn MCP...
📝 Text mode (default)

============================================================
🎯 INPUT ARCHITECTURE
============================================================
We have a 3-tier e-commerce application on Azure:
- Frontend: Virtual Machines running Node.js (public IPs)
- Backend: Virtual Machines running .NET APIs (public IPs)
...

============================================================
🔍 STEP 1: Architecture Critic (MCP-grounded)
============================================================
According to Microsoft Learn, exposing VMs with public IPs is a security risk...
...

============================================================
✅ PIPELINE COMPLETE
============================================================
```

## 🖼️ Image Mode: Analyzing Architecture Diagrams

### Why Use Image Mode?

> **"Architects don't start with JSON. They start with whiteboards, screenshots, and PowerPoint diagrams."**

Image mode is the **"wow" moment** for live demos — upload a real architecture diagram and watch the agents interpret, critique, and improve it.

### Supported Image Formats

- **PNG, JPG, JPEG** (recommended)
- **URLs** (public images)
- **Local files** (from your computer)

### How to Prepare Architecture Diagrams

1. **Create or find an Azure architecture diagram**:
   - Export from Visio, draw.io, PowerPoint, or Lucidchart
   - Screenshot from Azure Portal's "Architecture Center"
   - Use existing whiteboards or hand-drawn sketches

2. **Recommended content**:
   - Clear service icons or labels (e.g., "VM", "SQL Database", "App Service")
   - Connection lines showing data flow
   - Public vs private components labeled
   - Resource names or types visible

3. **Example sources**:
   - [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
   - Your organization's existing diagrams
   - Conference slide decks

### Running with Image Input

#### Option 1: Using Environment Variables

```powershell
# Edit .env file
USE_IMAGE_MODE=true
ARCHITECTURE_IMAGE_PATH=path/to/your/diagram.png
# OR
ARCHITECTURE_IMAGE_PATH=https://example.com/azure-architecture.png

# Run
python agentcon_demo.py
```

#### Option 2: Programmatic (Modify `main()`)

For live demos, you can hardcode the image path:

```python
# In agentcon_demo.py, update main():

async def main():
    # ... (keep existing setup)
    
    # Use a specific image
    from agent_framework import ImageContent
    diagram_image = ImageContent(url="https://your-image-url.png")
    # OR for local files:
    # diagram_image = ImageContent.from_file("diagrams/my-architecture.png")
    
    await run_sequential_workflow(factory, diagram_image, is_image=True)
```

### Example: Using a Sample Diagram

```powershell
# 1. Download a sample Azure architecture diagram
# Example: https://learn.microsoft.com/azure/architecture/reference-architectures/n-tier/images/n-tier-sql-server.png

# 2. Save it locally as "sample_arch.png"

# 3. Update .env
USE_IMAGE_MODE=true
ARCHITECTURE_IMAGE_PATH=sample_arch.png

# 4. Run
python agentcon_demo.py
```

**Expected Output**:
```
🔌 Connecting to Microsoft Learn MCP...
📸 Image mode enabled

============================================================
🖼️  STEP 0: Diagram Interpreter (image → text)
============================================================
The diagram shows a 3-tier web application with:
- Frontend: Application Gateway routing to VMs
- Backend: Multiple VMs in an availability set
- Database: Azure SQL Database with public endpoint
...

============================================================
🔍 STEP 1: Architecture Critic (MCP-grounded)
============================================================
According to Microsoft Learn, the diagram has several issues:
• Public endpoints on SQL Database violate the principle of least privilege
• VMs should be replaced with Azure App Service for better scalability
...
```

## 📋 Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | Model to use (gpt-4o, gpt-4o-mini, etc.) |
| `USE_IMAGE_MODE` | No | `false` | Enable image input mode |
| `ARCHITECTURE_IMAGE_PATH` | No | - | Path/URL to architecture diagram |

### Supported Models

**Recommended**:
- `gpt-4o` - Best quality, supports vision
- `gpt-4o-mini` - Cost-effective, supports vision

**Not Recommended**:
- `o1-mini`, `o1-preview` - Reasoning models that buffer tokens (no streaming)

### MCP Endpoint

The demo uses Microsoft Learn MCP:
```
https://learn.microsoft.com/api/mcp
```

**Available MCP Tools**:
- `microsoft_docs_search` - Search Azure documentation
- `microsoft_docs_fetch` - Retrieve specific documentation pages
- `microsoft_code_sample_search` - Find code examples

## 🎤 Conference Presentation Tips

### Slide 1: The Problem
*"Traditional AI hallucinates. It invents Azure resource types, suggests deprecated APIs, and confidently proposes architectures that don't work."*

### Slide 2: The Solution
*"Microsoft Agent Framework with MCP grounds every decision in real documentation."*

### Slide 3: Live Demo
1. Show text mode first (safe, predictable)
2. Then switch to image mode for "wow" moment
3. Point out citations: *"According to Microsoft Learn..."*

### Key Talking Points

✅ **"This isn't hallucinating — it checked Microsoft Learn."**
- Agents cite sources in their output

✅ **"Architects don't start with JSON."**
- Show image upload capability

✅ **"Every resource type is validated."**
- Point to IaC step checking API versions

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'agent_framework'`

**Solution**:
```powershell
pip install agent-framework --pre
```

### Issue: `OpenAI API Error: Incorrect API key`

**Solution**: Check your `.env` file has valid `OPENAI_API_KEY`

### Issue: MCP Connection Timeout

**Solution**: Ensure internet connection. MCP endpoint requires HTTPS.

### Issue: Image Not Recognized

**Causes**:
- Model doesn't support vision (use `gpt-4o` or `gpt-4o-mini`)
- Image file corrupted or unsupported format
- Image URL not publicly accessible

**Solution**:
```bash
# Verify model in .env supports vision
OPENAI_MODEL=gpt-4o

# Test image URL is accessible
curl -I https://your-image-url.png
```

## 📊 Code Structure

```
agentcon_demo.py (172 lines)
├── Imports & Environment Loading
├── last_text() - Safe message extraction
├── AgentRole (Enum) - 5 agent types
├── AgentFactory
│   ├── __init__() - MCP tool + OpenAI client
│   └── create_agent() - Role-specific prompts
├── run_sequential_workflow()
│   ├── Step 0: Diagram Interpreter (optional)
│   ├── Step 1: Critic (MCP)
│   ├── Step 2: Fixer (MCP)
│   ├── Step 3: Visualizer
│   └── Step 4: IaC Generator (MCP)
└── main()
    ├── Load environment
    ├── Initialize MCP
    ├── Create factory
    └── Run workflow (text or image mode)
```

## 🔧 Advanced Usage

### Custom Architecture Input

Edit the `demo_architecture` variable in `main()`:

```python
demo_architecture = """
Your custom architecture description here:
- Service 1: ...
- Service 2: ...
- Connections: ...
"""
```

### Using Azure OpenAI Instead of OpenAI

Update `.env`:
```bash
# Comment out OpenAI config
# OPENAI_API_KEY=...

# Enable Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

Update `agentcon_demo.py`:
```python
from agent_framework.azure import AzureOpenAIChatClient

# In AgentFactory.__init__():
self.chat_client = AzureOpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
)
```

### Extending Agents

Add a new agent by:

1. Adding to `AgentRole` enum
2. Adding prompt to `AgentFactory.create_agent()`
3. Adding step to `run_sequential_workflow()`

Example:
```python
class AgentRole(Enum):
    # ... existing agents
    COST_ESTIMATOR = "cost_estimator"

# In create_agent():
prompts = {
    # ... existing prompts
    AgentRole.COST_ESTIMATOR: """Estimate monthly Azure costs..."""
}

# In workflow:
cost_estimator = factory.create_agent(AgentRole.COST_ESTIMATOR)
cost_response = await cost_estimator.run(improved)
```

## 📚 Additional Resources

- [Microsoft Agent Framework Docs](https://github.com/microsoft/agent-framework)
- [Model Context Protocol (MCP)](https://spec.modelcontextprotocol.io/)
- [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)

## 🤝 Contributing

This is a conference demo. For production use:
- Add error handling and retries
- Implement proper logging
- Add unit tests
- Consider streaming for better UX
- Add deployment pipelines
- Integrate Terraform MCP for multi-cloud

## 📄 License

MIT License - See `LICENSE` file

## ✨ Credits

Built for **AgentCon Zürich** by **Igor Iric**

**Technologies:**
- **Microsoft Agent Framework** - Multi-agent orchestration
- **Model Context Protocol (MCP)** - Real-time documentation grounding
- **Microsoft Learn API** - Official Azure documentation
- **OpenAI** - Language models with vision capabilities

**Special Thanks:**
- Microsoft Agent Framework Team
- Azure Architecture Center
- AgentCon Zürich organizers

---

<div align="center">

**🎤 Ready for the stage?**

Run `python agentcon_demo.py` and show the world what grounded AI can do! 🚀

**Workshop: Wednesday 1:30 pm - 3:00 pm**
![Global AI Zürich](global-ai-zurich_495_sticker.png)
**AgentCon Zürich**

</div>
