"""Step 1: Single Agent Critic - Build the simplest working unit"""
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

async def main():
    """Single agent that critiques Azure architecture"""
    
    # Initialize OpenAI client
    chat_client = OpenAIChatClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    
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
