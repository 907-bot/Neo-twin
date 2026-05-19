# ============================================================
#  NeoTwin -- Deploy Backend to HuggingFace Spaces
#  Run from: D:\3D-Deeplearning
#  Usage:    .\deploy_to_hf.ps1
# ============================================================

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "NeoTwin Backend -- HuggingFace Spaces Deploy" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow

# -- Step 1: Copy backend files into the cloned HF Space --
Write-Host ""
Write-Host "[1/4] Copying backend files to neotwin-api/..." -ForegroundColor Cyan

$backendPath  = (Resolve-Path "backend").Path
$hfSpacePath  = (Resolve-Path "neotwin-api").Path
$excludeNames = @("venv", "__pycache__", ".env", "*.pyc", "*.pth", "*.ckpt")

Get-ChildItem -Path $backendPath -Recurse | ForEach-Object {
    $skip = $false
    foreach ($ex in $excludeNames) {
        if ($_.FullName -like "*\$ex" -or $_.FullName -like "*\$ex\*") {
            $skip = $true
            break
        }
    }
    if (-not $skip) {
        $dest = $_.FullName.Replace($backendPath, $hfSpacePath)
        if ($_.PSIsContainer) {
            New-Item -ItemType Directory -Path $dest -Force | Out-Null
        } else {
            Copy-Item -Path $_.FullName -Destination $dest -Force
        }
    }
}

Write-Host "   OK - Files copied." -ForegroundColor Green

# -- Step 2: Write .gitignore inside the HF Space --
Write-Host ""
Write-Host "[2/4] Writing .gitignore for HF Space..." -ForegroundColor Cyan

$gitignoreContent = "venv/`n__pycache__/`n*.pyc`n.env`n*.pth`n*.ckpt`ndata/`noutput/"
Set-Content -Path "neotwin-api\.gitignore" -Value $gitignoreContent -Encoding UTF8

Write-Host "   OK - .gitignore written." -ForegroundColor Green

# -- Step 3: Git commit inside the HF Space clone --
Write-Host ""
Write-Host "[3/4] Committing changes..." -ForegroundColor Cyan

Push-Location "neotwin-api"

git add .
$status = git status --short
if ($status) {
    git commit -m "deploy: NeoTwin backend v1.0 - FastAPI + Gemini AI"
    Write-Host "   OK - Committed." -ForegroundColor Green
} else {
    Write-Host "   INFO - Nothing new to commit." -ForegroundColor Gray
}

# -- Step 4: Push to HuggingFace Spaces --
Write-Host ""
Write-Host "[4/4] Pushing to HuggingFace Spaces..." -ForegroundColor Cyan
git push
Write-Host "   OK - Push complete!" -ForegroundColor Green

Pop-Location

Write-Host ""
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host "DONE! Backend deployed." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Visit: https://huggingface.co/spaces/1qwsd/neotwin-api" -ForegroundColor White
Write-Host "  2. Wait 2-3 min for Docker build" -ForegroundColor White
Write-Host "  3. Settings -> Variables and Secrets -> add:" -ForegroundColor White
Write-Host "       GEMINI_API_KEY    = your_key" -ForegroundColor Gray
Write-Host "       HUGGINGFACE_TOKEN = your_token" -ForegroundColor Gray
Write-Host "       ALLOWED_ORIGINS   = *" -ForegroundColor Gray
Write-Host "  4. API Docs: https://1qwsd-neotwin-api.hf.space/docs" -ForegroundColor White
Write-Host ""
