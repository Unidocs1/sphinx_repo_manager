##########################################################################
# This script deactivates the venv if active, then destroys it.
##########################################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Python Virtual Environment Destroy..."
Write-Host "Project root: $projRoot"
$venvRoot = "xbe-venv"

# Check if the 'venv' directory exists
if (Test-Path "$venvRoot") {
    # Check if the virtual environment is active
    if ($env:VIRTUAL_ENV) {
        Write-Host "Deactivating virtual environment..."
        & "$env:VIRTUAL_ENV/Scripts/deactivate.ps1"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to deactivate virtual environment."
            Pop-Location
            exit 1
        }
        Write-Host "Virtual environment deactivated."
    }

    try {
        # Remove the virtual environment
        Remove-Item -Recurse -Force "$venvRoot"
        Write-Host "Virtual environment destroyed at: '$venvRoot'"
    } catch {
        Write-Host "Error: Failed to destroy virtual environment."
        Pop-Location
        exit 1
    }
} else {
    Write-Host "No virtual environment found at: '$venvRoot'"
}

Write-Host "-----------------------------------"
Pop-Location
