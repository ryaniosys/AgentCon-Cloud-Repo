"""
AgentCon Zürich Demo: Agentic AI with Microsoft Learn MCP
==========================================================
Demonstrates: Agent Factory + Microsoft Learn MCP grounding for Azure architecture
"""
import asyncio
import os
import json
from enum import Enum
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from agent_framework import ChatAgent, ChatMessage, MCPStreamableHTTPTool, DataContent, UriContent
from agent_framework.openai import OpenAIChatClient

# Load environment variables
load_dotenv()


def last_text(response):
    """Safely extract assistant message text from AgentResponse"""
    # New API: AgentResponse has a .text property
    if hasattr(response, 'text') and response.text:
        return response.text
    # Fallback: empty string if no text
    return ""


def save_response_to_file(step_name: str, content: str, output_dir: str = "output"):
    """Save agent response to a text file"""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{step_name}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 Saved to: {filename}")
    return filename


class AgentRole(Enum):
    """Agent roles in the architecture pipeline"""
    DIAGRAM_INTERPRETER = "diagram_interpreter"
    CRITIC = "critic"
    FIXER = "fixer"
    VISUALIZER = "visualizer"
    IAC_GENERATOR = "iac_generator"


class AgentFactory:
    """Centralized factory for creating MCP-grounded agents"""
    
    def __init__(self, mcp_tool):
        self.mcp_tool = mcp_tool
        # Initialize with API key and model from environment
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        print(f"🤖 Using model: {model}")
        self.chat_client = OpenAIChatClient(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_id=model
        )
    
    def create_agent(self, role: AgentRole) -> ChatAgent:
        """Create agent with role-specific prompt and tools"""
        prompts = {
            AgentRole.DIAGRAM_INTERPRETER: """Convert diagram to text. List: services, connections, access (public/private). Azure assumed. Be concise.""",
            
            AgentRole.CRITIC: """Critique Azure architecture: security issues, wrong services, missing best practices. Use Microsoft Learn MCP. Keep brief with bullets.""",
            
            AgentRole.FIXER: """Fix architecture: apply Well-Architected, use managed services, secure networking. Use Microsoft Learn MCP. Output improved text.""",
            
            AgentRole.VISUALIZER: """Generate a Mermaid diagram in flowchart syntax showing the Azure architecture. Use this format:
```mermaid
graph TB
    A[Service Name] --> B[Another Service]
    B --> C[Database]
```
Use proper Azure service names. Include all components and connections.""",
            
            AgentRole.IAC_GENERATOR: """Generate Bicep snippet. Use Microsoft Learn MCP to verify types/versions. Keep short."""
        }
        
        tools = [self.mcp_tool] if role != AgentRole.VISUALIZER else []
        
        return ChatAgent(
            chat_client=self.chat_client,
            instructions=prompts[role],
            name=role.value,
            tools=tools
        )


