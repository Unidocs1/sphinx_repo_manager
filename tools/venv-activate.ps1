##########################################################################
# This script creates a local venv if it doesn't exist and activates it.
##########################################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Python Virtual Environment Activate..."
Write-Host "Project root: $projRoot"
$venvRoot = "xbe-venv"

# Check if the 'venv' directory exists
if (-Not (Test-Path "$venvRoot")) {
    try {
        # Create the virtual environment
        python -m venv "$venvRoot"
        Write-Host "Virtual environment created at: '$venvRoot'"
    } catch {
        Write-Host "Error: Failed to create virtual environment."
        Pop-Location
        exit 1
    }
} else {
    Write-Host "Existing virtual environment found."
}

# Check if the activation script exists
$venvActivateScript = "$venvRoot/Scripts/Activate.ps1"
if (-Not (Test-Path $venvActivateScript)) {
    Write-Host "Error: Activation script not found at $venvActivateScript"
    Pop-Location
    exit 1
}

try {
    # Activate the virtual environment
    & $venvActivateScript
    Write-Host "Virtual environment activated."
} catch {
    Write-Host "An error occurred during the installation of requirements."
    Pop-Location
    exit 1
}

Write-Host "-----------------------------------"
Pop-Location
