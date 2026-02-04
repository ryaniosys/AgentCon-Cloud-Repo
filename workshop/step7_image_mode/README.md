# Step 7: Image Mode (Bonus)

**Duration:** 2 minutes (88-90 min of workshop) - Bonus if time permits

## Learning Objectives
- Process **images** (photos, whiteboards, screenshots) as input
- Use **multimodal AI** (vision + text) for diagram interpretation
- Add **preprocessing step** to extract text from images
- Demonstrate **real-world scenario**: photo → deployment

## Key Concept
**Multimodal AI:** Modern LLMs can "see" images using vision capabilities. This enables:
- **Whiteboard photos** → Text descriptions
- **Architecture screenshots** → Analysis
- **Hand-drawn diagrams** → Formal documentation
- **Conference room collaboration** → Automated IaC

**Image → Text → Pipeline Pattern:**
1. Diagram Interpreter (vision) → Text description
2. Text enters existing pipeline (Critic → Fixer → Visualizer → IaC)

## What's New from Step 6
- Added `DIAGRAM_INTERPRETER` role (vision-capable agent)
- `UriContent` for image inputs (supports file paths)
- `run_image_mode()` function for image preprocessing
- Environment variable: `ARCHITECTURE_IMAGE_PATH` for image input
- Fallback to text mode if no image provided

## Run This Step

### Text Mode (no image)
```bash
cd workshop\step7_image_mode
python agentcon_demo.py
```

### Image Mode (with diagram photo)
```bash
cd workshop\step7_image_mode
# Add to .env file:
ARCHITECTURE_IMAGE_PATH=path/to/diagram.jpg

python agentcon_demo.py
```

## Expected Output

### Image Mode
1. **Step 0 (NEW):** "📸 Diagram Interpreter" extracts text from image
2. Steps 1-4: Run normal pipeline with extracted text

### Text Mode
Runs Steps 1-4 as in Step 6 (fallback when no image)

## What's Happening

### Image Input with UriContent
```python
from agent_framework import UriContent

# Convert file path to file:// URI
image_uri = Path(image_path).absolute().as_uri()

# Send image to vision-capable agent
response = await interpreter.run(UriContent(uri=image_uri))
```

**UriContent:** Tells the agent to load content from a file/URL. Supports:
- Local files: `file:///C:/Users/diagrams/arch.jpg`
- Remote images: `https://example.com/diagram.png`

### Diagram Interpreter Agent
```python
instructions = """You are an Architecture Diagram Interpreter.
Extract a **detailed text description** of the Azure architecture from the image.
Identify:
- Azure services shown (VMs, databases, networks, etc.)
- Connections and data flow
- Security configurations (public vs private)
Output: Clear text description of the architecture."""
```

The agent uses vision capabilities to:
- Recognize Azure service icons/names
- Trace connections and arrows
- Read handwritten/typed annotations
- Identify security markers (locks, shields, etc.)

### Mode Detection
```python
image_path = os.getenv("ARCHITECTURE_IMAGE_PATH")

if image_path and Path(image_path).exists():
    # IMAGE MODE: Add Step 0
    architecture_text = await run_image_mode(factory, image_path)
else:
    # TEXT MODE: Use hardcoded example
    architecture_text = "..."
```

## Testing Image Mode
1. Take a photo of a whiteboard architecture diagram
2. Save as `diagram.jpg` in the workshop folder
3. Add to `.env`: `ARCHITECTURE_IMAGE_PATH=diagram.jpg`
4. Run: `python agentcon_demo.py`

**Tip:** For best results:
- Clear lighting (no shadows)
- Text/labels readable
- Azure service names visible
- Diagram centered in frame

## Discussion Points
- When to use image vs text input? (Quick capture vs detailed specs)
- Accuracy considerations? (Vision models can misread)
- Privacy/security? (Don't upload sensitive diagrams)
- Other image use cases? (Infrastructure photos, compliance audits)

## Real-World Use Cases
- **Conference room sessions:** Photo whiteboard → Automated docs
- **Legacy documentation:** Scan old diagrams → Modern IaC
- **Compliance audits:** Photo existing setup → Gap analysis
- **Rapid prototyping:** Sketch → Deployment in minutes

## Production Enhancements
- **Image preprocessing:** Crop, enhance contrast, denoise
- **Validation step:** Show extracted text, ask for confirmation
- **Error handling:** Fallback if image unclear
- **Batch processing:** Multiple diagrams → consolidated architecture

## Complete Journey
```
Whiteboard Photo
    ↓
Diagram Interpreter → "3-tier app with VMs, SQL, Storage..."
    ↓
Critic → Identifies security issues
    ↓
Fixer → Proposes App Service + Private Endpoints
    ↓
Visualizer → Mermaid diagram
    ↓
IaC Generator → Bicep code
    ↓
Deploy to Azure → Live infrastructure
```

**From sketch to deployment in 90 minutes!** 🚀

## Wrap-Up
Congratulations! You've built a complete **multimodal AI agent pipeline** that:
- ✅ Processes text and images
- ✅ Critiques architectures
- ✅ Proposes improvements
- ✅ Generates documentation (diagrams)
- ✅ Creates deployment code (Bicep)
- ✅ Uses external knowledge (Microsoft Learn MCP)

## Next Steps
- Add error handling and retries
- Implement streaming responses (see main demo)
- Add file saving for outputs
- Create CI/CD integration
- Explore other MCP sources (GitHub, Slack)

## 📖 Detailed Learning

For a comprehensive walkthrough of this step including:
- Understanding multimodal AI and vision capabilities
- How to structure image processing pipelines
- Explanation of each code line and "why"
- Best practices for image preprocessing
- Production considerations for vision-based systems

👉 See the **[TUTORIAL.md](../../TUTORIAL.md#part-7-multimodal-input--image-processing)** file!

It covers Step 7 in detail with full explanations.
