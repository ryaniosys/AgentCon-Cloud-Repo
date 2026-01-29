"""
Unit Tests for Refactored AgentCon Demo (agentcon_demo_refactored.py)
Tests design patterns and architecture
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, mock_open
from pathlib import Path
from dataclasses import dataclass
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentcon_demo_refactored import (
    DemoConfig,
    AgentRole,
    TextInputStrategy,
    ImageInputStrategy,
    AgentFactory,
    AgentPipeline,
    extract_last_text,
    load_agent_config,
    create_input_strategy,
    setup_dependencies
)


class TestDemoConfig:
    """Test configuration dataclass and factory method"""
    
    def test_from_env_loads_all_config(self):
        """Should load all configuration from environment variables"""
        test_env = {
            'OPENAI_API_KEY': 'test-api-key',
            'OPENAI_MODEL': 'gpt-4o-test',
            'USE_IMAGE_MODE': 'true',
            'ARCHITECTURE_IMAGE_PATH': '/path/to/image.png'
        }
        
        with patch.dict('os.environ', test_env):
            with patch('agentcon_demo_refactored.load_dotenv'):
                config = DemoConfig.from_env()
        
        assert config.openai_api_key == 'test-api-key'
        assert config.openai_model == 'gpt-4o-test'
        assert config.use_image_mode is True
        assert config.image_path == '/path/to/image.png'
    
    def test_from_env_provides_defaults(self):
        """Should provide sensible defaults when env vars missing"""
        with patch.dict('os.environ', {}, clear=True):
            with patch('agentcon_demo_refactored.load_dotenv'):
                config = DemoConfig.from_env()
        
        assert config.openai_model == 'gpt-4o'  # Default model
        assert config.use_image_mode is False   # Default to text mode
        assert config.mcp_endpoint == "https://learn.microsoft.com/api/mcp"
    
    def test_config_is_immutable(self):
        """Config should be a frozen dataclass (immutable)"""
        with patch('agentcon_demo_refactored.load_dotenv'):
            config = DemoConfig.from_env()
        
        # Try to modify - should raise if frozen
        with pytest.raises(AttributeError):
            config.openai_api_key = "new-key"


class TestExtractLastText:
    """Test the extract_last_text helper function"""
    
    def test_extracts_last_assistant_message(self):
        """Should extract content from last assistant message"""
        mock_response = Mock(messages=[
            Mock(role="assistant", content="First"),
            Mock(role="assistant", content="Last")
        ])
        
        result = extract_last_text(mock_response)
        assert result == "Last"
    
    def test_skips_tool_messages(self):
        """Should skip tool messages and find assistant content"""
        mock_response = Mock(messages=[
            Mock(role="assistant", content="Good message"),
            Mock(role="tool", content="Tool output"),
        ])
        
        result = extract_last_text(mock_response)
        assert result == "Good message"


class TestTextInputStrategy:
    """Test TextInputStrategy implementation"""
    
    def test_returns_text_input(self):
        """Should return the text provided"""
        strategy = TextInputStrategy("Test architecture")
        assert strategy.get_input() == "Test architecture"
    
    def test_does_not_require_interpretation(self):
        """Text input should not require interpretation"""
        strategy = TextInputStrategy("Test architecture")
        assert strategy.requires_interpretation() is False
    
    def test_implements_protocol(self):
        """Should implement InputStrategy protocol"""
        strategy = TextInputStrategy("test")
        assert hasattr(strategy, 'get_input')
        assert hasattr(strategy, 'requires_interpretation')
        assert callable(strategy.get_input)
        assert callable(strategy.requires_interpretation)


class TestImageInputStrategy:
    """Test ImageInputStrategy implementation"""
    
    def test_requires_interpretation(self):
        """Image input should require interpretation"""
        strategy = ImageInputStrategy("/path/to/image.png")
        assert strategy.requires_interpretation() is True
    
    def test_handles_url_input(self):
        """Should detect and handle URL inputs"""
        with patch('agentcon_demo_refactored.ImageContent') as mock_image:
            strategy = ImageInputStrategy("https://example.com/diagram.png")
            result = strategy.get_input()
            
            # Should call ImageContent with url parameter
            mock_image.assert_called_once_with(url="https://example.com/diagram.png")
    
    def test_handles_local_file_input(self):
        """Should detect and handle local file paths"""
        with patch('agentcon_demo_refactored.ImageContent') as mock_image:
            strategy = ImageInputStrategy("/local/diagram.png")
            result = strategy.get_input()
            
            # Should call ImageContent.from_file
            mock_image.from_file.assert_called_once_with("/local/diagram.png")
    
    def test_implements_protocol(self):
        """Should implement InputStrategy protocol"""
        strategy = ImageInputStrategy("test.png")
        assert hasattr(strategy, 'get_input')
        assert hasattr(strategy, 'requires_interpretation')


class TestAgentFactory:
    """Test AgentFactory with dependency injection"""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mocked dependencies"""
        mock_chat_client = Mock()
        mock_mcp_tool = Mock()
        return mock_chat_client, mock_mcp_tool
    
    @pytest.fixture
    def mock_config(self):
        """Create mock agent configuration"""
        return {
            'agents': {
                'critic': {
                    'name': 'Test Critic',
                    'instructions': 'Test instructions',
                    'uses_mcp': True
                },
                'visualizer': {
                    'name': 'Test Visualizer',
                    'instructions': 'Test instructions',
                    'uses_mcp': False
                }
            }
        }
    
    def test_injects_dependencies(self, mock_dependencies):
        """Factory should accept injected dependencies"""
        chat_client, mcp_tool = mock_dependencies
        
        with patch('agentcon_demo_refactored.load_agent_config', return_value={'agents': {}}):
            factory = AgentFactory(chat_client, mcp_tool)
        
        assert factory._chat_client == chat_client
        assert factory._mcp_tool == mcp_tool
    
    def test_loads_configuration_from_yaml(self, mock_dependencies):
        """Factory should load agent configuration from YAML"""
        with patch('agentcon_demo_refactored.load_agent_config') as mock_load:
            mock_load.return_value = {'agents': {'test': {}}}
            factory = AgentFactory(*mock_dependencies)
            
            mock_load.assert_called_once()
    
    def test_creates_agent_with_mcp_when_configured(self, mock_dependencies, mock_config):
        """Should add MCP tool when uses_mcp is true"""
        chat_client, mcp_tool = mock_dependencies
        
        with patch('agentcon_demo_refactored.load_agent_config', return_value=mock_config):
            with patch('agentcon_demo_refactored.ChatAgent') as mock_agent:
                factory = AgentFactory(chat_client, mcp_tool)
                agent = factory.create_agent(AgentRole.CRITIC)
                
                # Verify MCP tool included
                call_kwargs = mock_agent.call_args[1]
                assert call_kwargs['tools'] == [mcp_tool]
    
    def test_creates_agent_without_mcp_when_not_configured(self, mock_dependencies, mock_config):
        """Should NOT add MCP tool when uses_mcp is false"""
        chat_client, mcp_tool = mock_dependencies
        
        with patch('agentcon_demo_refactored.load_agent_config', return_value=mock_config):
            with patch('agentcon_demo_refactored.ChatAgent') as mock_agent:
                factory = AgentFactory(chat_client, mcp_tool)
                agent = factory.create_agent(AgentRole.VISUALIZER)
                
                # Verify MCP tool NOT included
                call_kwargs = mock_agent.call_args[1]
                assert call_kwargs['tools'] == []


