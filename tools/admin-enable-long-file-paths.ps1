#######################################################################################################
# [RUN AS ADMIN]
# This script enables long path support on Windows and configures Git to handle long paths (>256 chars)
# 1. Enable the "LongPathsEnabled" setting in the Windows registry
# 2. Configure Git to handle long paths by setting the `core.longpaths` option to `true`
#######################################################################################################

function Enable-LongPaths {
    Write-Output "Enabling long path support in the registry..."
    $regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem"
    $regName = "LongPathsEnabled"

    if (-Not (Test-Path $regPath)) {
        Write-Output "Registry path not found: $regPath"
        exit 1
    }

    Set-ItemProperty -Path $regPath -Name $regName -Value 1 -Force
    Write-Output "Long path support has been enabled in the registry."
}

function Configure-GitLongPaths {
    Write-Output "Configuring Git to support long paths..."
    git config --global core.longpaths true

    if ($LASTEXITCODE -eq 0) {
        Write-Output "Git is now configured to support long paths."
    } else {
        Write-Output "Failed to configure Git. Ensure Git is installed and available in PATH."
    }
}


# Main
Write-Output "Starting configuration..."
Enable-LongPaths
Configure-GitLongPaths
Write-Output "All steps completed. Please restart your system for changes to take effect."
