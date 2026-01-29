# Testing Guide for AgentCon Demo

## Overview

This directory contains comprehensive tests for both the **original demo** (`agentcon_demo.py`) and **refactored version** (`agentcon_demo_refactored.py`).

## Test Structure

```
tests/
├── __init__.py                        # Package marker
├── test_agentcon_demo.py              # Unit tests for original demo
├── test_agentcon_demo_refactored.py   # Unit tests for refactored demo
└── test_evaluation.py                 # Evaluation tests (requires API key)
```

## Test Categories

### 1. Unit Tests (No API Required)
**Files**: `test_agentcon_demo.py`, `test_agentcon_demo_refactored.py`

These tests use **mocks** to test logic without external API calls.

**Original Demo Tests**:
- ✅ Message extraction (`last_text` helper)
- ✅ Agent role enum
- ✅ Agent factory creation
- ✅ Sequential workflow execution
- ✅ Text vs image mode handling
- ✅ Error handling

**Refactored Demo Tests**:
- ✅ Configuration loading (`DemoConfig.from_env()`)
- ✅ YAML configuration parsing
- ✅ Strategy pattern implementation
- ✅ Dependency injection
- ✅ Agent factory with injected dependencies
- ✅ Pipeline orchestration
- ✅ Design pattern validation

**Run unit tests only**:
```bash
pytest tests/test_agentcon_demo.py tests/test_agentcon_demo_refactored.py -v
```

### 2. Evaluation Tests (Requires API Key)
**File**: `test_evaluation.py`

These tests make **real API calls** to evaluate output quality.

**What's Evaluated**:
- ✅ Output quality metrics
- ✅ MCP grounding and citations
- ✅ Diagram syntax generation
- ✅ IaC (Bicep) code generation
- ✅ Azure references in outputs
- ✅ Critique quality
- ✅ Version comparison (original vs refactored)
- ✅ Error resilience

**Run evaluation tests**:
```bash
# Set API key first
export OPENAI_API_KEY="your-key-here"  # Linux/Mac
# OR
$env:OPENAI_API_KEY="your-key-here"    # PowerShell

pytest tests/test_evaluation.py -v -s
```

## Installation

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Dependencies:
- `pytest>=7.4.0` - Test framework
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-cov>=4.1.0` - Coverage reporting

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_agentcon_demo.py -v
pytest tests/test_agentcon_demo_refactored.py -v
pytest tests/test_evaluation.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_agentcon_demo.py::TestLastText -v
pytest tests/test_agentcon_demo_refactored.py::TestDemoConfig -v
```

### Run Specific Test
```bash
pytest tests/test_agentcon_demo.py::TestLastText::test_extracts_last_assistant_message -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=agentcon_demo --cov=agentcon_demo_refactored --cov-report=html
```

View coverage: Open `htmlcov/index.html` in browser

### Skip Evaluation Tests (No API Key)
```bash
pytest tests/ -v -m "not evaluation"
```

### Run Only Evaluation Tests
```bash
pytest tests/test_evaluation.py -v
```

## Test Markers

Tests are marked by category:
- `unit` - Unit tests with mocks
- `integration` - Integration tests
- `evaluation` - Requires OpenAI API key
- `slow` - Long-running tests

Run tests by marker:
```bash
pytest -m unit -v
pytest -m evaluation -v
```

## Configuration

Test configuration in `pytest.ini`:
- Test discovery patterns
- Async mode settings
- Coverage settings
- Warning filters

## Evaluation Metrics

The evaluation framework (`test_evaluation.py`) uses these metrics:

### `EvaluationMetrics` Class

**1. `has_azure_references(text)`**
- Checks for Azure service mentions
- Keywords: azure, microsoft, cosmos, functions, storage

