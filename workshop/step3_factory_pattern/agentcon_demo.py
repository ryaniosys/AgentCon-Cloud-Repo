"""Step 3: Factory Pattern - Centralized agent creation"""
import asyncio, os
from enum import Enum
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    return response.text if hasattr(response, 'text') and response.text else ""

class AgentFactory:
    """Factory pattern: centralized agent creation with multi-provider support"""

    def __init__(self, chat_client: OpenAIChatClient):
        self.chat_client = chat_client

        # Track model capabilities (Azure OpenAI and OpenAI support copilot messages)
        self.model_supports_copilot_messages = (
            os.getenv("USE_AZURE_OPENAI", "false").lower() == "true" or
            os.getenv("USE_OPENAI", "false").lower() == "true"
        )

        # All agent prompts in one place
        self.prompts = {
            "critic": """You are an Azure Architecture Critic.
Review for: security issues, wrong service choices, missing best practices.
Keep brief with bullet points.""",

            "fixer": """You are an Azure Architecture Fixer.
Improve the architecture by:
- Applying Azure Well-Architected Framework
- Using managed services over IaaS
- Implementing secure-by-default networking
Output: improved architecture description."""
        }

    def create_agent(self, role: str) -> ChatAgent:
        """Create an agent by role - no duplication"""
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],
            name=role,
            model_supports_copilot_messages=self.model_supports_copilot_messages
        )

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
    """Sequential pipeline with factory pattern"""
    
    chat_client = create_chat_client()
    
    # Factory creates all agents
    factory = AgentFactory(chat_client)
    
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
    
    # Step 1: Critic
    print("\n" + "="*60)
    print("🔍 STEP 1: Architecture Critic")
    print("="*60)
    critic = factory.create_agent("critic")
    critique_response = await critic.run(architecture)
    critique = get_text(critique_response)
    print(critique)
    
    # Step 2: Fixer
    print("\n" + "="*60)
    print("🔧 STEP 2: Architecture Fixer")
    print("="*60)
    fixer = factory.create_agent("fixer")
    fixer_input = f"Original:\n{architecture}\n\nCritique:\n{critique}"
    fixer_response = await fixer.run(fixer_input)
    improved = get_text(fixer_response)
    print(improved)
    
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    asyncio.run(main())
