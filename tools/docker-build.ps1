#############################################################
# 1. Delete build folder if found
# 2. Runs docker-compose to build the HTML
#############################################################

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Push-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Docker Build..."

# Step 1: Check if the build folder exists
$buildPath = "${projRoot}/docs/build"
try {
    if (Test-Path $buildPath) {
        $process = Start-Process powershell -ArgumentList " -NoProfile -ExecutionPolicy Bypass -File ./tools/clean-build.ps1" -PassThru -Wait -NoNewWindow
        if ($process.ExitCode -ne 0) {
            throw "git clean failed with exit code $($process.ExitCode)."
        }
        Write-Host "Build folder deleted successfully." -ForegroundColor Green
    } else {
        Write-Host "Build folder not found, skipping deletion." -ForegroundColor Green
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Pop-Location
    exit 1  # Exit with error code 1 to indicate failure
}

# Step 2: Build HTML to build folder using docker-compose
try {
    Write-Host "Building HTML to the build folder using docker-compose..." -ForegroundColor Yellow
    # Run docker compose to build the HTML
    $process = Start-Process docker -ArgumentList "compose -f ./docker/docker-compose.main.yaml run --rm main" -PassThru -Wait -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "docker compose failed with exit code $($process.ExitCode)."
    }
    Write-Host "HTML build completed successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Pop-Location
    exit 1  # Exit with error code 1 to indicate failure
}

Write-Host "-----------------------------------"
Pop-Location
