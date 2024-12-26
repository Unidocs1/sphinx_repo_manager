#####################################################################
# tools/common.ps1
# Shared utils for script working directory and cleanup
#####################################################################

# Store the initial working directory (only once when this script is loaded)
$global:InitialWorkingDir = Get-Location

function Set-WorkingDirectory {
    $ScriptDir = $PSScriptRoot
    if (-not $ScriptDir) {
        Write-Host "Error: Unable to determine script directory." -ForegroundColor Red
        exit 1
    }

    $WorkingDir = Split-Path -Parent $ScriptDir
    Set-Location -Path $WorkingDir
    Write-Host "Set working dir to $WorkingDir"
    return $WorkingDir
}

function Restore-WorkingDirectory {
    Set-Location -Path $global:InitialWorkingDir
}
