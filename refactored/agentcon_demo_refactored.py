"""
AgentCon Zürich Demo: Agentic AI with Microsoft Learn MCP (Refactored)
=======================================================================
Demonstrates: Clean Architecture + Agent Factory + MCP grounding

Improvements from bestpractice.md:
1. Declarative Configuration (YAML prompts)
2. Strategy Pattern (input handlers)
3. Dependency Injection (chat client)
4. Single Responsibility (smaller functions)
5. Tell, Don't Ask (input strategies)
"""
import asyncio
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol

import yaml
from dotenv import load_dotenv
from agent_framework import ChatAgent, ImageContent
from agent_framework.openai import OpenAIChatClient
from agent_framework.tools import MCPStreamableHTTPTool


# ============================================================
# Configuration (Declarative)
# ============================================================

@dataclass
class DemoConfig:
    """Configuration following Single Responsibility Principle"""
    openai_api_key: str
    openai_model: str
    use_image_mode: bool
    image_path: str
    mcp_endpoint: str = "https://learn.microsoft.com/api/mcp"
    
    @classmethod
    def from_env(cls) -> "DemoConfig":
        """Factory method for creating config from environment"""
        load_dotenv()
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            use_image_mode=os.getenv("USE_IMAGE_MODE", "false").lower() == "true",
            image_path=os.getenv("ARCHITECTURE_IMAGE_PATH", "")
        )


def load_agent_config() -> dict:
    """Load declarative agent configuration from YAML"""
    config_path = Path(__file__).parent / "agent_prompts.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


# ============================================================
# Domain Model
# ============================================================

class AgentRole(Enum):
    """Agent roles in the architecture pipeline"""
    DIAGRAM_INTERPRETER = "diagram_interpreter"
    CRITIC = "critic"
    FIXER = "fixer"
    VISUALIZER = "visualizer"
    IAC_GENERATOR = "iac_generator"


def extract_last_text(response) -> str:
    """
    Safely extract last assistant text message.
    Follows Tell, Don't Ask - encapsulates extraction logic.
    """
    for msg in reversed(response.messages):
        if msg.role == "assistant" and msg.content:
            return msg.content
    return ""


# ============================================================
# Strategy Pattern - Input Handling
# ============================================================

class InputStrategy(Protocol):
    """Protocol for input handling strategies (Hexagonal Architecture)"""
    
    def get_input(self) -> any:
        """Get the input for processing"""
        ...
    
    def requires_interpretation(self) -> bool:
        """Check if input needs interpretation step"""
        ...


class TextInputStrategy:
    """Strategy for text-based architecture descriptions"""
    
    def __init__(self, text: str):
        self._text = text
    
    def get_input(self) -> str:
        return self._text
    
    def requires_interpretation(self) -> bool:
        return False


class ImageInputStrategy:
    """Strategy for image-based architecture diagrams"""
    
    def __init__(self, image_path: str):
        self._image_path = image_path
    
    def get_input(self) -> ImageContent:
        """Tell, Don't Ask - encapsulates image loading logic"""
        if self._image_path.startswith(("http://", "https://")):
            return ImageContent(url=self._image_path)
        return ImageContent.from_file(self._image_path)
    
    def requires_interpretation(self) -> bool:
        return True


# ============================================================
# Factory Pattern - Agent Creation
# ============================================================

class AgentFactory:
    """
    Factory for creating MCP-grounded agents.
    Follows Dependency Injection + Factory Pattern.
    """
    
    def __init__(self, chat_client: OpenAIChatClient, mcp_tool: MCPStreamableHTTPTool):
        """Inject dependencies instead of creating them"""
        self._chat_client = chat_client
        self._mcp_tool = mcp_tool
        self._agent_config = load_agent_config()["agents"]
    
    def create_agent(self, role: AgentRole) -> ChatAgent:
        """
        Create agent with role-specific configuration.
        Configuration loaded from YAML (Declarative Pattern).
        """
        config = self._agent_config[role.value]
        tools = [self._mcp_tool] if config["uses_mcp"] else []
        
        return ChatAgent(
            name=role.value,
            instructions=config["instructions"],
            model_client=self._chat_client,
            tools=tools
        )


# ============================================================
# Pipeline Orchestration (Thin Controller)
# ============================================================

