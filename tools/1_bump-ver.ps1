#####################################################################
# tools/1_bump-ver.ps1
# PREREQS: 
# - pip install -r ../requirements-dev.txt
# - Clean git working dir
# OPTIONAL ARG: {bump_type}
# - Accepts: patch (default), minor, major
#####################################################################

# Import common functions
. $PSScriptRoot\common.ps1

# Capture arguments (supports positional or default)
$BumpType = if ($args[0]) { $args[0] } else { "patch" }

function Bump-Version {
    param([string]$BumpType)

    Write-Host "`nBumping version ($BumpType)..." -ForegroundColor Yellow
    bump2version $BumpType
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Version bump failed. Exiting." -ForegroundColor Red
        Restore-WorkingDirectory
        exit $LASTEXITCODE
    }

    Write-Host "Version bumped successfully." -ForegroundColor Green
}

# Main workflow
try {
    Set-WorkingDirectory
    Bump-Version -BumpType $BumpType
} finally {
    Restore-WorkingDirectory
}
