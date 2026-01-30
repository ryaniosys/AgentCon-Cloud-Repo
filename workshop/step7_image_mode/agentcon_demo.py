"""Step 7: Image Mode - Analyze architecture diagrams (photo/whiteboard)"""
import asyncio, os
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from agent_framework import ChatAgent, MCPStreamableHTTPTool, UriContent, DataContent, ChatMessage
from agent_framework.openai import OpenAIChatClient

load_dotenv()

def get_text(response):
    return response.text if hasattr(response, 'text') and response.text else ""

class AgentFactory:
    """Factory with image interpretation support"""
    
    def __init__(self, chat_client: OpenAIChatClient, mcp_tool: MCPStreamableHTTPTool):
        self.chat_client = chat_client
        self.mcp_tool = mcp_tool
        self.model_supports_copilot_messages = os.getenv("USE_OPENAI", "false").lower() == "true"
        
        self.prompts = {
            "diagram_interpreter": """You are an Architecture Diagram Interpreter.
Extract a **detailed text description** of the Azure architecture from the image.
Identify:
- Azure services shown (VMs, databases, networks, etc.)
- Connections and data flow
- Security configurations (public vs private)
- Any annotations or notes
Output: Clear text description of the architecture.""",
            
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
Output ONLY valid Mermaid code wrapped in ```mermaid blocks.""",
            
            "iac_generator": """You are a Bicep IaC Generator.
Generate **Azure Bicep code** to deploy the improved architecture.
Include: Resource definitions, secure configurations, parameters.
**Use Microsoft Learn MCP tool** for Bicep best practices.
Output: Production-ready Bicep code with comments."""
        }
    
    def create_agent(self, role: str) -> ChatAgent:
        """Create agent with role-specific tool configuration"""
        # Visualizer and Diagram Interpreter don't need MCP
        tools = [self.mcp_tool] if role not in ["visualizer", "diagram_interpreter"] else []
        
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

async def run_image_mode(factory: AgentFactory, image_path: str):
    """Process architecture from image file"""
    
    # Step 0: Interpret diagram image → text description
    print("="*60)
    print("📸 STEP 0: Diagram Interpreter (Image → Text)")
    print("="*60)
    interpreter = factory.create_agent("diagram_interpreter")
    
    # Handle both local files and URLs
    if image_path.startswith(("http://", "https://")):
        # Remote image - use UriContent
        image_content = UriContent(uri=image_path, media_type="image/png")
    else:
        # Local file - read and encode as DataContent
        with open(image_path, "rb") as f:
            image_data = f.read()
        image_content = DataContent(data=image_data, media_type="image/png")
    
    # Wrap image content in a ChatMessage and pass to agent
    message = ChatMessage(role="user", contents=[image_content])
    response = await interpreter.run(message)
    architecture_text = get_text(response)
    print(architecture_text)
    
    return architecture_text

async def run_text_pipeline(factory: AgentFactory, architecture: str, skip_input_display: bool = False):
    """Run the full 4-step pipeline on text architecture"""
    
    # Only display input architecture if not already shown (e.g., not from image mode)
    if not skip_input_display:
        print("\n" + "="*60)
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
    
    # Step 4: IaC Generator
    print("\n" + "="*60)
    print("📝 STEP 4: Bicep IaC Generator")
    print("="*60)
    iac_generator = factory.create_agent("iac_generator")
    iac_response = await iac_generator.run(improved)
    bicep_code = get_text(iac_response)
    print(bicep_code)

async def main():
    """Image mode: photo/whiteboard → architecture pipeline"""
    
    chat_client = create_chat_client()
    
    print("🔌 Connecting to Microsoft Learn MCP...")
    
    async with MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000"
    ) as mcp_tool:
        print("✅ MCP connected!\n")
        
        factory = AgentFactory(chat_client, mcp_tool)
        
        # Check for image input
        image_path = os.getenv("ARCHITECTURE_IMAGE_PATH")
        
        if image_path and Path(image_path).exists():
            # IMAGE MODE: Process photo/whiteboard
            print("🖼️  IMAGE MODE: Processing architecture diagram...\n")
            architecture_text = await run_image_mode(factory, image_path)
            await run_text_pipeline(factory, architecture_text, skip_input_display=True)
        else:
            # TEXT MODE: Use hardcoded example
            print("📝 TEXT MODE: Using example architecture\n")
            architecture = """
    We have a 3-tier e-commerce application on Azure:
    - Frontend: Virtual Machines running Node.js (public IPs)
    - Backend: Virtual Machines running .NET APIs (public IPs)
    - Database: Azure SQL Database (public endpoint enabled)
    - Storage: Azure Storage Account (no encryption at rest)
            """
            await run_text_pipeline(factory, architecture)
        
        print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    asyncio.run(main())
