"""Step 2: Two Agents (Critic → Fixer) - Sequential pipeline"""
import asyncio
import os
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    """Extract text from agent response"""
    return response.text if hasattr(response, 'text') and response.text else ""

async def main():
    """Sequential pipeline: Critic finds problems, Fixer solves them"""
    
    # Initialize OpenAI client
    chat_client = OpenAIChatClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    
    # Input architecture
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
    
    # Agent 1: Critic
    critic = ChatAgent(
        chat_client=chat_client,
        instructions="""You are an Azure Architecture Critic. 
Review for: security issues, wrong service choices, missing best practices.
Keep brief with bullet points.""",
        name="critic"
    )
    
    print("\n" + "="*60)
    print("🔍 STEP 1: Architecture Critic")
    print("="*60)
    critique_response = await critic.run(architecture)
    critique = get_text(critique_response)
    print(critique)
    
    # Agent 2: Fixer
    fixer = ChatAgent(
        chat_client=chat_client,
        instructions="""You are an Azure Architecture Fixer.
Improve the architecture by:
- Applying Azure Well-Architected Framework
- Using managed services over IaaS
- Implementing secure-by-default networking
Output: improved architecture description.""",
        name="fixer"
    )
    
    print("\n" + "="*60)
    print("🔧 STEP 2: Architecture Fixer")
    print("="*60)
    fixer_input = f"Original:\n{architecture}\n\nCritique:\n{critique}"
    fixer_response = await fixer.run(fixer_input)
    improved = get_text(fixer_response)
    print(improved)
    
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    asyncio.run(main())
