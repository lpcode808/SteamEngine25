# SteamEngine25 - Digital Garden

> Publishing my Obsidian notes to the web using [Quartz v4](https://quartz.jzhao.xyz/)

**Live Site:** https://lpcode808.github.io/SteamEngine25/

---

## What Is This?

Think of this as a **self-publishing press for your thoughts**. You write notes in Obsidian (your private notebook), and this system transforms them into a beautiful website that anyone can read.

**The analogy:**
```
Obsidian = Your private journal
   ↓
This repo = Your printing press
   ↓
GitHub Pages = Your bookstore
```

---

## How It Works (The Big Picture)

### The Publishing Pipeline

Imagine you're publishing a newspaper:

1. **✍️ You write articles** (Obsidian notes on your computer)
2. **📦 You send them to the print shop** (push to GitHub)
3. **🏭 The print shop processes them** (GitHub Actions builds the site)
4. **📰 Newspapers appear on newsstands** (your website updates)

### The Technical Flow

```
Your Computer
    │
    │ You edit notes in Obsidian
    │ You copy notes to content/ folder
    │
    ├─ git add content/
    ├─ git commit -m "Add new notes"
    ├─ git push
    │
    ▼
GitHub (The Cloud)
    │
    │ Receives your changes
    │ Triggers GitHub Actions
    │
    ▼
GitHub Actions (The Build Robot)
    │
    ├─ Step 1: Downloads your code
    ├─ Step 2: Installs Node.js 22
    ├─ Step 3: Installs dependencies (npm ci)
    ├─ Step 4: Runs Quartz build
    │          - Converts Markdown → HTML
    │          - Resolves [[wikilinks]]
    │          - Generates backlinks
    │          - Creates search index
    │          - Bundles JavaScript & CSS
    ├─ Step 5: Packages everything
    │
    ▼
GitHub Pages (Your Website)
    │
    │ Receives the built site
    │ Deploys to CDN
    │
    ▼
🌐 https://lpcode808.github.io/SteamEngine25/
    │
    └─ Visitors can read your notes!
```

---

## How to Update Your Notes

### Method 1: Copy & Push (Simplest)

**The recipe:**

```bash
# 1. Navigate to this repository on your computer
cd /path/to/SteamEngine25

# 2. Make sure you're on the right branch
git checkout claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF

# 3. Copy notes from your Obsidian vault
cp /path/to/YourObsidianVault/*.md content/

# Or copy specific folders:
cp -r /path/to/YourObsidianVault/Projects content/
cp -r /path/to/YourObsidianVault/Writing content/

# 4. Stage your changes
git add content/

# 5. Commit with a message
git commit -m "Add latest notes from Obsidian"

# 6. Push to GitHub (this triggers deployment!)
git push

# 7. Wait 2-5 minutes, then check your site
```

**What happens next:**
- GitHub receives your push
- GitHub Actions automatically starts building
- 2-5 minutes later, your site updates
- Your new notes are live!

### Method 2: Sync Script (Advanced)

Create a file called `sync-obsidian.sh`:

```bash
#!/bin/bash

# Configuration
OBSIDIAN_VAULT="/path/to/your/ObsidianVault"
REPO_PATH="/path/to/SteamEngine25"
BRANCH="claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF"

# Navigate to repo
cd "$REPO_PATH"

# Make sure we're on the right branch
git checkout "$BRANCH"

# Sync files (excluding .obsidian folder)
rsync -av --delete \
  --exclude='.obsidian' \
  --exclude='private' \
  --exclude='templates' \
  "$OBSIDIAN_VAULT/" content/

# Commit and push
git add content/
git commit -m "Sync from Obsidian $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ Sync complete! Site will update in 2-5 minutes."
```

Make it executable and run:
```bash
chmod +x sync-obsidian.sh
./sync-obsidian.sh
```

**Pro tip:** Add this to cron to auto-sync daily!

### Method 3: Selective Publishing

Only publish specific folders:

```bash
# Only sync your "Public" folder from Obsidian
cp -r ~/ObsidianVault/Public/* content/

# Or use tags in frontmatter
# Only copy files with "publish: true" in frontmatter
# (requires a custom script)
```

---

## Understanding the Magic: What Happens During Build

### The Transformation

**Think of Quartz as a translator:**

```
INPUT: Your Markdown
═══════════════════════════════════════════
---
title: My Note
tags: [ideas, projects]
---

# My Note

This is a [[linked note]] about #productivity.

`code example`
═══════════════════════════════════════════

          ↓ [Quartz Build Process]

OUTPUT: A Beautiful Website
═══════════════════════════════════════════
• HTML with proper structure
• CSS for styling
• JavaScript for interactivity
• Search index for finding notes
• Graph visualization of connections
• Working links between notes
• Syntax highlighted code
═══════════════════════════════════════════
```

### The Build Steps (Demystified)

**1. Parse Frontmatter** 📋
```
Before: ---\ntitle: My Note\n---
After:  metadata = { title: "My Note" }
```
*Like reading the cover page of a document*

**2. Convert Markdown to HTML** 🔄
```
Before: # Heading
After:  <h1>Heading</h1>
```
*Translating from shorthand to full format*

**3. Resolve Wikilinks** 🔗
```
Before: [[my-other-note]]
After:  <a href="/my-other-note">my-other-note</a>
```
*Finding all the cross-references and making them clickable*

**4. Generate Backlinks** ⬅️
```
If note A links to note B,
Then note B shows "linked from: note A"
```
*Like a bibliography that builds itself*

**5. Create Search Index** 🔍
```
Takes all your content → Makes it searchable
Think: Creating an index at the back of a book
```

**6. Bundle Assets** 📦
```
Combines all JavaScript files → One optimized file
Compiles all CSS styles → One stylesheet
Optimizes images → Smaller file sizes
```
*Packing everything efficiently for travel*

---

## The "Why" Behind the Workflow

### Why Git?

**Analogy:** Git is like track changes in Microsoft Word, but way more powerful.

- **Version control:** See every change you've ever made
- **Undo anything:** Made a mistake? `git revert`
- **Branching:** Try changes without affecting the live site
- **Collaboration:** Multiple people can work without conflicts

### Why GitHub Actions?

**Analogy:** GitHub Actions is like a robot assistant that works 24/7.

**Without automation:**
```
You: Write notes
You: Copy files
You: Run build script
You: Upload to server
You: Configure server
You: Clear cache
You: Test site
You: Fix issues
You: Repeat
```

**With GitHub Actions:**
```
You: Write notes
You: git push
Robot: Does everything else perfectly, every time
```

### Why Static Site Generation?

**Analogy:** The difference between a restaurant and a microwave meal.

**Dynamic site (like WordPress):**
```
User requests page
  ↓
Server wakes up
  ↓
Queries database
  ↓
Runs PHP code
  ↓
Generates HTML
  ↓
Sends to user
⏱️ Takes 500ms+
```

**Static site (like Quartz):**
```
User requests page
  ↓
CDN sends pre-built HTML
⏱️ Takes 50ms
```

**Benefits:**
- ⚡ **Fast:** No processing, just serve files
- 💰 **Cheap:** No server, no database
- 🛡️ **Secure:** Nothing to hack (no PHP, no database)
- 📈 **Scalable:** CDN handles millions of visitors
- 🔧 **Simple:** No server maintenance

---

## Troubleshooting

### "My changes aren't showing up!"

**Check these things:**

1. **Did the build succeed?**
   - Visit: https://github.com/lpcode808/SteamEngine25/actions
   - Look for a green checkmark ✅
   - If red ❌, click to see error logs

2. **Did you push to the right branch?**
   ```bash
   git branch  # Should show: claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF
   ```

3. **Browser cache?**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Or open in incognito mode

4. **Still building?**
   - Wait 5 minutes
   - Check Actions tab for "In progress" 🟡

### "Build failed with exit code 1"

**Common causes:**

1. **Broken link in markdown**
   ```markdown
   [[note-that-doesnt-exist]]  # This might cause issues
   ```

2. **Invalid frontmatter**
   ```yaml
   ---
   title: My Note
   date: not-a-real-date  # Should be YYYY-MM-DD
   ---
   ```

3. **Syntax errors in files**
   - Look at the GitHub Actions logs
   - It will tell you which file failed

### "Push failed with 403 error"

Your token might have expired (remember, we set it to 7 days).

**Solution:**
1. Create new token: https://github.com/settings/tokens
2. Select scopes: ✅ `repo` ✅ `workflow`
3. Update git remote:
   ```bash
   git remote set-url origin https://YOUR_NEW_TOKEN@github.com/lpcode808/SteamEngine25.git
   ```

---

## File Structure Explained

```
SteamEngine25/
│
├── content/                    ← YOUR NOTES GO HERE
│   ├── index.md               ← Homepage
│   ├── example-note.md        ← Example (can delete)
│   └── [your notes].md        ← Add your notes here
│
├── quartz/                     ← Quartz source code (don't edit)
│   └── ...
│
├── quartz.config.ts           ← Site configuration
│   ├── Page title: "SteamEngine25"
│   ├── URL: lpcode808.github.io/SteamEngine25
│   ├── Plugins: What features are enabled
│   └── Theme: Colors, fonts, etc.
│
├── quartz.layout.ts           ← Page layout (sidebar, header, etc.)
│
├── .github/workflows/
│   └── deploy.yml             ← The "robot" that builds your site
│
├── package.json               ← Defines dependencies
│
├── log.md                     ← What we did to set this up
├── lessons.md                 ← What we learned
└── README.md                  ← This file!
```

---

## Customization

### Change Site Title

Edit `quartz.config.ts`:
```typescript
pageTitle: "SteamEngine25",  // Change this
```

### Change Colors

Edit `quartz.config.ts`, look for the `colors` section:
```typescript
colors: {
  lightMode: {
    light: "#faf8f8",      // Background
    dark: "#2b2b2b",       // Text
    secondary: "#284b63",  // Links
    // etc.
  }
}
```

### Add Custom Domain

1. Buy a domain (example.com)
2. Add CNAME record pointing to: `lpcode808.github.io`
3. Add file `content/CNAME` with your domain:
   ```
   example.com
   ```
4. Update `baseUrl` in `quartz.config.ts`

### Disable Features

Don't need graph view? Edit `quartz.config.ts`:
```typescript
// Comment out plugins you don't want
// Plugin.Graph(),  ← Now disabled
```

---

## Advanced: Understanding Your Workflow File

**Location:** `.github/workflows/deploy.yml`

Let's break it down:

```yaml
name: Deploy Quartz to GitHub Pages
# This is just a label, shows up in Actions tab

on:
  push:
    branches:
      - claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF
  # Trigger: When you push to this branch

  workflow_dispatch:
  # Trigger: Manual button in GitHub UI

permissions:
  contents: read      # Can read repo files
  pages: write        # Can deploy to GitHub Pages
  id-token: write     # Can authenticate

jobs:
  build:
    runs-on: ubuntu-latest  # Use Ubuntu VM

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        # Downloads your code to the VM

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
        # Installs Node.js (needed for build tools)

      - name: Install dependencies
        run: npm ci
        # Installs Quartz and all its tools

      - name: Build Quartz
        run: npx quartz build
        # THE MAGIC STEP: Transforms markdown → website

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public
        # Packages the built site for deployment

  deploy:
    needs: build  # Wait for build to finish
    runs-on: ubuntu-latest

    steps:
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
        # Publishes your site to the web
```

**In human terms:**
1. GitHub notices you pushed code
2. Spins up a fresh Ubuntu computer in the cloud
3. Downloads your code onto it
4. Installs Node.js and tools
5. Runs the build process
6. Takes the output and publishes it
7. Your site is live!
8. Shuts down the computer (you don't pay for it)

---

## The Big Picture: Why This Is Powerful

### What You Get

✅ **Version control:** Never lose a note, see all history
✅ **Automatic deployment:** Push once, robot does the rest
✅ **Free hosting:** GitHub Pages = $0/month
✅ **Fast website:** CDN, static files, global distribution
✅ **Professional setup:** Same tools used by major companies
✅ **Learning opportunity:** Understanding modern web development
✅ **Privacy control:** You decide what's published
✅ **Backup:** Your notes are on GitHub + your computer

### Compared to Alternatives

| Feature | This Setup | Obsidian Publish | Notion | Medium |
|---------|-----------|------------------|--------|--------|
| Cost | Free | $8/month | Free/Paid | Free |
| Customization | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡ | ⚡⚡ |
| Privacy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Setup complexity | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Learning value | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐ |

---

## Quick Reference

### Daily Workflow
```bash
# 1. Update notes
cd /path/to/SteamEngine25
git checkout claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF

# 2. Copy from Obsidian
cp /path/to/Obsidian/*.md content/

# 3. Push
git add content/
git commit -m "Update notes"
git push

# 4. Wait ~3 minutes
# 5. Visit https://lpcode808.github.io/SteamEngine25/
```

### Useful Commands
```bash
# See what changed
git status
git diff

# View commit history
git log --oneline -10

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Check build status
# Visit: https://github.com/lpcode808/SteamEngine25/actions

# Test locally before pushing
npm install
npx quartz build --serve
# Visit: http://localhost:8080
```

### Important URLs
- 🌐 Live site: https://lpcode808.github.io/SteamEngine25/
- 📊 Build status: https://github.com/lpcode808/SteamEngine25/actions
- ⚙️ GitHub Pages settings: https://github.com/lpcode808/SteamEngine25/settings/pages
- 🔑 Tokens: https://github.com/settings/tokens

---

## Learning Resources

### Want to understand more?

**Read these files in this repo:**
- `log.md` - What we did step by step
- `lessons.md` - Deep dive into concepts

**Quartz documentation:**
- Official docs: https://quartz.jzhao.xyz/
- Configuration: https://quartz.jzhao.xyz/configuration
- Plugins: https://quartz.jzhao.xyz/plugins

**Related technologies:**
- Git basics: https://rogerdudler.github.io/git-guide/
- GitHub Actions: https://docs.github.com/actions
- Markdown: https://www.markdownguide.org/
- Static site generators: https://jamstack.org/

---

## Philosophy

**This setup embodies:**

🌱 **Digital Gardening** - Notes grow and connect over time
🔓 **Open by default** - Share knowledge freely
🛠️ **Tools over platforms** - Own your content and workflow
📚 **Learn by doing** - Understanding beats memorization
⚡ **Automation** - Computers should do repetitive tasks

**From Obsidian to web:**
```
Private thinking → Public sharing
Local files → Global access
Personal notes → Collective knowledge
```

---

## Questions?

**Common questions:**

**Q: Can I keep some notes private?**
A: Yes! Don't copy them to `content/`, or add folders to `ignorePatterns` in config.

**Q: What if I break something?**
A: That's what git is for! `git log` + `git revert` = time machine.

**Q: How much does this cost?**
A: $0. GitHub Pages is free for public repos.

**Q: Can I delete the example notes?**
A: Absolutely! Delete `content/example-note.md` and update `content/index.md`.

**Q: What if my Obsidian vault is huge?**
A: Only copy what you want to publish. Or use `rsync --exclude` to filter.

**Q: Can I use a custom domain?**
A: Yes! See "Add Custom Domain" section above.

---

**Happy publishing! 🚀**

*Remember: Every expert started as a beginner. You just built something that many developers would find impressive.*