class TestAgentPipeline:
    """Test AgentPipeline orchestration"""
    
    @pytest.fixture
    def mock_factory(self):
        """Create mock factory with agents"""
        factory = Mock()
        
        async def mock_agent_run(input_data):
            return Mock(messages=[Mock(role="assistant", content="Mock response")])
        
        mock_agent = Mock()
        mock_agent.run = AsyncMock(side_effect=mock_agent_run)
        factory.create_agent = Mock(return_value=mock_agent)
        
        return factory
    
    @pytest.fixture
    def pipeline(self, mock_factory):
        """Create pipeline with mocked factory"""
        return AgentPipeline(mock_factory)
    
    @pytest.mark.asyncio
    async def test_runs_all_steps_for_text_input(self, pipeline, mock_factory):
        """Should run all 4 steps for text input"""
        text_strategy = TextInputStrategy("Test architecture")
        
        with patch('builtins.print'):
            results = await pipeline.run(text_strategy)
        
        # Should have 4 results (no interpretation)
        assert 'input' in results
        assert 'critique' in results
        assert 'improved' in results
        assert 'diagram' in results
        assert 'iac' in results
        assert 'interpretation' not in results
    
    @pytest.mark.asyncio
    async def test_runs_interpretation_for_image_input(self, pipeline, mock_factory):
        """Should run interpretation step for image input"""
        with patch('agentcon_demo_refactored.ImageContent'):
            image_strategy = ImageInputStrategy("test.png")
        
        with patch('builtins.print'):
            results = await pipeline.run(image_strategy)
        
        # Should have interpretation result
        assert 'interpretation' in results
        assert 'input' not in results  # Input not stored separately
    
    @pytest.mark.asyncio
    async def test_single_responsibility_methods(self, pipeline, mock_factory):
        """Each pipeline method should have single responsibility"""
        # Test individual methods
        with patch('builtins.print'):
            critique = await pipeline._critique_architecture("test")
            assert critique == "Mock response"
            
            improved = await pipeline._fix_architecture("original", "critique")
            assert improved == "Mock response"
            
            diagram = await pipeline._visualize_architecture("improved")
            assert diagram == "Mock response"
            
            iac = await pipeline._generate_iac("improved")
            assert iac == "Mock response"
    
    @pytest.mark.asyncio
    async def test_pipeline_creates_correct_agents(self, pipeline, mock_factory):
        """Pipeline should create agents in correct order"""
        text_strategy = TextInputStrategy("Test")
        
        with patch('builtins.print'):
            await pipeline.run(text_strategy)
        
        # Extract agent roles created
        created_roles = [call[0][0] for call in mock_factory.create_agent.call_args_list]
        
        assert AgentRole.CRITIC in created_roles
        assert AgentRole.FIXER in created_roles
        assert AgentRole.VISUALIZER in created_roles
        assert AgentRole.IAC_GENERATOR in created_roles


