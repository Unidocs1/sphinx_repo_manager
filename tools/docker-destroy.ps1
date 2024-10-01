#############################################################
# 1. Clears local docker images and containers
# 2. Clears docs folder of all unversioned files
#############################################################

# Save the original location
$originalLocation = Get-Location

# Get the location of the current script file and project root
$scriptFile = $MyInvocation.MyCommand.Path
$fileLocation = Split-Path -Path $scriptFile
$projRoot = (Resolve-Path -Path "$fileLocation/..").ProviderPath
Set-Location $projRoot

Write-Host "-----------------------------------"
Write-Host "Docker Destroy..."

# Step 1: Build docker images and clear images, orphans
try {
    Write-Host "Clearing local Docker images and orphan containers..." -ForegroundColor Yellow
    # Run docker compose to remove images and orphans
    $process = Start-Process docker -ArgumentList "compose -f ./docker/docker-compose.base.yaml -f ./docker/docker-compose.main.yaml down --rmi local --remove-orphans" -PassThru -Wait -NoNewWindow
    if ($process.ExitCode -ne 0) {
        throw "docker compose down command failed with exit code $($process.ExitCode)."
    }
    Write-Host "Docker cleanup finished successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Set-Location $originalLocation
    exit 1  # Exit with error code 1 to indicate failure
}

# Step 2: Clear docs folder of all unversioned files
$process = Start-Process powershell -ArgumentList " -NoProfile -ExecutionPolicy Bypass -File ./tools/clean-cache.ps1" -PassThru -Wait -NoNewWindow
# try {
#     # Explicitly run docker-clean.ps1 and capture its output
    
#     if ($process.ExitCode -ne 0) {
#         throw "docker-clean.ps1 failed with exit code $($process.ExitCode)."
#     }
# } catch {
#     Write-Host "Error: $_" -ForegroundColor Red
#     exit 1  # Exit with error code 1 to indicate failure
# }

Set-Location $originalLocation
