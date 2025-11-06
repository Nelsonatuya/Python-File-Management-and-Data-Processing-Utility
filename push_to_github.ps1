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
    # Check if there is anything to commit
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

    # Push (may prompt for credentials)
    Write-Host "Pushing to origin/$branch ..."
    git push -u origin $branch

    Write-Host "Push complete. If authentication failed, follow instructions in PUSH_INSTRUCTIONS.md." -ForegroundColor Green
}
catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
    exit 1
}