class AgentPipeline:
    """
    Pipeline orchestrator following Single Responsibility.
    Thin controller - delegates to agents.
    """
    
    def __init__(self, factory: AgentFactory):
        self._factory = factory
    
    async def run(self, input_strategy: InputStrategy) -> dict:
        """
        Execute pipeline with given input strategy.
        Returns structured results.
        """
        results = {}
        
        # Step 0: Optional interpretation
        if input_strategy.requires_interpretation():
            architecture_text = await self._interpret_diagram(input_strategy.get_input())
            results["interpretation"] = architecture_text
        else:
            architecture_text = input_strategy.get_input()
            results["input"] = architecture_text
        
        # Step 1: Critique
        results["critique"] = await self._critique_architecture(architecture_text)
        
        # Step 2: Fix
        results["improved"] = await self._fix_architecture(architecture_text, results["critique"])
        
        # Step 3: Visualize
        results["diagram"] = await self._visualize_architecture(results["improved"])
        
        # Step 4: Generate IaC
        results["iac"] = await self._generate_iac(results["improved"])
        
        return results
    
    async def _interpret_diagram(self, image: ImageContent) -> str:
        """Single responsibility: interpret diagram image"""
        self._print_step("🖼️  STEP 0: Diagram Interpreter (image → text)")
        agent = self._factory.create_agent(AgentRole.DIAGRAM_INTERPRETER)
        response = await agent.run(image)
        text = extract_last_text(response)
        print(text)
        return text
    
    async def _critique_architecture(self, architecture: str) -> str:
        """Single responsibility: critique architecture"""
        self._print_step("🔍 STEP 1: Architecture Critic (MCP-grounded)")
        agent = self._factory.create_agent(AgentRole.CRITIC)
        response = await agent.run(architecture)
        critique = extract_last_text(response)
        print(critique)
        return critique
    
    async def _fix_architecture(self, original: str, critique: str) -> str:
        """Single responsibility: fix architecture"""
        self._print_step("🔧 STEP 2: Architecture Fixer (MCP-grounded)")
        agent = self._factory.create_agent(AgentRole.FIXER)
        prompt = f"Original:\n{original}\n\nCritique:\n{critique}"
        response = await agent.run(prompt)
        improved = extract_last_text(response)
        print(improved)
        return improved
    
    async def _visualize_architecture(self, architecture: str) -> str:
        """Single responsibility: visualize architecture"""
        self._print_step("📊 STEP 3: Diagram Visualizer")
        agent = self._factory.create_agent(AgentRole.VISUALIZER)
        response = await agent.run(architecture)
        diagram = extract_last_text(response)
        print(diagram)
        return diagram
    
    async def _generate_iac(self, architecture: str) -> str:
        """Single responsibility: generate IaC"""
        self._print_step("📝 STEP 4: IaC Generator (MCP-grounded)")
        agent = self._factory.create_agent(AgentRole.IAC_GENERATOR)
        response = await agent.run(architecture)
        iac = extract_last_text(response)
        print(iac)
        return iac
    
    def _print_step(self, title: str):
        """Helper: consistent step formatting"""
        print(f"\n{'='*60}")
        print(title)
        print(f"{'='*60}")


# ============================================================
# Application Setup (Composition Root)
# ============================================================

def create_input_strategy(config: DemoConfig) -> InputStrategy:
    """
    Factory for input strategies.
    Follows Strategy Pattern + Factory Pattern.
    """
    if config.use_image_mode and config.image_path:
        print("📸 Image mode enabled")
        return ImageInputStrategy(config.image_path)
    
    print("📝 Text mode (default)")
    default_architecture = """
    We have a 3-tier e-commerce application on Azure:
    - Frontend: Virtual Machines running Node.js (public IPs)
    - Backend: Virtual Machines running .NET APIs (public IPs)
    - Database: Azure SQL Database (public endpoint enabled)
    - Storage: Azure Storage Account (no encryption at rest)
    """
    return TextInputStrategy(default_architecture)


def setup_dependencies(config: DemoConfig) -> tuple[OpenAIChatClient, MCPStreamableHTTPTool]:
    """
    Dependency injection setup.
    Creates infrastructure components.
    """
    chat_client = OpenAIChatClient(
        api_key=config.openai_api_key,
        model=config.openai_model
    )
    mcp_tool = MCPStreamableHTTPTool(config.mcp_endpoint)
    return chat_client, mcp_tool


# ============================================================
# Main Entry Point (Thin Controller)
# ============================================================

async def main():
    """
    Main entry point - thin controller.
    Composes dependencies and delegates to pipeline.
    """
    # Load configuration
    config = DemoConfig.from_env()
    
    # Setup dependencies (Composition Root)
    print("🔌 Connecting to Microsoft Learn MCP...")
    chat_client, mcp_tool = setup_dependencies(config)
    
    # Create factory and pipeline (Composition)
    factory = AgentFactory(chat_client, mcp_tool)
    pipeline = AgentPipeline(factory)
    
    # Create input strategy (Strategy Pattern)
    input_strategy = create_input_strategy(config)
    
    # Execute pipeline (Tell, Don't Ask)
    await pipeline.run(input_strategy)
    
    # Success
    print(f"\n{'='*60}")
    print("✅ PIPELINE COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
