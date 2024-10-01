#############################################################
# 1. Checks if the build folder exists, runs docker-build.ps1 if not
# 2. Opens web browser to preview docs
# 3. Launches webserver container to host docs
#############################################################

# Save the original location
$originalLocation = Get-Location

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Set-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Docker Start..."

# Step 1: Check if the build folder exists
$buildPath = "${projRoot}/docs/build"
try {
    # Run docker-build.ps1 if build folder not found
    Write-Host "Build folder not found, running docker-build.ps1..." -ForegroundColor Yellow
    # Explicitly invoke PowerShell to ensure output is printed in real-time
    $process = Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File ./tools/docker-build.ps1" -PassThru -Wait -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "docker-build.ps1 failed with exit code $($process.ExitCode)."
    }
    Write-Host "Build completed successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Set-Location $originalLocation
    exit 1  # Exit with error code 1 to indicate failure
}

# Step 2: Open the page in the default web browser
try {
    Start-Process "http://localhost:8080"
    Write-Host "Opened browser to http://localhost:8080." -ForegroundColor Green
} catch {
    Write-Host "Failed to open web browser: $_" -ForegroundColor Red
    Set-Location $originalLocation
    exit 1  # Exit with error code 1 to indicate failure
}

# Step 3: Launch webserver container to preview docs
try {
    docker run --rm `
        -p 8080:80 `
        -v "${buildPath}/html:/usr/share/nginx/html:ro" `
        nginx:latest
    if ($LASTEXITCODE -ne 0) {
        throw "Docker container failed to start with exit code $LASTEXITCODE."
    }
} catch {
    Write-Host "Error running Docker container: $_" -ForegroundColor Red
    Set-Location $originalLocation
    exit 1  # Exit with error code 1 to indicate failure
}

Write-Host "-----------------------------------"
Set-Location $originalLocation
