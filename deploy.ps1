# NyayMitra Serverless Deployment Script
# This script deploys the serverless backend to Vercel

Write-Host "🚀 NyayMitra Serverless Deployment" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    $vercelVersion = vercel --version
    Write-Host "✅ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
}

# Check if .env file exists
if (Test-Path ".env") {
    Write-Host "✅ Environment file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  No .env file found. Please create one from .env.example" -ForegroundColor Yellow
    Write-Host "   Copy .env.example to .env and fill in your API keys" -ForegroundColor Yellow
}

# Check if API directory exists
if (Test-Path "api") {
    Write-Host "✅ API directory found" -ForegroundColor Green
    $apiFiles = Get-ChildItem -Path "api" -Filter "*.py" | Measure-Object
    Write-Host "   Found $($apiFiles.Count) serverless functions" -ForegroundColor Cyan
} else {
    Write-Host "❌ API directory not found!" -ForegroundColor Red
    exit 1
}

# Ask for deployment type
Write-Host ""
Write-Host "Select deployment type:" -ForegroundColor Yellow
Write-Host "1. Preview deployment (for testing)" -ForegroundColor Cyan
Write-Host "2. Production deployment" -ForegroundColor Cyan
Write-Host "3. Local development server" -ForegroundColor Cyan

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "🔄 Deploying to preview environment..." -ForegroundColor Cyan
        vercel
    }
    "2" {
        Write-Host "🔄 Deploying to production..." -ForegroundColor Cyan
        vercel --prod
    }
    "3" {
        Write-Host "🔄 Starting local development server..." -ForegroundColor Cyan
        Write-Host "   API will be available at: http://localhost:3000/api" -ForegroundColor Green
        Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
        vercel dev
    }
    default {
        Write-Host "❌ Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update frontend API_BASE_URL in src/api.js" -ForegroundColor Cyan
Write-Host "2. Test the deployment using test_serverless.py" -ForegroundColor Cyan
Write-Host "3. Configure environment variables in Vercel dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  vercel logs          - View function logs" -ForegroundColor Cyan
Write-Host "  vercel env ls        - List environment variables" -ForegroundColor Cyan
Write-Host "  vercel domains       - Manage custom domains" -ForegroundColor Cyan
Write-Host "  python test_serverless.py - Test all endpoints" -ForegroundColor Cyan
