# Test script to upload a PDF to the NyayMitra API
$uri = "http://localhost:5000/analyze"
$filePath = "d:\New folder\nyaymitra\sample_contracts\sample_contract.pdf"

Write-Host "Testing file upload to NyayMitra API..."
Write-Host "File: $filePath"
Write-Host "Endpoint: $uri"

# Create form data
$form = @{
    file = Get-Item -Path $filePath
}

try {
    Write-Host "Uploading file..."
    $response = Invoke-RestMethod -Uri $uri -Method Post -Form $form
    Write-Host "✅ Upload successful!"
    Write-Host "Response:"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "❌ Upload failed:"
    Write-Host $_.Exception.Message
}
