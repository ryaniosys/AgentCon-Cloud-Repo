# Step 6: IaC Generator (Bicep)

**Duration:** 8 minutes (80-88 min of workshop)

## Learning Objectives
- Add **Infrastructure-as-Code generation** to the pipeline
- Generate **Azure Bicep code** from architecture descriptions
- Understand **declarative deployment** from agent output
- Complete a **full architecture lifecycle**: Analyze → Fix → Visualize → Deploy

## Key Concept
**IaC Agent:** Translates human-readable architecture into deployable Bicep code. This closes the loop from design to deployment, enabling:
- **Automated provisioning** from natural language
- **Consistent deployments** (no manual portal clicking)
- **Version-controlled infrastructure** (Git-friendly)
- **Testable architectures** (validate before deploy)

## What's New from Step 5
- Added `IAC_GENERATOR` role to enum
- Fourth pipeline step: Critic → Fixer → Visualizer → **IaC Generator**
- IaC Generator gets MCP tool (needs Bicep syntax/best practices)
- Complete end-to-end workflow: from critique to deployment code

## Run This Step
```bash
cd workshop\step6_iac_generator
python agentcon_demo.py
```

## Expected Output
1. Steps 1-3 run as before (Critic, Fixer, Visualizer)
2. **Step 4:** Bicep code like:
```bicep
param location string = resourceGroup().location

resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: 'my-app-service'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
  }
}
```

## What's Happening

### Adding the Fourth Agent
```python
class AgentRole(Enum):
    CRITIC = "architecture_critic"
    FIXER = "architecture_fixer"
    VISUALIZER = "diagram_visualizer"
    IAC_GENERATOR = "iac_generator"  # New role
```

### Tool Assignment Logic
```python
# IaC Generator needs MCP for Bicep syntax/best practices
tools = [self.mcp_tool] if role != AgentRole.VISUALIZER else []
```

**Tool Assignment by Role:**
- ✅ CRITIC: Gets MCP (research Azure best practices)
- ✅ FIXER: Gets MCP (reference Well-Architected Framework)
- ❌ VISUALIZER: No MCP (generates diagrams from LLM knowledge)
- ✅ IAC_GENERATOR: Gets MCP (look up Bicep syntax, resource properties)

### IaC Prompt Engineering
```python
instructions = """You are a Bicep IaC Generator.
Generate **Azure Bicep code** to deploy the improved architecture.
Include:
- Resource definitions (App Service, SQL, VNet, etc.)
- Secure configurations (Private Endpoints, managed identities)
- Parameters and outputs
**Use Microsoft Learn MCP tool** for Bicep best practices..."""
```

Key elements:
- **Specific format** (Bicep, not ARM/Terraform)
- **Security requirements** (Private Endpoints, managed identities)
- **Structure guidance** (parameters, outputs)
- **MCP instruction** (cite best practices)

## Deploying the Generated Code
1. Save output to `main.bicep`
2. Validate: `az bicep build --file main.bicep`
3. Deploy: `az deployment group create --resource-group <rg> --template-file main.bicep`

## Discussion Points
- Why Bicep vs Terraform? (Azure-native, simpler syntax, type safety)
- How to validate generated code? (linting, testing, dry-run deploys)
- Error handling: What if generated code is invalid?
- Production considerations: Add CI/CD pipelines, testing gates

## Real-World Pipeline Enhancement
In production, you might add:
- **Validator Agent:** Lint Bicep code, check policies
- **Cost Estimator Agent:** Calculate deployment costs
- **Security Auditor Agent:** Check for compliance violations
- **Tester Agent:** Generate test cases for deployed resources

## Complete Lifecycle
```
User Idea (text)
    ↓
Critic Agent → Identifies issues
    ↓
Fixer Agent → Proposes improvements
    ↓
Visualizer Agent → Generates diagram
    ↓
IaC Generator → Creates Bicep code
    ↓
Azure Deployment → Infrastructure live
```

## Next: [Step 7 - Image Mode (Bonus) →](../step7_image_mode/)

## 📖 Detailed Learning

For a comprehensive walkthrough of this step including:
- Understanding IaC and Bicep syntax
- How to structure Bicep generation prompts
- Explanation of each code line and "why"
- Best practices for infrastructure code generation
- Validation and testing strategies

👉 See the **[TUTORIAL.md](../../TUTORIAL.md#part-6-infrastructure-as-code--bicep-generation)** file!

It covers Step 6 in detail with full explanations.
