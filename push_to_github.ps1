try {
    $cwd = Get-Location
    Write-Host "Working directory: $cwd"

    # Check git is available
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Git is not installed or not in PATH. Please install Git first." -ForegroundColor Red
        exit 1
    }

    # Ask for remote URL and branch
    $remoteUrl = Read-Host "Enter remote repository URL (e.g. https://github.com/username/repo.git or git@github.com:username/repo.git)"
    if ([string]::IsNullOrWhiteSpace($remoteUrl)) {
        Write-Host "Remote URL is required. Aborting." -ForegroundColor Yellow
        exit 1
    }
    $branch = Read-Host "Enter branch to push (default: main)"
    if ([string]::IsNullOrWhiteSpace($branch)) { $branch = "main" }

    # Init repo if .git not present
    if (-not (Test-Path -Path ".git")) {
        git init
        Write-Host "Initialized empty git repository."
    }
    else {
        Write-Host "Git repository already initialized."
    }

    # Stage files and commit
    git add -A
    $status = git status --porcelain
    if (-not [string]::IsNullOrWhiteSpace($status)) {
        git commit -m "Initial commit"
        Write-Host "Committed changes."
    }
    else {
        Write-Host "No changes to commit."
    }

    # Add or update remote
    $existing = git remote
    if ($existing -contains "origin") {
        git remote set-url origin $remoteUrl
        Write-Host "Updated remote 'origin' URL."
    }
    else {
        git remote add origin $remoteUrl
        Write-Host "Added remote 'origin'."
    }

    # Ensure branch exists locally, create if necessary
    $localBranches = git branch --list | ForEach-Object { $_.TrimStart("* ").Trim() }
    if (-not ($localBranches -contains $branch)) {
        git branch -M $branch
    }
    else {
        git checkout $branch
    }

    function Attempt-Push {
        param($branch)
        Write-Host "Pushing to origin/$branch ..."
        $pushOutput = git push -u origin $branch 2>&1
        $exit = $LASTEXITCODE
        return @{ ExitCode = $exit; Output = $pushOutput }
    }

    $result = Attempt-Push -branch $branch
    if ($result.ExitCode -eq 0) {
        Write-Host "Push succeeded." -ForegroundColor Green
    }
    else {
        Write-Host $result.Output
        if ($result.Output -match "rejected" -or $result.Output -match "non-fast-forward") {
            Write-Host ""
            Write-Host "Push was rejected because the remote contains work you do not have locally." -ForegroundColor Yellow
            Write-Host "Choose how to proceed:"
            Write-Host "  1) Pull (rebase) from remote and retry push (recommended)"
            Write-Host "  2) Pull (merge) from remote and retry push"
            Write-Host "  3) Force push (overwrite remote) -- DANGEROUS"
            Write-Host "  4) Abort and resolve manually"
            $choice = Read-Host "Enter choice number (1/2/3/4)"

            switch ($choice) {
                "1" {
                    Write-Host "Running: git pull --rebase origin $branch"
                    $pullOut = git pull --rebase origin $branch 2>&1
                    if ($LASTEXITCODE -ne 0) {
                        Write-Host $pullOut
                        Write-Host "Rebase/pull failed. You may need to resolve conflicts manually." -ForegroundColor Red
                        Write-Host "Abort rebase with: git rebase --abort"
                        exit 1
                    }
                    Write-Host "Rebase/pull succeeded. Retrying push..."
                    $retry = Attempt-Push -branch $branch
                    if ($retry.ExitCode -eq 0) { Write-Host "Push succeeded." -ForegroundColor Green } else { Write-Host $retry.Output; Write-Host "Push still failed. Resolve manually." -ForegroundColor Red }
                }
                "2" {
                    Write-Host "Running: git pull origin $branch"
                    $pullOut = git pull origin $branch 2>&1
                    if ($LASTEXITCODE -ne 0) {
                        Write-Host $pullOut
                        Write-Host "Pull failed. Resolve conflicts manually." -ForegroundColor Red
                        exit 1
                    }
                    Write-Host "Pull succeeded. Retrying push..."
                    $retry = Attempt-Push -branch $branch
                    if ($retry.ExitCode -eq 0) { Write-Host "Push succeeded." -ForegroundColor Green } else { Write-Host $retry.Output; Write-Host "Push still failed. Resolve manually." -ForegroundColor Red }
                }
                "3" {
                    $confirm = Read-Host "Are you sure you want to force-push and overwrite remote branch? Type 'YES' to confirm"
                    if ($confirm -eq "YES") {
                        Write-Host "Force pushing (git push -f origin $branch) ..."
                        $forceOut = git push -f origin $branch 2>&1
                        if ($LASTEXITCODE -eq 0) { Write-Host "Force push succeeded." -ForegroundColor Green } else { Write-Host $forceOut; Write-Host "Force push failed." -ForegroundColor Red }
                    }
                    else {
                        Write-Host "Force-push aborted by user."
                    }
                }
                default {
                    Write-Host "Aborting. Resolve the remote/local divergence manually (see PUSH_INSTRUCTIONS.md)." -ForegroundColor Yellow
                }
            }
        }
        else {
            Write-Host "Push failed with unexpected error. See output above." -ForegroundColor Red
        }
    }

    Write-Host "Done."
}
catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
    exit 1
}
