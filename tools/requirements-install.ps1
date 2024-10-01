##########################################################################
# This script installs the root requirements.txt with a clean venv:
# (1) [Re]Creates a local venv -> activates it
# (2) Installs requirements.txt
# (3) Installs requirements-dev.txt
# You can optionally just `python3 -m pip install requirements.txt` @ root
# If you want Docker support, also install `requirements-dev.txt`
##########################################################################

# Save the original location
$originalLocation = Get-Location

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Write-Host "-----------------------------------"
Write-Host "Project root: $projRoot"

try {
    # $requirements = "${projRoot}/docs/requirements.txt"
    # $requirements  = (Resolve-Path -Path $requirements).ProviderPath
    # Write-Host "Installing core requirements from '$requirements' ..."
    Set-Location $projRoot/docs
    make install
}
catch {
    Write-Host "An error occurred. "
}

Write-Host "-----------------------------------"
Set-Location $originalLocation
Write-Host ""
Write-Host Done.
