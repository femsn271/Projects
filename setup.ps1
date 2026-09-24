# Stop the script if any command fails
$ErrorActionPreference = "Stop"

Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
python3 -m venv .venv

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
. \.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..." -ForegroundColor Cyan
python.exe -m pip install --upgrade pip

Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "Virtual environment setup and installation completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Warning: 'requirements.txt' not found in the current directory. Skipping dependency installation." -ForegroundColor Yellow
}