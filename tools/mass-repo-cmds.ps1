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
$FAIL_ON_1ST_ERR = $true
$MASTER_MAIN_BRANCH_PROTECTION = $true  # Fail on master || main branch

# RUN YOUR CUSTOM COMMANDS HERE (or leave empty for dry run) >>
function Run-CustomCmds {
    # Add your custom commands here, for example:
    #git add .
    #git commit -m "doc(fix): Foo" -m "[XBND-123]"
    #git pull
    #git push
}

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
