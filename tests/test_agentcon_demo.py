"""
Unit Tests for Original AgentCon Demo (agentcon_demo.py)
Tests basic functionality without external API calls
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentcon_demo import (
    AgentRole,
    AgentFactory,
    last_text,
    run_sequential_workflow
)


class TestLastText:
    """Test the last_text helper function"""
    
    def test_extracts_last_assistant_message(self):
        """Should extract last assistant message with content"""
        mock_msg1 = Mock(role="assistant", content="First message")
        mock_msg2 = Mock(role="assistant", content="Second message")
        mock_response = Mock(messages=[mock_msg1, mock_msg2])
        
        result = last_text(mock_response)
        
        assert result == "Second message"
    
    def test_skips_messages_without_content(self):
        """Should skip messages with None content"""
        mock_msg1 = Mock(role="assistant", content="Good message")
        mock_msg2 = Mock(role="assistant", content=None)
        mock_response = Mock(messages=[mock_msg1, mock_msg2])
        
        result = last_text(mock_response)
        
        assert result == "Good message"
    
    def test_skips_non_assistant_messages(self):
        """Should skip user and system messages"""
        mock_msg1 = Mock(role="user", content="User message")
        mock_msg2 = Mock(role="assistant", content="Assistant message")
        mock_response = Mock(messages=[mock_msg1, mock_msg2])
        
        result = last_text(mock_response)
        
        assert result == "Assistant message"
    
    def test_returns_empty_string_when_no_valid_messages(self):
        """Should return empty string if no valid messages found"""
        mock_response = Mock(messages=[])
        
        result = last_text(mock_response)
        
        assert result == ""


class TestAgentRole:
    """Test AgentRole enum"""
    
    def test_has_all_required_roles(self):
        """Should have all 5 agent roles defined"""
        assert hasattr(AgentRole, "DIAGRAM_INTERPRETER")
        assert hasattr(AgentRole, "CRITIC")
        assert hasattr(AgentRole, "FIXER")
        assert hasattr(AgentRole, "VISUALIZER")
        assert hasattr(AgentRole, "IAC_GENERATOR")
    
    def test_role_values_are_strings(self):
        """Role values should be strings for agent names"""
        assert isinstance(AgentRole.CRITIC.value, str)
        assert isinstance(AgentRole.FIXER.value, str)


class TestAgentFactory:
    """Test AgentFactory class"""
    
    @pytest.fixture
    def mock_mcp_tool(self):
        """Mock MCP tool"""
        return Mock()
    
    @pytest.fixture
    def factory(self, mock_mcp_tool):
        """Create factory with mocked dependencies"""
        with patch.dict('os.environ', {
            'OPENAI_API_KEY': 'test-key',
            'OPENAI_MODEL': 'gpt-4o'
        }):
            with patch('agentcon_demo.OpenAIChatClient') as mock_client:
                factory = AgentFactory(mock_mcp_tool)
                factory.chat_client = Mock()  # Replace with mock
                return factory
    
    def test_creates_critic_agent_with_mcp(self, factory, mock_mcp_tool):
        """Critic agent should be created with MCP tool"""
        with patch('agentcon_demo.ChatAgent') as mock_agent_class:
            agent = factory.create_agent(AgentRole.CRITIC)
            
            # Verify ChatAgent was called
            mock_agent_class.assert_called_once()
            call_kwargs = mock_agent_class.call_args[1]
            
            # Should include MCP tool
            assert call_kwargs['tools'] == [mock_mcp_tool]
            assert 'critic' in call_kwargs['name'].lower()
    
    def test_creates_visualizer_agent_without_mcp(self, factory):
        """Visualizer agent should NOT have MCP tool"""
        with patch('agentcon_demo.ChatAgent') as mock_agent_class:
            agent = factory.create_agent(AgentRole.VISUALIZER)
            
            mock_agent_class.assert_called_once()
            call_kwargs = mock_agent_class.call_args[1]
            
            # Should NOT include MCP tool
            assert call_kwargs['tools'] == []
            assert 'visualizer' in call_kwargs['name'].lower()
    
    def test_creates_all_agent_types(self, factory):
        """Factory should create all 5 agent types"""
        with patch('agentcon_demo.ChatAgent'):
            for role in AgentRole:
                agent = factory.create_agent(role)
                assert agent is not None


class TestSequentialWorkflow:
    """Test the sequential workflow execution"""
    
    @pytest.fixture
    def mock_factory(self):
        """Mock AgentFactory"""
        factory = Mock()
        
        # Mock agents with async run methods
        async def mock_run(input_data):
            mock_msg = Mock(role="assistant", content="Mock response")
            return Mock(messages=[mock_msg])
        
        mock_agent = Mock()
        mock_agent.run = AsyncMock(side_effect=mock_run)
        factory.create_agent = Mock(return_value=mock_agent)
        
        return factory
    
    @pytest.mark.asyncio
    async def test_text_mode_skips_interpretation(self, mock_factory):
        """Text mode should skip diagram interpretation step"""
        test_input = "Test architecture"
        
        with patch('builtins.print'):  # Suppress output
            await run_sequential_workflow(mock_factory, test_input, is_image=False)
        
        # Should call create_agent 4 times (not 5 - no interpreter)
        assert mock_factory.create_agent.call_count == 4
        
        # Should NOT create DIAGRAM_INTERPRETER
        created_roles = [call[0][0] for call in mock_factory.create_agent.call_args_list]
        assert AgentRole.DIAGRAM_INTERPRETER not in created_roles
    
    @pytest.mark.asyncio
    async def test_image_mode_includes_interpretation(self, mock_factory):
        """Image mode should include diagram interpretation step"""
        mock_image = Mock()
        
        with patch('builtins.print'):  # Suppress output
            await run_sequential_workflow(mock_factory, mock_image, is_image=True)
        
        # Should call create_agent 5 times (includes interpreter)
        assert mock_factory.create_agent.call_count == 5
        
        # Should create DIAGRAM_INTERPRETER first
        first_role = mock_factory.create_agent.call_args_list[0][0][0]
        assert first_role == AgentRole.DIAGRAM_INTERPRETER
    
    @pytest.mark.asyncio
    async def test_workflow_executes_all_steps_in_order(self, mock_factory):
        """Workflow should execute all steps in correct order"""
        test_input = "Test architecture"
        
        with patch('builtins.print'):
            await run_sequential_workflow(mock_factory, test_input, is_image=False)
        
        # Extract created roles in order
        created_roles = [call[0][0] for call in mock_factory.create_agent.call_args_list]
        
        # Verify order: Critic → Fixer → Visualizer → IaC
        assert created_roles[0] == AgentRole.CRITIC
        assert created_roles[1] == AgentRole.FIXER
        assert created_roles[2] == AgentRole.VISUALIZER
        assert created_roles[3] == AgentRole.IAC_GENERATOR
    
    @pytest.mark.asyncio
    async def test_workflow_passes_critique_to_fixer(self, mock_factory):
        """Fixer should receive both original architecture and critique"""
        test_input = "Original architecture"
        
        # Track what's passed to each agent
        run_inputs = []
        
        async def capture_run(input_data):
            run_inputs.append(input_data)
            mock_msg = Mock(role="assistant", content=f"Response {len(run_inputs)}")
            return Mock(messages=[mock_msg])
        
        mock_agent = Mock()
        mock_agent.run = AsyncMock(side_effect=capture_run)
        mock_factory.create_agent = Mock(return_value=mock_agent)
        
        with patch('builtins.print'):
            await run_sequential_workflow(mock_factory, test_input, is_image=False)
        
        # Fixer (2nd call) should receive combined input
        fixer_input = run_inputs[1]
        assert "Original" in fixer_input
        assert "Response 1" in fixer_input  # Critique from step 1


class TestIntegration:
    """Integration tests without external API calls"""
    
    @pytest.mark.asyncio
    async def test_main_flow_with_mocks(self):
        """Test main flow with all dependencies mocked"""
        test_config = {
            'OPENAI_API_KEY': 'test-key',
            'OPENAI_MODEL': 'gpt-4o',
            'USE_IMAGE_MODE': 'false',
            'ARCHITECTURE_IMAGE_PATH': ''
        }
        
        with patch.dict('os.environ', test_config):
            with patch('agentcon_demo.load_dotenv'):
                with patch('agentcon_demo.MCPStreamableHTTPTool') as mock_mcp:
                    with patch('agentcon_demo.OpenAIChatClient') as mock_client:
                        with patch('agentcon_demo.ChatAgent') as mock_agent_class:
                            # Mock agent run method
                            async def mock_run(input_data):
                                return Mock(messages=[Mock(role="assistant", content="Test")])
                            
                            mock_agent = Mock()
                            mock_agent.run = AsyncMock(side_effect=mock_run)
                            mock_agent_class.return_value = mock_agent
                            
                            # Import and run main
                            from agentcon_demo import main
                            
                            with patch('builtins.print'):
                                await main()
                            
                            # Verify MCP tool was created
                            mock_mcp.assert_called_once()
                            
                            # Verify OpenAI client was created
                            mock_client.assert_called()


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @pytest.mark.asyncio
    async def test_handles_empty_agent_response(self):
        """Should handle agents returning empty responses"""
        factory = Mock()
        
        async def empty_response(input_data):
            return Mock(messages=[])
        
        mock_agent = Mock()
        mock_agent.run = AsyncMock(side_effect=empty_response)
        factory.create_agent = Mock(return_value=mock_agent)
        
        with patch('builtins.print'):
            # Should not raise exception
            await run_sequential_workflow(factory, "test", is_image=False)
    
    @pytest.mark.asyncio
    async def test_handles_agent_with_tool_calls(self):
        """Should handle agents that return tool call messages"""
        factory = Mock()
        
        async def tool_call_response(input_data):
            # Mix of tool calls and assistant messages
            return Mock(messages=[
                Mock(role="tool", content="Tool result"),
                Mock(role="assistant", content=None),  # Tool call message
                Mock(role="assistant", content="Final response")
            ])
        
        mock_agent = Mock()
        mock_agent.run = AsyncMock(side_effect=tool_call_response)
        factory.create_agent = Mock(return_value=mock_agent)
        
        with patch('builtins.print'):
            await run_sequential_workflow(factory, "test", is_image=False)
        
        # Should complete without errors


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
