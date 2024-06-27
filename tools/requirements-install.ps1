##########################################################################
# This script installs the root requirements.txt with a clean venv:
# (1) [Re]Creates a local venv -> activates it
# (2) Installs requirements.txt
# (3) Installs requirements-dev.txt
# You can optionally just `python3 -m pip install requirements.txt` @ root
# If you want Docker support, also install `requirements-dev.txt`
##########################################################################

try {
    # Save the project root path
    $projRoot = (Get-Location).Path + "\.."

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
    Write-Host ""
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
	
    ## Create a symbolic link to sphinx_repo_manager for tooling
    #Write-Host
    #Write-Host "Creating symbolic link to sphinx_repo_manager for tooling..."
    #python3 ./symlink_to_repo_manager.py
}
catch {
    Write-Host "An error occurred. Try deleting the project root proj root 'venv' directory and run the script again."
}

Write-Host ""
Write-Host Done.
#Read-Host "Done. Press Enter to quit"
