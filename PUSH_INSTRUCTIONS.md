# How to push this project to GitHub (manual)

1. Create a GitHub repository on github.com (click "New repository") and copy the remote URL (HTTPS or SSH).

2. In PowerShell (inside the project folder c:\Users\User\Desktop\python\filemanagement):

- Initialize git (if not already):
  git init

- Stage and commit:
  git add -A
  git commit -m "Initial commit"

- Add remote (replace URL with your repo URL):
  git remote add origin https://github.com/username/repo.git

- Create/rename to main branch and push:
  git branch -M main
  git push -u origin main

3. Authentication notes:
- HTTPS: Git may prompt for username/password. For better security use a Personal Access Token (PAT) instead of password.
- SSH: Set up SSH keys and add the public key to your GitHub account, then use the SSH remote URL (git@github.com:username/repo.git).

4. Troubleshooting:
- If you get permission errors, follow GitHub's instructions to configure PAT or SSH: https://docs.github.com/en/authentication
- If the remote already exists and you need to change it:
  git remote set-url origin <new-url>

5. Optional helper:
- Run the provided PowerShell helper:
  .\push_to_github.ps1
  It will prompt for the remote URL and branch and attempt to push interactively.


## Resolving "Updates were rejected" (non-fast-forward)

If `git push` is rejected with messages like:
- "Updates were rejected because the remote contains work that you do not have locally."
or
- "failed to push some refs ... (fetch first)"

You have a few safe options:

1) Pull with rebase (recommended)
- This updates your local branch by replaying your commits on top of remote changes.
  git fetch origin
  git pull --rebase origin main
  git push origin main

If rebase reports conflicts, resolve them, then:
  git add <resolved-files>
  git rebase --continue
  git push origin main

2) Pull with merge
- Merges remote changes into your local branch:
  git fetch origin
  git pull origin main
  # Resolve conflicts if any, commit, then:
  git push origin main

3) Force push (dangerous)
- This overwrites the remote branch with your local branch. Avoid unless you are certain.
  git push --force origin main
- Only use when you understand consequences (you may erase others' commits).

4) If unsure, inspect remote commits:
  git fetch origin
  git log --oneline origin/main --not main

General notes
- Prefer pull --rebase to create a linear history.
- If others are collaborating, coordinate before force-pushing.
- Use a Personal Access Token (PAT) or SSH for authentication if prompted.

