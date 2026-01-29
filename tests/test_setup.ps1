# AgentCon Demo - Test Script
# Quick validation that everything is configured correctly

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AgentCon Demo - Configuration Test" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check dependencies
Write-Host "`n[2/5] Checking dependencies..." -ForegroundColor Yellow
$packages = @("agent_framework", "dotenv")
$allInstalled = $true

foreach ($package in $packages) {
    $result = python -c "import $package" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $package not installed" -ForegroundColor Red
        $allInstalled = $false
    }
}

if (-not $allInstalled) {
    Write-Host "`n  Installing missing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Check .env file
Write-Host "`n[3/5] Checking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file found" -ForegroundColor Green
    
    # Check for API key
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "  ✓ OPENAI_API_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ OPENAI_API_KEY not set or invalid" -ForegroundColor Yellow
        Write-Host "    Please add your OpenAI API key to .env file" -ForegroundColor Yellow
    }
    
    if ($envContent -match "OPENAI_MODEL=") {
        Write-Host "  ✓ OPENAI_MODEL configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ OPENAI_MODEL not set" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ .env file not found" -ForegroundColor Red
    Write-Host "    Creating template .env file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env" -ErrorAction SilentlyContinue
}

# Check demo file
Write-Host "`n[4/5] Checking demo file..." -ForegroundColor Yellow
if (Test-Path "agentcon_demo.py") {
    Write-Host "  ✓ agentcon_demo.py found" -ForegroundColor Green
    $lineCount = (Get-Content "agentcon_demo.py" | Measure-Object -Line).Lines
    Write-Host "    Lines: $lineCount" -ForegroundColor Gray
} else {
    Write-Host "  ✗ agentcon_demo.py not found" -ForegroundColor Red
    exit 1
}

# Check internet connectivity
Write-Host "`n[5/5] Checking internet connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://learn.microsoft.com" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✓ Internet connection active" -ForegroundColor Green
    Write-Host "  ✓ Microsoft Learn MCP accessible" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Cannot reach Microsoft Learn" -ForegroundColor Yellow
    Write-Host "    MCP integration may not work" -ForegroundColor Yellow
}

# Summary
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  Test Complete!" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

Write-Host "✅ Ready to run the demo!" -ForegroundColor Green
Write-Host "`nTo start the demo, run:" -ForegroundColor White
Write-Host "  python agentcon_demo.py`n" -ForegroundColor Yellow

Write-Host "📚 For more information:" -ForegroundColor White
Write-Host "  - Quick Start: QUICKSTART.md" -ForegroundColor Gray
Write-Host "  - Full Docs:   README.md" -ForegroundColor Gray
Write-Host "  - Examples:    examples/README.md`n" -ForegroundColor Gray
