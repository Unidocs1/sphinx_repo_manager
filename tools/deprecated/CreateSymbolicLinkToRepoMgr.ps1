Function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

If (-Not (Test-Admin)) {
    Write-Warning "Restarting script with elevated permissions..."
    Start-Process pwsh "-File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

try {
    # Navigate to the directory where you want to create the symbolic link
    Set-Location -Path "D:\repos\xsolla\acceleratxr.io\tools"

    # Define the relative target path
    $targetPath = "..\source\_extensions\repo_manager"

    # Create the symbolic link using relative paths
    New-Item -ItemType SymbolicLink -Path "repo_manager" -Target $targetPath -Force

    # Verify the symbolic link
    Get-Item -Path "repo_manager"

    # Success message
    Write-Host "Symbolic link created successfully."
} catch {
    # Error message
    Write-Host "An error occurred: $_"
} finally {
    # Prompt to press Enter to quit
    Read-Host "Done. Press Enter to quit"
}
