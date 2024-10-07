#############################################################
# 1. Clears unversioned files from build and source folders
#############################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Clean Cache..."

# Step 1: Clear unversioned files from the docs folder
try {
    Write-Host "Clearing unversioned files from ./docs..." -ForegroundColor Yellow
    # Run git clean for source folder
    $process = Start-Process git -ArgumentList "clean", "-Xffd", "./docs" -PassThru -Wait -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "git clean failed for ./docs with exit code $($process.ExitCode)."
    }
    Write-Host "Unversioned files from ./docs cleared successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Pop-Location
    exit 1  # Exit with error code 1 to indicate failure
}

Write-Host "-----------------------------------"
Pop-Location
