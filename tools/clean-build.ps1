#############################################################
# 1. Clears unversioned files from build folder
#############################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Clean Build..."

# Step 1: Clear unversioned files from the build folder
try {
    Write-Host "Clearing unversioned files from ./docs/build..." -ForegroundColor Yellow
    # Run git clean for build folder
    $process = Start-Process git -ArgumentList "clean", "-Xffd", "./docs/build" -PassThru -Wait -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "git clean failed for ./docs/build with exit code $($process.ExitCode)."
    }
    Write-Host "Unversioned files from ./docs/build cleared successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Pop-Location
    exit 1  # Exit with error code 1 to indicate failure
}

Write-Host "-----------------------------------"
Pop-Location
