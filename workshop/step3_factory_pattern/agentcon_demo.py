"""Step 3: Factory Pattern - Centralized agent creation"""
import asyncio, os
from enum import Enum
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    return response.text if hasattr(response, 'text') and response.text else ""

class AgentRole(Enum):
    CRITIC = "architecture_critic"
    FIXER = "architecture_fixer"

class AgentFactory:
    """Factory pattern: centralized agent creation with shared config"""
    
    def __init__(self, chat_client: OpenAIChatClient):
        self.chat_client = chat_client
        
        # All agent prompts in one place
        self.prompts = {
            AgentRole.CRITIC: """You are an Azure Architecture Critic. 
Review for: security issues, wrong service choices, missing best practices.
Keep brief with bullet points.""",
            
            AgentRole.FIXER: """You are an Azure Architecture Fixer.
Improve the architecture by:
- Applying Azure Well-Architected Framework
- Using managed services over IaaS
- Implementing secure-by-default networking
Output: improved architecture description."""
        }
    
    def create_agent(self, role: AgentRole) -> ChatAgent:
        """Create an agent by role - no duplication"""
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],
            name=role.value
        )

async def main():
    """Sequential pipeline with factory pattern"""
    
    chat_client = OpenAIChatClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    
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
    critic = factory.create_agent(AgentRole.CRITIC)
    critique_response = await critic.run(architecture)
    critique = get_text(critique_response)
    print(critique)
    
    # Step 2: Fixer
    print("\n" + "="*60)
    print("🔧 STEP 2: Architecture Fixer")
    print("="*60)
    fixer = factory.create_agent(AgentRole.FIXER)
    fixer_input = f"Original:\n{architecture}\n\nCritique:\n{critique}"
    fixer_response = await fixer.run(fixer_input)
    improved = get_text(fixer_response)
    print(improved)
    
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    asyncio.run(main())
