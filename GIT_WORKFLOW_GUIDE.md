# Git Workflow Guide for Collaborators

## Initial Setup (One Time Only)

### 1. Accept the GitHub Invitation
- Check your email for the repository invitation
- Click the link and accept the invitation

### 2. Clone the Repository
```bash
# Clone the repo to your computer
git clone <repository-url>
cd CondBalanceCode
```

### 3. Set Up Your Virtual Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Daily Workflow (Every Time You Work)

### Step 1: Update Your Local Main Branch
```bash
# Make sure you're on main branch
git checkout main

# Get the latest changes from GitHub
git pull origin main
```

### Step 2: Do Your Work
- Edit files, run code, create notebooks
- Test your changes to make sure they work

### Step 3: Save Your Changes Locally
```bash
# See what files you changed
git status

# Add all changed files
git add .

# Or add specific files
git add filename.py another_file.ipynb

# Commit with a descriptive message
git commit -m "Brief description of what you did"
```

### Step 4: Push Your Changes to GitHub
```bash
# Push to main branch
git push origin main
```

That's it! Your changes are now on GitHub.

## Working on Features (Optional - For Bigger Changes)

If you're working on something experimental or want to keep main stable:

```bash
# Create a new branch
git checkout -b feature-name

# Work and commit as usual
git add .
git commit -m "Description"

# Push the branch
git push origin feature-name

# When ready, merge it into main
git checkout main
git merge feature-name
git push origin main

# Delete the feature branch
git branch -d feature-name
```

## Important Guidelines

### ✅ DO:
- **Always pull before you start working** (`git pull origin main`)
- **Pull before pushing** to avoid conflicts
- Commit frequently with clear messages
- Test your code before pushing
- Communicate with your collaborator about what you're working on

### ❌ DON'T:
- **Don't use `git push -f` or `git push --force`** (this can overwrite your collaborator's work!)
- Don't commit large data files (they go in the Data/ folder which is gitignored)
- Don't commit virtual environment files (the venv/ folder is gitignored)
- Don't commit when you have broken code (fix it first or stash it)

## Common Commands Quick Reference

```bash
# Check what branch you're on
git branch

# See what files changed
git status

# See your recent commits
git log --oneline -10

# Discard changes to a file (be careful!)
git checkout -- filename.py

# See differences before committing
git diff

# Stash changes temporarily (to pull updates)
git stash
git pull origin main
git stash pop
```

## Troubleshooting

### "I get a merge conflict when pulling!"

This happens when you and your collaborator edited the same file.

```bash
# Git will mark the conflicts in your files
# Open the conflicted files and look for:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>>

# Edit the file to keep what you want (remove the markers)
# Then:
git add .
git commit -m "Resolved merge conflicts"
git push origin main
```

### "I need to update my code but I have uncommitted changes!"

**Option 1: Commit your changes**
```bash
git add .
git commit -m "Work in progress"
git pull origin main
```

**Option 2: Stash temporarily**
```bash
git stash              # Save changes temporarily
git pull origin main   # Get updates
git stash pop          # Restore your changes
```

### "I accidentally committed something wrong!"

**If you haven't pushed yet:**
```bash
# Undo the last commit (keeps your changes)
git reset --soft HEAD~1

# Fix your files, then commit again
git add .
git commit -m "Corrected commit message"
```

**If you already pushed:**
Contact your collaborator before trying to fix it!

### "I'm confused about what state I'm in!"

```bash
# This shows you everything
git status

# This shows recent commits
git log --oneline -5

# If really stuck, ask your collaborator or clone fresh
```

## Best Practices for Smooth Collaboration

1. **Communicate** - Let each other know what files you're working on
2. **Pull often** - Before starting work, before pushing
3. **Push complete work** - Don't push broken code
4. **Small commits** - Commit logical chunks, not giant changes
5. **Clear messages** - Write commit messages that explain what and why

## Project Structure Reminder

- `Figures/` - Your generated plots go here (not tracked by git)
- `Data/` - Your data files go here (not tracked by git)
- `*.py` - Python scripts (tracked by git)
- `*.ipynb` - Jupyter notebooks (tracked by git)
- `venv/` - Virtual environment (not tracked by git)
- `GIT_WORKFLOW_GUIDE.md` - This file!

## When in Doubt

- Run `git status` to see what's happening
- Run `git pull` to get the latest changes
- Ask your collaborator
- Google the error message (git errors are usually well-documented)
- You can always clone a fresh copy if things get messy
