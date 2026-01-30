"""Step 4: MCP Grounding - Agents with Microsoft Learn knowledge"""
import asyncio, os
from enum import Enum
from dotenv import load_dotenv
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    return response.text if hasattr(response, 'text') and response.text else ""

class AgentRole(Enum):
    CRITIC = "architecture_critic"
    FIXER = "architecture_fixer"

class AgentFactory:
    """Factory with MCP tool for grounded agents"""
    
    def __init__(self, chat_client: OpenAIChatClient, mcp_tool: MCPStreamableHTTPTool):
        self.chat_client = chat_client
        self.mcp_tool = mcp_tool
        
        self.prompts = {
            AgentRole.CRITIC: """You are an Azure Architecture Critic.
Review for: security issues, wrong service choices, missing best practices.
**Use the Microsoft Learn MCP tool** to cite official Azure documentation.
Keep brief with bullet points and cite sources.""",
            
            AgentRole.FIXER: """You are an Azure Architecture Fixer.
Improve the architecture by:
- Applying Azure Well-Architected Framework
- Using managed services over IaaS
- Implementing secure-by-default networking
**Use the Microsoft Learn MCP tool** to reference official guidance.
Output: improved architecture with documentation links."""
        }
    
    def create_agent(self, role: AgentRole) -> ChatAgent:
        """Create agent with MCP tool for knowledge grounding"""
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],
            name=role.value,
            tools=[self.mcp_tool]  # All agents can access Microsoft Learn
        )

async def main():
    """Sequential pipeline with MCP-grounded agents"""
    
    chat_client = OpenAIChatClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    
    # Initialize MCP connection to Microsoft Learn
    print("🔌 Connecting to Microsoft Learn MCP...")
    
    async with MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000"
    ) as mcp_tool:
        print("✅ MCP connected!\n")
        
        factory = AgentFactory(chat_client, mcp_tool)
        
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
        
        # Step 1: Critic with MCP grounding
        print("\n" + "="*60)
        print("🔍 STEP 1: Architecture Critic (MCP-Grounded)")
        print("="*60)
        critic = factory.create_agent(AgentRole.CRITIC)
        critique_response = await critic.run(architecture)
        critique = get_text(critique_response)
        print(critique)
        
        # Step 2: Fixer with MCP grounding
        print("\n" + "="*60)
        print("🔧 STEP 2: Architecture Fixer (MCP-Grounded)")
        print("="*60)
        fixer = factory.create_agent(AgentRole.FIXER)
        fixer_input = f"Original:\n{architecture}\n\nCritique:\n{critique}"
        fixer_response = await fixer.run(fixer_input)
        improved = get_text(fixer_response)
        print(improved)
        
        print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    asyncio.run(main())