async def run_sequential_workflow(factory: AgentFactory, input_data, is_image: bool = False):
    """Execute the pipeline sequentially (with optional image interpretation)"""
    
    # Optional Step 0: Diagram Interpreter (for image inputs)
    if is_image:
        print(f"\n{'='*60}")
        print("🖼️  STEP 0: Diagram Interpreter (image → text)")
        print(f"{'='*60}")
        interpreter = factory.create_agent(AgentRole.DIAGRAM_INTERPRETER)
        interpreter_response = await interpreter.run(input_data)
        architecture_text = last_text(interpreter_response)
        print(architecture_text)
    else:
        architecture_text = input_data
        print(f"\n{'='*60}")
        print("🎯 INPUT ARCHITECTURE")
        print(f"{'='*60}")
        print(architecture_text)
    
    # Step 1: Critic (with MCP) - STREAMING
    print(f"\n{'='*60}")
    print("🔍 STEP 1: Architecture Critic (MCP-grounded)")
    print(f"{'='*60}")
    critic = factory.create_agent(AgentRole.CRITIC)
    
    # Use streaming to show live reasoning
    critique_parts = []
    async for chunk in critic.run_stream(architecture_text):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            critique_parts.append(chunk.text)
    
    critique = ''.join(critique_parts)
    print()  # New line after streaming
    save_response_to_file("step1_critic", critique)
    
    # Step 2: Fixer (with MCP) - STREAMING
    print(f"\n{'='*60}")
    print("🔧 STEP 2: Architecture Fixer (MCP-grounded)")
    print(f"{'='*60}")
    fixer = factory.create_agent(AgentRole.FIXER)
    
    fixer_parts = []
    async for chunk in fixer.run_stream(f"Original:\n{architecture_text}\n\nCritique:\n{critique}"):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            fixer_parts.append(chunk.text)
    
    improved = ''.join(fixer_parts)
    print()  # New line after streaming
    save_response_to_file("step2_fixer", improved)
    
    # Step 3: Visualizer (Mermaid diagram)
    print(f"\n{'='*60}")
    print("📊 STEP 3: Diagram Visualizer (Mermaid)")
    print(f"{'='*60}")
    visualizer = factory.create_agent(AgentRole.VISUALIZER)
    diagram_response = await visualizer.run(improved)
    diagram = last_text(diagram_response)
    print(diagram)
    save_response_to_file("step3_mermaid_diagram", diagram)
    
    # Step 4: IaC Generator (with MCP) - STREAMING
    print(f"\n{'='*60}")
    print("📝 STEP 4: IaC Generator (MCP-grounded)")
    print(f"{'='*60}")
    iac_generator = factory.create_agent(AgentRole.IAC_GENERATOR)
    
    bicep_parts = []
    async for chunk in iac_generator.run_stream(improved):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            bicep_parts.append(chunk.text)
    
    bicep = ''.join(bicep_parts)
    print()  # New line after streaming
    save_response_to_file("step4_bicep", bicep)
    
    print(f"\n{'='*60}")
    print("✅ PIPELINE COMPLETE")
    print(f"{'='*60}")


async def main():
    """Main demo entry point"""
    
    # Initialize Microsoft Learn MCP (single source of truth)
    print("🔌 Connecting to Microsoft Learn MCP...")
    
    # Use async context manager for proper cleanup
    # Added maxTokenBudget=3000 to limit token usage per Microsoft Learn MCP docs
    async with MCPStreamableHTTPTool(
        name="microsoft_learn",
        url="https://learn.microsoft.com/api/mcp?maxTokenBudget=3000"
    ) as mcp_tool:
        # Create agent factory
        factory = AgentFactory(mcp_tool)
        
        # Demo Mode 1: Text input (default)
        demo_architecture = """
    We have a 3-tier e-commerce application on Azure:
    - Frontend: Virtual Machines running Node.js (public IPs)
    - Backend: Virtual Machines running .NET APIs (public IPs)
    - Database: Azure SQL Database (public endpoint enabled)
    - Storage: Azure Storage Account (no encryption at rest)
    """
        
        # Check if we should use image mode
        use_image_mode = os.getenv("USE_IMAGE_MODE", "false").lower() == "true"
        image_path = os.getenv("ARCHITECTURE_IMAGE_PATH", "")
        
        if use_image_mode and image_path:
            print("📸 Image mode enabled")
            # Support both local files and URLs
            if image_path.startswith(("http://", "https://")):
                diagram_image = UriContent(uri=image_path, media_type="image/png")
            else:
                # Local file - read and encode
                with open(image_path, "rb") as f:
                    image_data = f.read()
                diagram_image = DataContent(data=image_data, media_type="image/png")
            await run_sequential_workflow(factory, diagram_image, is_image=True)
        else:
            print("📝 Text mode (default)")
            await run_sequential_workflow(factory, demo_architecture, is_image=False)
    
    # Production note (comment only)
    # Production version integrates: Terraform MCP, compliance agents, deployment pipelines


if __name__ == "__main__":
    asyncio.run(main())
