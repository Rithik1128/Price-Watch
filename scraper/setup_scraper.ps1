<#
.SYNOPSIS
Sets up the Python virtual environment and installs scraper dependencies.
.PARAMETER venvPath
Path to create or use the Python virtual environment (default ".\.venv").
.EXAMPLE
PS> .\setup_scraper.ps1
#>
param(
    [string]$venvPath = ".\\.venv"
)

# Navigate to script directory
Set-Location $PSScriptRoot

# Create or reuse venv
if (!(Test-Path $venvPath)) {
    Write-Host "Creating virtual environment at $venvPath"
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

# Activate venv
Write-Host "Activating virtual environment"
& "$venvPath\Scripts\Activate.ps1"

# Upgrade pip, setuptools, wheel
Write-Host "Upgrading pip, setuptools, wheel"
python -m pip install --upgrade pip setuptools wheel

# Install requirements
Write-Host "Installing requirements from requirements.txt"
pip install -r ..\requirements.txt

Write-Host "Setup complete. To run the scraper: python reliance-scraper.py"
