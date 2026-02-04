# Step 1: Single Agent Critic

**Duration:** 10-15 minutes
**Goal:** Build the simplest working agent and prove the framework works

## What You'll Learn

- How to create an `OpenAIChatClient`
- How to create a `ChatAgent` with instructions
- How to run an agent with `.run()`
- What an agent response looks like
- How to detect model provider (Azure OpenAI, OpenAI, Ollama, Foundry)

## Prerequisites

### 1. Create Virtual Environment

From the repository root:

```bash
cd /path/to/AgentCon-Cloud-Repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and configure your provider:

```bash
cp .env.example .env
```

Edit `.env` with your preferred provider. For Azure OpenAI:

```env
USE_AZURE_OPENAI=true
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Note:** The endpoint should be just the base URL, not the full path.

## 📖 Detailed Learning

For a comprehensive walkthrough of this step including:
- Installation and setup
- Understanding async/await
- Explanation of each code line and "why"
- How providers work

👉 See the **[TUTORIAL.md](../../TUTORIAL.md#part-1-single-agent--architecture-critic)** file!

It covers Step 1 in detail with full explanations.

## Key Concepts

> **"An Agent is a specialized LLM with instructions and optional tools."**

This is the smallest working unit in the Microsoft Agent Framework. We start with one role: **Critic**.

## Run This Step

From the repository root (with venv activated):

```bash
source .venv/bin/activate
cd workshop/step1_single_agent
python agentcon_demo.py
```

Or as a one-liner:

```bash
source .venv/bin/activate && python workshop/step1_single_agent/agentcon_demo.py
```

## Expected Output

You should see:
1. ✅ The input architecture (deliberately flawed)
2. ✅ A critique with bullet points identifying problems

## What's Happening

1. **Client Creation** - `OpenAIChatClient` connects to OpenAI API
2. **Agent Creation** - `ChatAgent` wraps the client with role-specific instructions
3. **Execution** - `.run()` sends the message and gets a response
4. **Result** - `response.text` contains the agent's output

## Next Step

➡️ **Step 2**: Add a second agent (Fixer) to create a sequential pipeline
