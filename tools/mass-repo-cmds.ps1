# ---------------------------------------------------------------------
# mass-repo-cmds.ps1
#
# 1. Ensure the $REPOS_AVAIL_DIR matches your root repos dir
# 2. Write your custom per-repo cmds at the `Run-CustomCmds` function
#
# 💡It's ok if your repos are nested (!flat); we'll look for .git dirs
# ---------------------------------------------------------------------
$REPOS_AVAIL_DIR = "../docs/source/_repos-available"
$STARTING_DIR = Get-Location
$DRY_RUN_ON_1ST_AVAIL_REPO = $false  # Test this script on the 1st alphabetically-available repo
$FAIL_ON_1ST_ERR = $true
$MASTER_MAIN_BRANCH_PROTECTION = $true  # Fail on master || main branch

# RUN YOUR CUSTOM COMMANDS HERE (or leave empty for dry run) >>
function Run-CustomCmds {
	## TEMPLATE EXAMPLES >>
	#Copy-FileToRepo
	#Append-Readme
	#Run-GitAddCommitPullPush
}

## TEMPLATE EXAMPLES ############################################################
function Run-GitAddCommitPullPush {
	#git add .
    #git commit -m "docs(legal): Add LICENSE.md EULA" -m "[XBND-1214]"
    #git pull
    #git push
}

function Copy-FileToRepo {
    $fileName = "LICENSE.md"
    $srcFilePath = Join-Path $PSScriptRoot $fileName
    
    # Check if the file does not exist, stop the script if missing
    if (-not (Test-Path $srcFilePath)) {
        Throw "$fileName not found at: $srcFilePath. Stopping script."
    }

    # Destination path in the current repository
    $destinationPath = Join-Path (Get-Location) $fileName
    
    # Copy file to the repo root
    Copy-Item -Path $srcFilePath -Destination $destinationPath -Force        
    Write-Output "$fileName copied to: $destinationPath"
}

function Append-Readme {
    $appendedText = "#License\n\nThis software is licensed under a custom [XBE EULA](LICENSE.md). By using it, you agree to the terms."
    
    # Define the README file path in the current repository
	$fileName = "README.md"
    $filePath = Join-Path (Get-Location) $fileName
    
    # Check if README.md exists
    if (Test-Path $filePath) {
        # Read the current content of README.md
        $currentContent = Get-Content -Path $filePath -Raw

        # Check if the notice is already present
        if ($currentContent -notlike "*$appendedText*") {
            # Ensure there is one line break before appending the text
            if ($currentContent -notlike "*`n") {
                $currentContent += "`n"
            }

            # Append the notice to the README.md
            Add-Content -Path $filePath -Value "`n$appendedText"
            Write-Output "Appended text to: $filePath"
        }
        else {
            Write-Output "appendedText already present in: $filePath"
        }
    }
    else {
        Write-Output "$fileName not found in: $(Get-Location)"
    }
}

## /TEMPLATE EXAMPLES ###########################################################

function Get-CurrentBranch {
    # Gets the current branch name
    $branch = git rev-parse --abbrev-ref HEAD
    return $branch
}

function Start-RepoCmds {
    param (
        [string]$dirPath
    )

    Set-Location $dirPath
	
    Write-Output ""
    Write-Output "-------------------------------"
    Write-Output "@ Repo: '${dirPath}'"
    
    $currentBranch = Get-CurrentBranch

    if ($MASTER_MAIN_BRANCH_PROTECTION -and ($currentBranch -eq 'master' -or $currentBranch -eq 'main')) {
        Write-Warning "Skipping repository '$dirPath' because it is on a protected branch: '$currentBranch'"
        return
    }

    Run-CustomCmds
	
    Write-Output ""
}

function Find-GitRepos {
    param (
        [string]$rootDir
    )

    $gitDirs = Get-ChildItem -Path $rootDir -Recurse -Directory -Force | Where-Object { Test-Path "$($_.FullName)\.git" }
    return $gitDirs
}

function Main {
    try {
        # Resolve the full path of the repos directory
        $resolvedReposDir = Resolve-Path $REPOS_AVAIL_DIR
        Set-Location $resolvedReposDir
        Write-Output "BASE DIR: $(pwd)"

        # Find all git repositories recursively
        $gitRepositories = Find-GitRepos -rootDir $resolvedReposDir

        foreach ($repo in $gitRepositories) {
            try {
                Start-RepoCmds -dirPath $repo.FullName
            }
            catch {
                Write-Error "Error processing repository '$($repo.FullName)': $_"
                if ($FAIL_ON_1ST_ERR) {
                    throw
                }
            }
        }
    }
    catch {
        Write-Error "An error occurred in the Main function: $_"
        if ($FAIL_ON_1ST_ERR) {
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
    Set-Location $STARTING_DIR
	
    Write-Output ""
    Write-Output "Done."
}
