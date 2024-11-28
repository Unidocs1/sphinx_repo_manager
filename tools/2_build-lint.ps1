#####################################################################
# tools/2_build-lint.ps1
# PREREQS: pip install -r ../requirements-dev.txt
#####################################################################

# Import common functions
. $PSScriptRoot\common.ps1

function Clean-DistDirectory {
    $DistDir = Join-Path -Path (Get-Location) -ChildPath "dist"
    if (Test-Path -Path $DistDir) {
        Write-Host "`nCleaning 'dist' directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force -Path $DistDir
        Write-Host "'dist' directory removed."
    } else {
        Write-Host "'dist' directory does not exist. Skipping."
    }
}

function Build-Package {
    Write-Host "`nBuilding the Python package..." -ForegroundColor Yellow
    python -m build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Build failed. Exiting." -ForegroundColor Red
        Restore-WorkingDirectory
        exit $LASTEXITCODE
    }
    Write-Host "Package built successfully." -ForegroundColor Green
}

function Lint-With-Twine {
    Write-Host "`nChecking distribution files with Twine..." -ForegroundColor Yellow
    twine check dist/*
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Twine check failed. Exiting." -ForegroundColor Red
        Restore-WorkingDirectory
        exit $LASTEXITCODE
    }
    Write-Host "Twine check passed successfully.`n" -ForegroundColor Green
}

# Main workflow
try {
    Set-WorkingDirectory
    Clean-DistDirectory
    Build-Package
    Lint-With-Twine
} finally {
    Restore-WorkingDirectory
}
