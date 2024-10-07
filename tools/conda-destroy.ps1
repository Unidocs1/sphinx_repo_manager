##########################################################################
# This script deactivates and destroys a Conda environment named 'xbe-docs':
# (1) Checks if the 'xbe-docs' conda environment exists
#     - If it exists, deactivates and destroys it
#
# Note:
# - To ensure that the conda environment remains deactivated in your current
#   shell session, please dot-source this script:
#   . .\conda-destroy.ps1
##########################################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Conda Environment Destroy..."
$envName = "xbe-docs"

function DeactivateEnv($name) {
    conda deactivate
    Write-Host "Conda environment '$envName' deactivated."
}

function DestroyEnv($name) {
    conda env remove --name $envName -y
    Write-Host "Conda environment '$envName' destroyed."
}

try {
    conda info --envs | Select-String -Pattern "^\s*$envName\s"
    if ($?) {
        DeactivateEnv($envName)
        DestroyEnv($envName)
    } else {
        Write-Host "No conda environment called '$envName' found."
    }
} catch {
    Write-Host "Error: Failed to deactivate or destroy conda environment '$envName'."
    Pop-Location
    exit 1
}

Write-Host "-----------------------------------"
Pop-Location

