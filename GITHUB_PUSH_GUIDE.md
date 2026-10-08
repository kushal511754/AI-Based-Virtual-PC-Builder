# Push this project to GitHub

1. Create an empty repository on GitHub, or use an existing repository URL.
2. Sign in with Git Credential Manager or GitHub CLI. Do not put a personal access token in a remote URL or commit it to a file.
3. Add the repository as `origin`, then push the `main` branch:

   ```powershell
   git remote add origin <repository-url>
   git branch -M main
   git push -u origin main
   ```

Local environment files, virtual environments, databases with user data, logs, extracted datasets, and the oversized `games.csv` are excluded by `.gitignore`. The included `.env.example` lists the configuration variable names; copy it to `.env` locally and provide your own values.
