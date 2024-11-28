#####################################################################
# tools/3b_deploy-to-prod.ps1
# PREREQS: 
# - pip install -r ../requirements-dev.tx
# - Ensure ../dist/ exists
# - Ensure .env PYPI_PROD_API_KEY
#####################################################################

$PYPI_DEPLOYMENT_URL = "https://upload.pypi.org/legacy/"

function Get-ApiKey {
    param([string]$KeyName)
    $EnvFile = Join-Path -Path $PSScriptRoot -ChildPath ".env"
    if (Test-Path -Path $EnvFile) {
        Write-Host "`nLoading environment variables from .env..." -ForegroundColor Yellow
        Get-Content $EnvFile | ForEach-Object {
            if ($_ -match "^\s*(\w+)\s*=\s*(.+?)\s*$") {
                $name = $matches[1]
                $value = $matches[2]
                Set-Item -Path "env:$name" -Value $value
            }
        }
    } else {
        Write-Host ".env file not found. Skipping environment variable loading."
    }

    $EnvVariable = Get-Item -Path "env:$KeyName" -ErrorAction SilentlyContinue
    if ($EnvVariable) {
        Write-Host "Using $KeyName from environment."
        return $EnvVariable.Value
    } else {
        $ApiKey = Read-Host -Prompt "Enter your $KeyName"
        if (-not $ApiKey) {
            Write-Host "$KeyName is required. Exiting." -ForegroundColor Red
            exit 1
        }
        return $ApiKey
    }
}

function Deploy-To-PyPi {
    param([string]$ApiKey)
    Write-Host "`nDeploying to Production PyPI..." -ForegroundColor Yellow
    twine upload --repository-url $PYPI_DEPLOYMENT_URL -u __token__ -p $ApiKey dist/*
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Deployment to Production PyPI was successful!" -ForegroundColor Green
    } else {
        Write-Host "Error: Deployment to Production PyPI failed. Exiting." -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# Main workflow
$ApiKey = Get-ApiKey -KeyName "PYPI_PROD_API_KEY"
Deploy-To-PyPi -ApiKey $ApiKey
