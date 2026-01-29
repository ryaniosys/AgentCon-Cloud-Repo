# Example Architecture Diagrams

This directory contains sample architecture diagrams you can use to test the image recognition feature.

## How to Use

1. **Save a diagram** to this directory (PNG, JPG, or JPEG format)

2. **Update `.env`**:
   ```bash
   USE_IMAGE_MODE=true
   ARCHITECTURE_IMAGE_PATH=examples/your-diagram.png
   ```

3. **Run the demo**:
   ```powershell
   python agentcon_demo.py
   ```

## Where to Find Architecture Diagrams

### 1. Azure Architecture Center
**URL**: https://learn.microsoft.com/azure/architecture/browse/

Best for:
- Reference architectures
- Real-world patterns
- Production-quality diagrams

Example types:
- N-tier applications
- Microservices architectures
- Data analytics pipelines
- AI/ML workflows

### 2. Your Organization's Diagrams
- Export from Visio (File → Export → PNG)
- Export from draw.io (File → Export as → PNG)
- Screenshot from PowerPoint presentations
- Export from Lucidchart

### 3. Create Your Own
Use any tool to create a simple architecture diagram:
- **draw.io** (free, web-based)
- **Visio** (Microsoft)
- **Lucidchart** (web-based)
- **PowerPoint** (shapes + arrows)
- **Excalidraw** (hand-drawn style)

## Tips for Best Results

### ✅ Good Diagram Characteristics

1. **Clear Labels**
   - Service names visible (e.g., "Azure App Service", "SQL Database")
   - Component types labeled
   - Resource names shown

2. **Visible Connections**
   - Arrows showing data flow
   - Connection types labeled (HTTP, SQL, etc.)
   - Public vs private zones clearly marked

3. **Standard Icons**
   - Use Azure official icons when possible
   - Consistent icon style
   - Icons large enough to be recognized

4. **Good Contrast**
   - Light background, dark text
   - High-resolution (at least 800x600)
   - Not too cluttered

### ❌ Avoid

- Hand-drawn sketches (unless very clear)
- Low-resolution images (< 400px)
- Complex diagrams with 20+ services (start simple)
- Diagrams with no labels
- Watermarked or copyrighted images

## Example Scenarios to Test

### 1. Flawed 3-Tier Architecture
Create or find a diagram showing:
- VMs with public IPs (security issue)
- SQL Database with public endpoint (issue)
- No load balancer (scalability issue)

**Expected**: Agents will identify all issues and propose improvements

### 2. Legacy AWS Architecture
Find an AWS architecture diagram with:
- EC2 instances
- RDS database
- S3 buckets

**Expected**: Agents will suggest Azure equivalents (App Service, Azure SQL, Blob Storage)

### 3. Serverless Architecture
Diagram with:
- API Gateway / Front Door
- Function Apps / Lambda
- CosmosDB / DynamoDB

**Expected**: Agents will validate best practices for serverless

## Sample Diagram Structure (ASCII)

```
┌─────────────────────────────────────────────┐
│  Internet (Public Zone)                     │
└──────────────┬──────────────────────────────┘
               │
       ┌───────▼────────┐
       │ Load Balancer  │
       │  (Public IP)   │
       └───────┬────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐          ┌────▼───┐
│  VM 1  │          │  VM 2  │  ← Issue: Should be App Service
│Node.js │          │Node.js │
└───┬────┘          └────┬───┘
    │                    │
    └──────────┬─────────┘
               │
        ┌──────▼─────┐
        │ Azure SQL  │  ← Issue: Public endpoint
        │  Database  │
        └────────────┘
```

## Testing Checklist

- [ ] Text mode works (default demo)
- [ ] Image from URL works
- [ ] Local image file works
- [ ] Diagram with clear labels recognized
- [ ] Agents cite Microsoft Learn sources
- [ ] Issues correctly identified
- [ ] Improvements make sense
- [ ] Bicep code validates resource types

## Need Help?

See [README.md](../README.md) for:
- Full documentation
- Troubleshooting guide
- Advanced configuration
- Azure OpenAI setup
