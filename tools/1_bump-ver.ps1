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

function Bump-Git-Toml-Version {
    param([string]$BumpType)

    Write-Host "`nBumping Git version ($BumpType)..." -ForegroundColor Yellow
    $BumpCfg = (Resolve-Path -Path (Join-Path -Path $PSScriptRoot -ChildPath "../.bumpversion.cfg")).Path
    bump2version $BumpType --config-file $BumpCfg
	
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Git version bump failed. Exiting." -ForegroundColor Red
        Restore-WorkingDirectory
        exit $LASTEXITCODE
    }

    Write-Host "Git version bumped successfully." -ForegroundColor Green
}

# Main workflow
try {
    Set-WorkingDirectory
    Bump-Git-Toml-Version -BumpType $BumpType
} finally {
    Restore-WorkingDirectory
}
