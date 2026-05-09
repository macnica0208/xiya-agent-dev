# Git And GitHub Workflow

Last updated: 2026-05-09

## Goal

Put the Xiya project under version control without leaking secrets, private assets, runtime data, or the user's separate research work.

Current fact: `data/plugins/astrbot_plugin_xiya` is not a Git repository yet.

## Recommended Repo Shape

Recommended first repo:

- Private GitHub repo.
- New GitHub account is fine if the user wants separation from research work.
- Code and safe docs only at first.
- Do not commit private archives, adult/private assets, API keys, Discord tokens, NovelAI keys, Kimi/DeepSeek keys, `.env`, or `runtime_data`.

Optional later split:

- `xiya-agent-sfw-dev`: code, SFW docs, safe fixtures.
- Separate encrypted/private storage for normal/private content, only if the user explicitly wants it.

## Secret Audit Before First Commit

Before `git add`, inspect and/or create `.gitignore`.

Must ignore:

```gitignore
.env
.env.*
*.key
*.pem
*token*
*secret*
runtime_data/
private_assets/
*.tar.gz
*.zip
*.7z
*.sha256.txt
__pycache__/
.pytest_cache/
node_modules/
```

Also check for:

- Discord bot tokens.
- NovelAI keys.
- DeepSeek / Kimi / NAI / OpenAI keys.
- Downloaded archives.
- Generated images that the user has not approved for repo storage.
- Claude/Anthropic config, auth, cache, or research directories.

Codex rule: never run `git add .` for the first commit until the secret audit is complete.

## Local Git Commands

After the user chooses the repo root and remote:

```powershell
git init
git status --short
git add .gitignore docs/CODEX_START_HERE.md docs/PROJECT_GOAL_AND_ROLES.md docs/TODO_ACCEPTANCE_BOARD.md docs/GIT_GITHUB_WORKFLOW.md
git status --short
git commit -m "docs: add Codex operating workflow"
git branch -M main
git remote add origin https://github.com/<account>/<repo>.git
git push -u origin main
```

For future work:

```powershell
git status --short
git diff -- <path>
git add <reviewed-path>
git commit -m "<type>: <short summary>"
git push
```

## Authentication Options

Current blocker on 2026-05-09:

- Local safe commit exists.
- Remote is `https://github.com/macnica0208/xiya-agent-dev.git`.
- Push failed because Windows Git used cached HTTPS credentials for `s20175zhang-svg`, and GitHub returned 403.
- A dedicated SSH key and alias were then created:
  - Private key: `C:\Users\BRADY\.ssh\xiya_agent_dev_ed25519`
  - SSH alias: `github-xiya`
  - Project remote: `git@github-xiya:macnica0208/xiya-agent-dev.git`
  - SSH test result: authenticated as `macnica0208`.

Safe fix: authenticate Git as `macnica0208` or grant `s20175zhang-svg` write access to the repo. For separation, authenticating as `macnica0208` with a dedicated SSH key is the cleanest route.

Option A: GitHub CLI

```powershell
gh auth login
gh repo create <account>/<repo> --private --source . --remote origin
git push -u origin main
```

Option B: HTTPS personal access token

- Use a fine-grained token with access only to the chosen repo.
- Let Windows Credential Manager store it.
- Do not paste the token into Markdown, Discord, logs, or repo files.

Option C: SSH key dedicated to this project/account

```powershell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\xiya_github_ed25519 -C "xiya-github"
```

Then add a host alias in SSH config and use an SSH remote. This is clean if the user uses multiple GitHub accounts.

## Codex Git Red Lines

- No push without explicit user approval or a previously agreed automation rule.
- No force push unless the user explicitly asks and the target is verified.
- No `git reset --hard` or checkout-based reverts unless explicitly requested.
- No commits containing secrets, private assets, adult/private packs, or unrelated user changes.
- If the worktree is dirty, inspect before staging and commit only the paths relevant to the task.

## GitHub Connector

The Codex GitHub connector is available in this environment for GitHub-side work such as inspecting repos, issues, PRs, or creating GitHub objects. It does not replace local secret audit. Use local Git for file history and the connector later for repo/PR operations once the user selects or creates the repo.
