# Deployment Log: Quartz Setup for SteamEngine25

**Date:** November 10, 2025
**Repository:** lpcode808/SteamEngine25
**Objective:** Deploy Quartz (Obsidian publish alternative) to GitHub Pages

---

## Timeline of Actions

### 1. Initial Setup (Commit 759dbf1)

**What we did:**
- Cloned Quartz v4 repository into empty SteamEngine25 repo
- Copied all Quartz files (source code, configs, workflows)
- Configured `quartz.config.ts` with custom settings:
  - Changed page title from "Quartz 4" → "SteamEngine25"
  - Updated base URL to `lpcode808.github.io/SteamEngine25`
  - Kept default theme and plugins

**Files created:**
- `.github/workflows/deploy.yml` - GitHub Actions deployment workflow
- `content/index.md` - Welcome page
- `content/example-note.md` - Example note showing Quartz features
- All Quartz infrastructure (quartz/, package.json, etc.)

**Files removed:**
- Quartz's original workflow files (build-preview.yaml, ci.yaml, etc.)
- Kept only our custom deploy.yml for simpler setup

---

### 2. Authentication Struggles

**Problem:** Could not push to GitHub from the CLI environment.

**Attempts made:**
1. **First token attempt:** Created PAT without `repo` scope
   - Result: 403 Permission denied

2. **Second token attempt:** Created PAT with `repo` scope but no `workflow` scope
   - Result: 403 error - "refusing to allow a Personal Access Token to create or update workflow without `workflow` scope"

3. **Final token attempt:** Created PAT with both `repo` AND `workflow` scopes
   - Result: ✅ Success!

**Why this happened:**
- GitHub requires special permission to modify `.github/workflows/` files for security
- Regular `repo` scope isn't enough when pushing workflow files
- The `workflow` scope is specifically needed to update GitHub Actions workflows

---

### 3. Branch Strategy Issues

**Problem:** Could not push to `v4` branch (got 403 errors).

**Why it failed:**
- `v4` branch likely has branch protection rules enabled
- Even with proper token, protected branches restrict who can push
- This is a common security practice for main branches

**Our solution:**
- Created feature branch: `claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF`
- Updated workflow to deploy from feature branch (added branch name to `on.push.branches`)
- This allows deployment without touching protected branches

**Alternative solutions we considered:**
- Creating a `main` branch (tried but also got 403)
- Merging via Pull Request (would require manual approval)
- Pushing from local machine with admin credentials

---

### 4. First Deployment Failure (Commit a4f654a)

**Problem:** GitHub Actions build failed with exit code 1.

**The issue:**
```yaml
# In .github/workflows/deploy.yml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 20  # ❌ Wrong version!
```

**Root cause:**
- Quartz's `package.json` specifies engine requirements:
  ```json
  "engines": {
    "npm": ">=10.9.2",
    "node": ">=22"  // Requires Node.js 22 or higher
  }
  ```
- Our workflow used Node.js 20
- npm refused to install dependencies due to version mismatch

---

### 5. Final Fix (Commit 4fb155f)

**What we changed:**
```yaml
# In .github/workflows/deploy.yml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: 22  # ✅ Correct version!
```

**Result:** ✅ Deployment succeeded!

**Build process:**
1. GitHub Actions checks out code
2. Sets up Node.js 22
3. Runs `npm ci` (clean install of dependencies)
4. Runs `npx quartz build` (builds static site)
5. Uploads build artifacts to GitHub Pages
6. Deploys to https://lpcode808.github.io/SteamEngine25/

---

## Final Configuration

### Repository Structure
```
SteamEngine25/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── content/                     # Your Obsidian notes go here
│   ├── index.md                # Homepage
│   └── example-note.md         # Example note
├── quartz/                      # Quartz source code
├── docs/                        # Quartz documentation
├── quartz.config.ts            # Site configuration
├── quartz.layout.ts            # Layout configuration
├── package.json                # Dependencies
└── tsconfig.json               # TypeScript config
```

### Active Branch
- **Feature branch:** `claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF`
- **Deploys from:** This feature branch (not main/master)
- **Protected branch:** `v4` (upstream, cannot push directly)

### Deployment Configuration
- **Platform:** GitHub Pages
- **URL:** https://lpcode808.github.io/SteamEngine25/
- **Trigger:** Push to feature branch or manual workflow dispatch
- **Build time:** ~2-5 minutes

---

## Troubleshooting History

| Issue | Error | Solution |
|-------|-------|----------|
| Can't push to GitHub | `could not read Username` | Created Personal Access Token |
| Can't push workflows | `refusing to allow PAT without workflow scope` | Added `workflow` scope to token |
| Can't push to v4 | `403 forbidden` | Used feature branch instead |
| Build fails | `exit code 1` | Updated Node.js 20 → 22 |

---

## Next Steps for Content

### Adding Your Obsidian Notes

**Method 1: Direct copy**
```bash
cp -r /path/to/ObsidianVault/*.md content/
git add content/
git commit -m "Add my notes"
git push
```

**Method 2: Selective sync**
```bash
# Copy specific folders
cp -r /path/to/ObsidianVault/Projects content/
cp -r /path/to/ObsidianVault/Notes content/
```

**What gets published:**
- ✅ All `.md` files in `content/`
- ✅ Wikilinks, backlinks, tags
- ✅ Images and attachments
- ❌ `.obsidian/` folder (excluded via config)
- ❌ `private/` folder (excluded via config)
- ❌ Files marked with `draft: true` frontmatter

---

## Current Status

✅ **Deployment successful**
✅ **Site live at:** https://lpcode808.github.io/SteamEngine25/
✅ **Automatic deployments enabled**
✅ **Sample content in place**

Ready for your Obsidian notes!
