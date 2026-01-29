# Quick Start Guide

## 30-Second Setup

```powershell
# 1. Install dependencies
pip install agent-framework --pre python-dotenv

# 2. Set your OpenAI API key in .env file
# (Already configured - just verify OPENAI_API_KEY is valid)

# 3. Run the demo
python agentcon_demo.py
```

## 5-Minute Image Demo

```powershell
# 1. Download a sample architecture diagram
# Visit: https://learn.microsoft.com/azure/architecture/browse/

# 2. Save the image as "my_architecture.png"

# 3. Update .env:
USE_IMAGE_MODE=true
ARCHITECTURE_IMAGE_PATH=my_architecture.png

# 4. Run
python agentcon_demo.py
```

## What You'll See

### Text Mode Output (Default)
```
🔌 Connecting to Microsoft Learn MCP...
📝 Text mode (default)
============================================================
🎯 INPUT ARCHITECTURE
============================================================
[Your text description]

🔍 STEP 1: Architecture Critic
[AI identifies issues, cites Microsoft Learn]

🔧 STEP 2: Architecture Fixer  
[AI proposes improvements with documentation links]

📊 STEP 3: Diagram Visualizer
[JSON representation]

📝 STEP 4: IaC Generator
[Bicep code with validated resource types]

✅ PIPELINE COMPLETE
```

### Image Mode Output
```
🔌 Connecting to Microsoft Learn MCP...
📸 Image mode enabled
============================================================
🖼️ STEP 0: Diagram Interpreter
============================================================
[AI describes what it sees in the diagram]

[... then same as text mode]
```

## Common Issues

**"No module named 'agent_framework'"**
```powershell
pip install agent-framework --pre
```

**"OpenAI API Error"**
- Check `.env` file has valid `OPENAI_API_KEY`
- Verify internet connection

**Image not recognized**
- Use `gpt-4o` or `gpt-4o-mini` model (supports vision)
- Ensure image file exists and is readable
- Try a simpler diagram with clear labels

## Next Steps

- Read [README.md](README.md) for full documentation
- Try different architecture diagrams
- Customize agent prompts in `agentcon_demo.py`
- Present at AgentCon! 🎤
