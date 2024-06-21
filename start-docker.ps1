docker compose -f ./docker/docker-compose.yaml up --build
docker compose -f ./docker/docker-compose.yaml down

$index = "./docs/build/html/index.html"
Write-Output "Launching '${index}'"
Start-Process $index
