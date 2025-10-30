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
# Switch to main branch
git checkout main

# Get the latest changes
git pull origin main
```

### Step 2: Create a New Branch for Your Work
```bash
# Create and switch to a new branch
# Use a descriptive name like: fix-bug, add-analysis, update-plots
git checkout -b your-branch-name-here
```

### Step 3: Do Your Work
- Edit files, run code, create notebooks
- Test your changes to make sure they work

### Step 4: Save Your Changes
```bash
# See what files you changed
git status

# Add all changed files
git add .

# Or add specific files
git add filename.py

# Commit with a descriptive message
git commit -m "Brief description of what you did"
```

### Step 5: Push Your Branch to GitHub
```bash
# Push your branch (not main!)
git push origin your-branch-name-here
```

### Step 6: Create a Pull Request on GitHub
1. Go to the repository on GitHub.com
2. You'll see a yellow banner saying "your-branch-name-here had recent pushes"
3. Click the green **"Compare & pull request"** button
4. Add a description if needed
5. Click **"Create pull request"**

### Step 7: Merge Your Pull Request
1. On the pull request page, click the green **"Merge pull request"** button
2. Click **"Confirm merge"**
3. Optionally click **"Delete branch"** to clean up

### Step 8: Update Your Local Repository
```bash
# Switch back to main
git checkout main

# Pull the merged changes
git pull origin main

# Delete your local branch (cleanup)
git branch -d your-branch-name-here
```

## Important Rules

### ✅ DO:
- Always work on a new branch
- Pull the latest changes before starting new work
- Use descriptive branch names (`add-feature`, not `branch1`)
- Commit frequently with clear messages
- Ask questions if something seems wrong

### ❌ DON'T:
- Don't push directly to main (it's protected anyway)
- Don't use `git push -f` (force push) unless you're absolutely sure
- Don't commit large data files (they go in the Data/ folder which is gitignored)
- Don't commit virtual environment files (the venv/ folder is gitignored)

## Common Commands Quick Reference

```bash
# Check what branch you're on
git branch

# See what files changed
git status

# See your recent commits
git log --oneline -5

# Discard changes to a file (be careful!)
git checkout -- filename.py

# Switch to an existing branch
git checkout branch-name

# List all branches
git branch -a
```

## Troubleshooting

### "I'm on the wrong branch!"
```bash
# If you haven't committed yet:
git stash              # Save your changes temporarily
git checkout main      # Switch to main
git pull origin main   # Update main
git checkout -b new-branch-name  # Create proper branch
git stash pop          # Restore your changes
```

### "I committed to main by accident!"
Don't panic! Contact your collaborator. The branch protection should prevent pushing it.

### "I have merge conflicts!"
```bash
# Pull the latest changes
git pull origin main

# Git will mark the conflicts in the files
# Open the files and look for <<<<<<< ======= >>>>>>>
# Edit to keep what you want
# Then:
git add .
git commit -m "Resolved merge conflicts"
```

### "I need help!"
- Check `git status` to see what state you're in
- Ask your collaborator
- You can always make a fresh clone if things get really messy

## Project Structure Reminder

- `Figures/` - Your generated plots go here (not tracked by git)
- `Data/` - Your data files go here (not tracked by git)
- `*.py` - Python scripts (tracked by git)
- `*.ipynb` - Jupyter notebooks (tracked by git)
- `venv/` - Virtual environment (not tracked by git)

