"""Step 5: Visualizer Agent - Generate Mermaid diagrams"""
import asyncio, os
from enum import Enum
from dotenv import load_dotenv
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    return response.text if hasattr(response, 'text') and response.text else ""

class AgentFactory:
    """Factory with role-based tool assignment"""
    
    def __init__(self, chat_client: OpenAIChatClient, mcp_tool: MCPStreamableHTTPTool):
        self.chat_client = chat_client
        self.mcp_tool = mcp_tool
        self.model_supports_copilot_messages = os.getenv("USE_OPENAI", "false").lower() == "true"
        
        self.prompts = {
            "critic": """You are an Azure Architecture Critic.
Review for: security issues, wrong service choices, missing best practices.
**Use the Microsoft Learn MCP tool** to cite official Azure documentation.
Keep brief with bullet points and cite sources.""",
            
            "fixer": """You are an Azure Architecture Fixer.
Improve the architecture by:
- Applying Azure Well-Architected Framework
- Using managed services over IaaS
- Implementing secure-by-default networking
**Use the Microsoft Learn MCP tool** to reference official guidance.
Output: improved architecture with documentation links.""",
            
            "visualizer": """You are a Mermaid Diagram Generator.
Generate a **valid Mermaid syntax** diagram of the Azure architecture.
Use Mermaid graph notation with Azure service icons.
Example:
```mermaid
graph TD
    A[Azure App Service] -->|HTTPS| B[Azure SQL Database]
    B -->|Private Endpoint| C[Virtual Network]
```
Output ONLY valid Mermaid code wrapped in ```mermaid blocks."""
        }
    
    def create_agent(self, role: str) -> ChatAgent:
        """Create agent with role-specific tool configuration"""
        # Visualizer doesn't need MCP (generates diagrams, no research)
        tools = [self.mcp_tool] if role != "visualizer" else []
        
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=self.prompts[role],
            name=role,
            tools=tools,
            model_supports_copilot_messages=self.model_supports_copilot_messages
        )

def create_chat_client():
    """Create chat client from configured provider (OpenAI, Ollama, or Foundry Local)"""
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"
    
    if use_openai:
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
    """Pipeline with visualization step"""
    
    chat_client = create_chat_client()
    
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
        
        # Step 3: Visualizer
        print("\n" + "="*60)
        print("📊 STEP 3: Diagram Visualizer")
        print("="*60)
        visualizer = factory.create_agent("visualizer")
        diagram_response = await visualizer.run(improved)
        diagram = get_text(diagram_response)
        print(diagram)
        
        print("\n✅ Pipeline complete!")
        print("\n💡 Tip: Copy the Mermaid code and paste into:")
        print("   - https://mermaid.live")
        print("   - VS Code Markdown preview (install Mermaid extension)")

if __name__ == "__main__":
    asyncio.run(main())
