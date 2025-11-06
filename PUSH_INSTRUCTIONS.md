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