**2. `has_mcp_citations(text)`**
- Checks for MCP grounding citations
- Patterns: learn.microsoft.com, [source:, citation:

**3. `has_critique_elements(text)`**
- Checks for architecture critique elements
- Keywords: security, scalability, reliability, cost, performance

**4. `has_iac_code(text)`**
- Checks for Bicep code syntax
- Patterns: bicep, resource, param, module, @description

**5. `has_diagram_syntax(text)`**
- Checks for Mermaid diagram syntax
- Patterns: mermaid, graph, -->, flowchart, subgraph

## Sample Architecture Inputs

Three sample architectures for testing:

**1. Simple Web App**
- Frontend: React SPA on Static Web Apps
- Backend: Azure Functions
- Database: Cosmos DB
- Auth: Azure AD B2C

**2. Microservices**
- API Gateway: API Management
- Services: 3 Container Apps
- Message Bus: Service Bus
- Database: SQL with replicas
- Cache: Redis Cache

**3. IoT Solution**
- Device Connectivity: IoT Hub
- Stream Processing: Stream Analytics
- Hot Storage: Cosmos DB
- Cold Storage: Data Lake
- Analytics: Synapse Analytics

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run unit tests
        run: pytest tests/test_agentcon_demo.py tests/test_agentcon_demo_refactored.py -v
      - name: Run evaluations
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: pytest tests/test_evaluation.py -v
```

## Writing New Tests

### Unit Test Template
```python
class TestNewFeature:
    """Test description"""
    
    @pytest.fixture
    def mock_dependency(self):
        """Create mock dependency"""
        return Mock()
    
    def test_feature_behavior(self, mock_dependency):
        """Test specific behavior"""
        # Arrange
        # Act
        # Assert
        pass
```

### Async Test Template
```python
@pytest.mark.asyncio
async def test_async_feature():
    """Test async functionality"""
    # Arrange
    mock_agent = Mock()
    mock_agent.run = AsyncMock(return_value=Mock())
    
    # Act
    result = await mock_agent.run("test")
    
    # Assert
    assert result is not None
```

### Evaluation Test Template
```python
@pytest.mark.asyncio
@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="Requires API key")
async def test_output_quality():
    """Test real API output quality"""
    # Import module
    import agentcon_demo
    
    # Setup
    # Run
    # Evaluate with metrics
    pass
```

## Troubleshooting

### Import Errors
```bash
# Ensure parent directory in path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Async Test Issues
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Set asyncio_mode in pytest.ini
asyncio_mode = "auto"
```

### Coverage Issues
```bash
# Generate detailed coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing
```

### Evaluation Tests Failing
```bash
# Check API key is set
echo $OPENAI_API_KEY  # Linux/Mac
echo $env:OPENAI_API_KEY  # PowerShell

# Skip evaluation tests
pytest -m "not evaluation"
```

## Best Practices

1. **Mock External Dependencies**: Never make real API calls in unit tests
2. **Use Fixtures**: Share setup code with fixtures
3. **Test Edge Cases**: Empty inputs, long inputs, None values
4. **Async Tests**: Use `pytest.mark.asyncio` and `AsyncMock`
5. **Clear Names**: Test names should describe what they test
6. **AAA Pattern**: Arrange, Act, Assert
7. **One Assertion Focus**: Each test should verify one behavior

## Coverage Goals

Target coverage metrics:
- **Overall**: >80%
- **Critical paths**: >90%
- **Helper functions**: 100%

Current coverage:
```bash
pytest --cov=. --cov-report=term
```

## Related Documentation

- [README.md](../README.md) - Main project documentation
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [VERSION_COMPARISON.md](../VERSION_COMPARISON.md) - Compare versions
- [REFACTORING_GUIDE.md](../REFACTORING_GUIDE.md) - Pattern explanations

## Contributing Tests

When adding new features:
1. Write unit tests first (TDD)
2. Mock all external dependencies
3. Add evaluation tests if quality matters
4. Update this README with new test categories
5. Ensure >80% coverage

## Support

For test issues:
1. Check pytest output carefully
2. Review test configuration in `pytest.ini`
3. Verify environment variables set correctly
4. Check mock setup matches actual code
5. Review recent code changes that might affect tests