class TestLoadAgentConfig:
    """Test YAML configuration loading"""
    
    def test_loads_yaml_configuration(self):
        """Should load and parse YAML configuration file"""
        mock_yaml = """
agents:
  critic:
    name: "Test Critic"
    instructions: "Test instructions"
    uses_mcp: true
"""
        
        with patch('builtins.open', mock_open(read_data=mock_yaml)):
            with patch('agentcon_demo_refactored.yaml.safe_load') as mock_load:
                mock_load.return_value = {'agents': {'critic': {}}}
                config = load_agent_config()
                
                assert 'agents' in config


class TestCreateInputStrategy:
    """Test input strategy factory function"""
    
    def test_creates_image_strategy_when_enabled(self):
        """Should create ImageInputStrategy when image mode enabled"""
        config = DemoConfig(
            openai_api_key="test",
            openai_model="gpt-4o",
            use_image_mode=True,
            image_path="/path/to/image.png"
        )
        
        with patch('builtins.print'):
            strategy = create_input_strategy(config)
        
        assert isinstance(strategy, ImageInputStrategy)
    
    def test_creates_text_strategy_by_default(self):
        """Should create TextInputStrategy when image mode disabled"""
        config = DemoConfig(
            openai_api_key="test",
            openai_model="gpt-4o",
            use_image_mode=False,
            image_path=""
        )
        
        with patch('builtins.print'):
            strategy = create_input_strategy(config)
        
        assert isinstance(strategy, TextInputStrategy)
    
    def test_creates_text_strategy_when_no_image_path(self):
        """Should default to text mode if image path empty"""
        config = DemoConfig(
            openai_api_key="test",
            openai_model="gpt-4o",
            use_image_mode=True,
            image_path=""
        )
        
        with patch('builtins.print'):
            strategy = create_input_strategy(config)
        
        assert isinstance(strategy, TextInputStrategy)


