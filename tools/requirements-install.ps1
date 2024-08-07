##########################################################################
# This script installs the root requirements.txt with a clean venv:
# (1) [Re]Creates a local venv -> activates it
# (2) Installs requirements.txt
# (3) Installs requirements-dev.txt
# You can optionally just `python3 -m pip install requirements.txt` @ root
# If you want Docker support, also install `requirements-dev.txt`
##########################################################################

try {
	# Save the original location
	$originalLocation = Get-Location

	# Normalize the project root path
	$projRoot = Join-Path -Path $originalLocation.Path -ChildPath ".."
	$projRoot = (Resolve-Path -Path $projRoot).ProviderPath

    # Check if the 'venv' directory exists
    if (Test-Path "$projRoot/venv") {
        # Remove the existing 'venv' directory
        Remove-Item -Recurse -Force "$projRoot/venv"
        Write-Host "Existing virtual environment removed."
    }

    # Create the virtual environment
    python3 -m venv "$projRoot/venv"
    Write-Host "Virtual environment created at: '$projRoot/venv'"

    # Check if the activation script exists
    $venvActivateScript = "$projRoot/venv/Scripts/Activate.ps1"
    if (-Not (Test-Path $venvActivateScript)) {
        Write-Host "Error: Activation script not found at $venvActivateScript"
        exit 1
    }

    # Activate the virtual environment
    & $venvActivateScript
    Write-Host "Virtual environment activated."
    Write-Host ""

    # Install requirements
    Write-Host "Installing core requirements from '$projRoot/requirements.txt' ..."
    Write-Host ""
    Write-Host "-----------------------------------"
    python3 -m pip install -r "$projRoot/requirements.txt"
	
	# Install requirements-dev
    Write-Host ""
    Write-Host "Installing dev requirements from '$projRoot/requirements-dev.txt' ..."
    Write-Host ""
    Write-Host "-----------------------------------"
    python3 -m pip install -r "$projRoot/requirements-dev.txt"
}
catch {
    Write-Host "An error occurred. Try deleting the project root proj root 'venv' directory and run the script again."
}

Set-Location $originalLocation
Write-Host ""
Write-Host Done.
