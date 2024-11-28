#####################################################################
# tools/3a_deploy-to-test.ps1
# PREREQS: 
# - pip install -r ../requirements-dev.txt
# - Ensure ../dist/ exists
# - Ensure .env PYPI_TEST_API_KEY
#####################################################################

# Import common functions
. $PSScriptRoot\common.ps1

$PYPI_DEPLOYMENT_URL = "https://test.pypi.org/legacy/"

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
            Restore-WorkingDirectory
            exit 1
        }
        return $ApiKey
    }
}

function Deploy-To-TestPyPI {
    param([string]$ApiKey)

    Write-Host "`nDeploying to Test PyPI @ $PYPI_DEPLOYMENT_URL..." -ForegroundColor Yellow
    twine upload --repository-url $PYPI_DEPLOYMENT_URL -u __token__ -p $ApiKey dist/*
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Deployment to Test PyPI was successful!" -ForegroundColor Green
    } else {
        Write-Host "Error: Deployment to Test PyPI failed. Exiting." -ForegroundColor Red
        Restore-WorkingDirectory
        exit $LASTEXITCODE
    }
}

# Main workflow
try {
    Set-WorkingDirectory
    $ApiKey = Get-ApiKey -KeyName "PYPI_TEST_API_KEY"
    Deploy-To-TestPyPI -ApiKey $ApiKey
} finally {
    Restore-WorkingDirectory
}