class TestSetupDependencies:
    """Test dependency setup (composition root)"""
    
    def test_creates_chat_client_with_config(self):
        """Should create OpenAIChatClient with config parameters"""
        config = DemoConfig(
            openai_api_key="test-key",
            openai_model="gpt-4o-test",
            use_image_mode=False,
            image_path=""
        )
        
        with patch('agentcon_demo_refactored.OpenAIChatClient') as mock_client:
            with patch('agentcon_demo_refactored.MCPStreamableHTTPTool') as mock_mcp:
                chat_client, mcp_tool = setup_dependencies(config)
                
                # Verify client created with correct params
                mock_client.assert_called_once_with(
                    api_key="test-key",
                    model="gpt-4o-test"
                )
    
    def test_creates_mcp_tool_with_endpoint(self):
        """Should create MCP tool with configured endpoint"""
        config = DemoConfig(
            openai_api_key="test",
            openai_model="gpt-4o",
            use_image_mode=False,
            image_path="",
            mcp_endpoint="https://custom.mcp.endpoint"
        )
        
        with patch('agentcon_demo_refactored.OpenAIChatClient'):
            with patch('agentcon_demo_refactored.MCPStreamableHTTPTool') as mock_mcp:
                chat_client, mcp_tool = setup_dependencies(config)
                
                # Verify MCP tool created with custom endpoint
                mock_mcp.assert_called_once_with("https://custom.mcp.endpoint")
    
    def test_returns_both_dependencies(self):
        """Should return tuple of (chat_client, mcp_tool)"""
        config = DemoConfig(
            openai_api_key="test",
            openai_model="gpt-4o",
            use_image_mode=False,
            image_path=""
        )
        
        with patch('agentcon_demo_refactored.OpenAIChatClient') as mock_client:
            with patch('agentcon_demo_refactored.MCPStreamableHTTPTool') as mock_mcp:
                result = setup_dependencies(config)
                
                assert isinstance(result, tuple)
                assert len(result) == 2


class TestIntegration:
    """Integration tests for refactored version"""
    
    @pytest.mark.asyncio
    async def test_main_flow_composes_correctly(self):
        """Test that main() composes all components correctly"""
        test_env = {
            'OPENAI_API_KEY': 'test-key',
            'OPENAI_MODEL': 'gpt-4o',
            'USE_IMAGE_MODE': 'false'
        }
        
        async def mock_agent_run(input_data):
            return Mock(messages=[Mock(role="assistant", content="Test")])
        
        with patch.dict('os.environ', test_env):
            with patch('agentcon_demo_refactored.load_dotenv'):
                with patch('agentcon_demo_refactored.MCPStreamableHTTPTool'):
                    with patch('agentcon_demo_refactored.OpenAIChatClient'):
                        with patch('agentcon_demo_refactored.load_agent_config') as mock_config:
                            mock_config.return_value = {'agents': {
                                'critic': {'instructions': 'test', 'uses_mcp': True},
                                'fixer': {'instructions': 'test', 'uses_mcp': True},
                                'visualizer': {'instructions': 'test', 'uses_mcp': False},
                                'iac_generator': {'instructions': 'test', 'uses_mcp': True},
                                'diagram_interpreter': {'instructions': 'test', 'uses_mcp': False}
                            }}
                            
                            with patch('agentcon_demo_refactored.ChatAgent') as mock_agent_class:
                                mock_agent = Mock()
                                mock_agent.run = AsyncMock(side_effect=mock_agent_run)
                                mock_agent_class.return_value = mock_agent
                                
                                from agentcon_demo_refactored import main
                                
                                with patch('builtins.print'):
                                    await main()


class TestDesignPatterns:
    """Test that design patterns are correctly implemented"""
    
    def test_strategy_pattern_implemented(self):
        """Verify Strategy pattern is properly implemented"""
        # Both strategies should implement the protocol
        text_strategy = TextInputStrategy("test")
        
        with patch('agentcon_demo_refactored.ImageContent'):
            image_strategy = ImageInputStrategy("test.png")
        
        # Both should have same interface
        assert hasattr(text_strategy, 'get_input')
        assert hasattr(image_strategy, 'get_input')
        assert hasattr(text_strategy, 'requires_interpretation')
        assert hasattr(image_strategy, 'requires_interpretation')
    
    def test_dependency_injection_used(self):
        """Verify dependencies are injected, not created internally"""
        mock_client = Mock()
        mock_mcp = Mock()
        
        with patch('agentcon_demo_refactored.load_agent_config', return_value={'agents': {}}):
            factory = AgentFactory(mock_client, mock_mcp)
        
        # Factory should store injected dependencies
        assert factory._chat_client is mock_client
        assert factory._mcp_tool is mock_mcp
    
    def test_configuration_is_separate_from_code(self):
        """Verify prompts are in configuration, not hardcoded"""
        # load_agent_config should load from YAML
        mock_yaml = {'agents': {'test': {'instructions': 'from yaml'}}}
        
        with patch('agentcon_demo_refactored.yaml.safe_load', return_value=mock_yaml):
            with patch('builtins.open', mock_open()):
                config = load_agent_config()
        
        # Configuration should be loaded, not hardcoded
        assert config['agents']['test']['instructions'] == 'from yaml'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
