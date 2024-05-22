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
    Write-Host "Virtual environment created."

    # Check if the activation script exists
    $venvActivateScript = "$projRoot/venv/Scripts/Activate.ps1"
    if (-Not (Test-Path $venvActivateScript)) {
        Write-Host "Error: Activation script not found at $venvActivateScript"
        exit 1
    }

    # Activate the virtual environment
    & $venvActivateScript
    Write-Host "Virtual environment activated."

    # Install requirements
    python3 -m pip install -r "$projRoot/requirements.txt"

    Write-Host ""
    Read-Host "Done. Press Enter to quit"
} catch {
    Write-Host "An error occurred. Try deleting the project root proj root 'venv' directory and run the script again."
}
