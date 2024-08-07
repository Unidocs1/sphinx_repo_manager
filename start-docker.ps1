#############################################################
# 1. Starts Docker
# 2. Launches index.html (comment this out if you !want)
# 3. Stops Docker
# --------------------------------
# (!) As an alternative to Docker:
# 1. Run tools/requirements-install.ps1
# 2. Run docs/make.bat
#############################################################
docker compose -f ./docker/docker-compose.yaml up --build
docker compose -f ./docker/docker-compose.yaml down

$index = "./docs/build/html/index.html"
Write-Output "Launching '${index}'"
Start-Process $index

Write-Output "Stopping Docker..."
docker compose -f ./docker/docker-compose.yaml down

Write-Host "Press any key to quit (when done reviewing logs)"
[void][System.Console]::ReadKey($true)
