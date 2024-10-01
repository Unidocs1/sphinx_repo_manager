##########################################################################
# This script creates a local venv if it doesn't exist and activates it.
##########################################################################

# Save the original location
$originalLocation = Get-Location

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Set-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Python Virtual Environment Activate..."
Write-Host "Project root: $projRoot"
$venvRoot = "$projRoot/venv"

# Check if the 'venv' directory exists
if (-Not (Test-Path "$venvRoot")) {
    try {
        # Create the virtual environment
        python -m venv "$venvRoot"
        Write-Host "Virtual environment created at: '$venvRoot'"
    } catch {
        Write-Host "Error: Failed to create virtual environment."
        Set-Location $originalLocation
        exit 1
    }
} else {
    Write-Host "Existing virtual environment found."
}

# Check if the activation script exists
$venvActivateScript = "$venvRoot/Scripts/Activate.ps1"
if (-Not (Test-Path $venvActivateScript)) {
    Write-Host "Error: Activation script not found at $venvActivateScript"
    Set-Location $originalLocation
    exit 1
}

try {
    # Activate the virtual environment
    & $venvActivateScript
    Write-Host "Virtual environment activated."
} catch {
    Write-Host "An error occurred during the installation of requirements."
    Set-Location $originalLocation
    exit 1
}

Write-Host "-----------------------------------"
Set-Location $originalLocation
