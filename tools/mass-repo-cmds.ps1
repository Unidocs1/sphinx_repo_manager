# mass-repo-cmds.ps1
$REPOS_AVAIL_DIR = "../source/_repos-available/"
$startingDir = Get-Location
pwd
$FAIL_ON_ITERATION = $true

function Start-RepoCmds {
    param (
        [string]$dirPath
    )

    Set-Location $dirPath
	
    Write-Output ""
    Write-Output "-------------------------------"
	Write-Output "@ Repo: '${dirPath}'"
    
	# >> Custom Cmds >>
    Write-Output "*TEST CMD"
	# << Custom Cmds <<
	
    Write-Output ""
}

function Iterate-Dirs {
    $directories = Get-ChildItem -Directory
    pwd

    foreach ($dir in $directories) {
        try {
            # Navigate to the directory
            Set-Location $dir.FullName

            # Check if the directory is a Git repository
            if (Test-Path ".git") {
                # Execute commands for the Git repository
                Start-RepoCmds -dirPath $dir.FullName
            }
        }
        catch {
            Write-Error "Error processing directory '$($dir.FullName)': $_"
            if ($FAIL_ON_ITERATION) {
                throw
            }
        }
        finally {
            # Return to the previous directory
            Set-Location ..
        }
    }
}

function Main {
    try {
        # Change to the target directory
        Set-Location $REPOS_AVAIL_DIR
        pwd

        # Iterate over directories and execute commands
        Iterate-Dirs
    }
    catch {
        Write-Error "An error occurred in the Main function: $_"
        if ($FAIL_ON_ITERATION) {
            throw
        }
    }
}

# Execute the main function with error handling
try {
    Main
}
catch {
    Write-Error "An unexpected error occurred: $_"
}
finally {
    # Return to the original working directory
    Set-Location $startingDir
	
	Write-Output ""
	Write-Output "Done."
}
