##########################################################################
# This script sets up a Conda environment named 'docs' with Python 3.10:
# (1) Checks if the 'docs' conda environment exists
#     - If not, creates it with Python 3.10
# (2) Activates the 'docs' conda environment
#
# Note:
# - To ensure that the conda environment remains activated in your current
#   shell session, please dot-source this script:
#   . .\conda-activate.ps1
##########################################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot


$envName = "sphinx-repo-mgr"
$pythonVersion = "3.10"

Write-Host "-----------------------------------"
Write-Host "Conda Environment Activate..."
Write-Host "Conda environment: $envName"
Write-Host "Python version: $pythonVersion"

function CreateEnv($name) {
    conda env create --name $envName --file environment.yml -y
    Write-Host "Conda environment '$envName' created with Python $pythonVersion."
}

function ActivateEnv($name) {
    conda activate $envName
    Write-Host "Conda environment '$envName' activated."
}

try {
    ActivateEnv($envName)
} catch {
    Write-Host "No conda environment called '$envName' found, creating..."
    try {
        CreateEnv($envName)
        ActivateEnv($envName)
    } catch {
        Write-Host "Error: Failed to create conda environment '$envName'."
        Pop-Location
        exit 1
    }
}

Write-Host "-----------------------------------"
Pop-Location
