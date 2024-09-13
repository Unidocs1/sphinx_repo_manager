#############################################################
# 1. Starts Docker
# 2. Launches index.html (comment this out if you !want)
# 3. Stops Docker
# --------------------------------
# (!) Legacy alternative to Docker:
# 1. Install Python 3.10
# 2. Run tools/requirements-install.ps1
# 3. Run docs/make.bat
#############################################################

# --abort-on-container-exit is for 1-shot Docker builds like our purpose of sphinx-building
docker compose -f ./docker/docker-compose.yaml build
$dockerExitCode = docker compose -f ./docker/docker-compose-preview.yaml up --build; $LASTEXITCODE

if ($dockerExitCode -eq 0) {
    $index = "./docs/build/html/index.html"
    Write-Output "Launching '${index}'"
    Start-Process $index
} else {
    Write-Output "Docker encountered an error, not launching index.html"
}

#Write-Output "Stopping Docker and cleaning up (comment this out for speedier iterations at the cost of storage)..."
#docker compose -f ./docker/docker-compose.yaml down

Write-Host "Press any key to quit (when done reviewing logs)"
[void][System.Console]::ReadKey($true)
