# Jump to project root
cd ../

# Check if the 'venv' directory does not exist
if (-Not (Test-Path "./venv")) {
    # Create the virtual environment
    python3 -m venv venv
    Write-Host "Virtual environment created."
}

# Activate the virtual environment
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated."

# Install requirements
python3 -m pip install -r requirements.txt

Write-Host ""
Write-Host "Done."