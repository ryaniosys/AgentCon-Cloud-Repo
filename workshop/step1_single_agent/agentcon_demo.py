"""Step 1: Single Agent Critic - Build the simplest working unit"""
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def create_chat_client():
    """Create chat client from configured provider (Azure OpenAI, OpenAI, Ollama, or Foundry Local)"""
    use_azure_openai = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"

    if use_azure_openai:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        print(f"🤖 Using Azure OpenAI deployment: {deployment}")
        azure_client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        return OpenAIChatClient(
            model_id=deployment,
            async_client=azure_client
        )
    elif use_openai:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🤖 Using OpenAI model: {model}")
        return OpenAIChatClient(api_key=api_key, model_id=model)
    elif use_ollama:
        model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        print(f"🤖 Using Ollama model: {model}")
        return OpenAIChatClient(api_key="dummy", model_id=model, base_url=base_url)
    else:
        model = os.getenv("LOCAL_MODEL", "gpt-oss-20b-generic-cpu:1")
        base_url = os.getenv("LOCAL_BASE_URL", "http://localhost:56238/v1")
        print(f"🤖 Using Foundry Local model: {model}")
        return OpenAIChatClient(api_key="dummy", model_id=model, base_url=base_url)

async def main():
    """Single agent that critiques Azure architecture"""
    
    # Initialize chat client (auto-detects provider from env vars)
    chat_client = create_chat_client()
    
    # Create a Critic agent
    critic = ChatAgent(
        chat_client=chat_client,
        instructions="""You are an Azure Architecture Critic. 
Review the architecture for:
- Security issues
- Wrong service choices
- Missing best practices
Keep your critique brief with bullet points.""",
        name="architecture_critic"
    )
    
    # Input architecture (flawed on purpose)
    architecture = """
    We have a 3-tier e-commerce application on Azure:
    - Frontend: Virtual Machines running Node.js (public IPs)
    - Backend: Virtual Machines running .NET APIs (public IPs)
    - Database: Azure SQL Database (public endpoint enabled)
    - Storage: Azure Storage Account (no encryption at rest)
    """
    
    print("="*60)
    print("🎯 INPUT ARCHITECTURE")
    print("="*60)
    print(architecture)
    
    # Run the critic
    print("\n" + "="*60)
    print("🔍 ARCHITECTURE CRITIQUE")
    print("="*60)
    response = await critic.run(architecture)
    print(response.text)
    
    print("\n✅ Single agent complete!")

if __name__ == "__main__":
    asyncio.run(main())
