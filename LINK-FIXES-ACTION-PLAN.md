# Link Fixes - Action Plan
## Step-by-Step Guide to Fix All Broken Links

**Repository:** /home/user/SteamEngine25
**Date:** 2025-11-13

---

## Quick Statistics

- **Total Broken Wikilinks:** 282
- **Critical Syntax Errors:** 3
- **Missing Files:** 1 (calendar/index.md)
- **Missing Images:** ~15
- **Estimated Fix Time:** 6-9 hours total

---

## PHASE 1: Critical Fixes (30 minutes)

### Fix 1: Malformed Markdown Link in architecture.md

**File:** `/home/user/SteamEngine25/docs/advanced/architecture.md`
**Line:** 12

**Current (Broken):**
```markdown
[shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>)
```

**Fixed:**
```markdown
[shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>)
```

**Action:** Add closing `)` at the end

---

### Fix 2: Malformed Markdown Link in configuration.md

**File:** `/home/user/SteamEngine25/docs/configuration.md`
**Line:** 43

**Current (Broken):**
```markdown
[glob](<https://en.wikipedia.org/wiki/Glob_(programming)>)
```

**Fixed:**
```markdown
[glob](<https://en.wikipedia.org/wiki/Glob_(programming)>)
```

**Action:** Add closing `)` at the end

---

### Fix 3: Wrong Filename in layout.md

**File:** `/home/user/SteamEngine25/docs/layout.md`
**Line:** 38

**Current (Broken):**
```markdown
See [a list of all the components](component.md) for all available components
```

**Fixed:**
```markdown
See [a list of all the components](layout-components.md) for all available components
```

**Action:** Change `component.md` to `layout-components.md`

---

### Fix 4: Create Missing calendar/index.md

**Missing File:** `/home/user/SteamEngine25/content/calendar/index.md`
**Referenced by:** 6 files

**Option A: Create New File**

Create `/content/calendar/index.md` with content like:

```markdown
---
title: "Calendar"
---

# Learning Journey Calendar

Navigate through the project timeline:

- [[calendar/Journey MOC|Journey Overview]]
- [[calendar/consolidated|Daily Breakdown]]
- [[calendar/timeline|Timeline]]
- [[calendar/milestones|Key Milestones]]

## Overview

This calendar section tracks the progression of the STEAM learning project
across 35+ days of instruction and student work.
```

**Option B: Update References**

Or update all 6 references to point to existing file:
- Change `[[calendar/index]]` to `[[calendar/Journey MOC]]` in:
  - `/content/atlas/Atlas MOC.md` (line 65)
  - `/content/calendar/Journey MOC.md` (line 118)
  - `/content/calendar/consolidated.md` (line 1237)
  - `/content/calendar/timeline.md` (line 119)
  - `/content/efforts/Project Storyarc.md` (line 148)
  - `/content/index.md` (lines 21, 71)

**Recommendation:** Option A (create the file) - better for site structure

---

## PHASE 2: Documentation Wikilinks (3-4 hours)

### Strategy Decision Required

Before bulk-fixing the 248 broken wikilinks in `/docs/`, you need to determine:

**How does Quartz resolve wikilinks in the `/docs/` directory?**

Test by checking `quartz.config.ts` for path resolution settings.

### Option 1: If Quartz uses content root

Update wikilinks to include `docs/` prefix:
- `[[configuration]]` → `[[docs/configuration]]`
- `[[layout]]` → `[[docs/layout]]`

### Option 2: If Quartz supports relative paths

Update wikilinks with relative paths:
- From `/docs/features/`: `[[configuration]]` → `[[../configuration]]`
- From `/docs/advanced/`: `[[configuration]]` → `[[../configuration]]`

### Option 3: If docs/ is a separate root

Keep same-directory references as-is, but add paths for cross-directory:
- Same dir: `[[configuration]]` stays as-is
- Features to root: `[[configuration]]` → `[[../configuration]]`
- Root to features: `[[wikilinks]]` → `[[features/wikilinks]]`

### Sample Fixes for Common Patterns

#### Pattern 1: Features referencing root docs

**Files affected:** Most files in `/docs/features/`

**Example from `/docs/features/i18n.md`:**
```markdown
Current: See [[configuration]] for more details
Fixed:   See [[../configuration]] for more details
```

**Bulk replace in features/ directory:**
```bash
# For same-directory links (keep as-is)
# For parent directory links
find /home/user/SteamEngine25/docs/features -name "*.md" -exec sed -i 's/\[\[configuration\]\]/[[..\/configuration]]/g' {} +
find /home/user/SteamEngine25/docs/features -name "*.md" -exec sed -i 's/\[\[layout\]\]/[[..\/layout]]/g' {} +
find /home/user/SteamEngine25/docs/features -name "*.md" -exec sed -i 's/\[\[authoring content\]\]/[[..\/authoring content]]/g' {} +
```

#### Pattern 2: Features referencing plugins

**Example from `/docs/features/Latex.md`:**
```markdown
Current: See [[plugins/Latex]] for configuration
Fixed:   See [[../plugins/Latex]] for configuration
```

#### Pattern 3: Root docs referencing features

**Example from `/docs/index.md`:**
```markdown
Current: Quartz supports [[wikilinks]]
Fixed:   Quartz supports [[features/wikilinks]]
```

### Systematic Approach

1. **Create a mapping file** of all broken wikilinks:
   - Source file
   - Current link
   - Correct path
   - Line number

2. **Test fixes** on a few files first:
   - Fix 2-3 files in each directory
   - Build the site with Quartz
   - Verify links work
   - Adjust strategy if needed

3. **Bulk apply** using find/replace:
   - Use sed, awk, or a Python script
   - Process by pattern (same patterns get same fix)
   - Verify with git diff before committing

---

## PHASE 3: Content Wikilinks (1-2 hours)

### Issue: Path Prefixes in Content

The `/content/atlas/` subdirectories have broken cross-references.

### Example Problem

In `/content/atlas/concepts/4Ms Framework MOC.md`:

**Current (Broken):**
```markdown
- [[concepts/4Ms Framework]]
- [[concepts/Design Thinking]]
- [[tools-techniques/Laser Cutting]]
```

### Solution Options

**Option A: Remove directory prefix** (if Quartz resolves by filename):
```markdown
- [[4Ms Framework]]
- [[Design Thinking]]
- [[Laser Cutting]]
```

**Option B: Use full path from content root**:
```markdown
- [[atlas/concepts/4Ms Framework]]
- [[atlas/concepts/Design Thinking]]
- [[atlas/tools-techniques/Laser Cutting]]
```

**Option C: Use relative paths**:
```markdown
- [[4Ms Framework]]  (same directory)
- [[Design Thinking]]  (same directory)
- [[../tools-techniques/Laser Cutting]]  (sibling directory)
```

### Test to Determine Correct Approach

1. Check how Quartz resolves links in existing working wikilinks
2. Look at `/content/index.md` for examples
3. Build and test with one file

### Bulk Fix Script Template

```python
#!/usr/bin/env python3
import re
from pathlib import Path

content_dir = Path("/home/user/SteamEngine25/content")

# Map of incorrect → correct paths
fixes = {
    r'\[\[concepts/': r'[[',  # Remove prefix if Option A
    r'\[\[tools-techniques/': r'[[../tools-techniques/',  # Relative if Option C
}

for md_file in content_dir.rglob("*.md"):
    content = md_file.read_text()
    for pattern, replacement in fixes.items():
        content = re.sub(pattern, replacement, content)
    md_file.write_text(content)
```

---

## PHASE 4: Images (2-3 hours)

### Missing Images Inventory

#### Documentation Screenshots

**Files that may exist elsewhere:**
1. `quartz transform pipeline.png` - Look in:
   - `/docs/assets/`
   - `/static/`
   - `/public/`
   - Original Quartz repo

2. `giscus-*.png` (4 images) - Screenshots of Giscus setup
3. `quartz-layout-*.png` (3 images) - Layout diagrams
4. `github-*.png` (2 images) - GitHub setup screenshots
5. `dns records.png` - DNS configuration
6. `social-image-preview-*.png` (4 images) - Social image examples

### Action Plan for Images

#### Step 1: Search for Images

```bash
# Search entire repo
find /home/user/SteamEngine25 -name "*.png" -o -name "*.jpg" -o -name "*.svg"

# Search for specific images
find /home/user/SteamEngine25 -name "*giscus*"
find /home/user/SteamEngine25 -name "*layout*"
```

#### Step 2: Locate Images

If images exist but are in wrong location:
- Move to appropriate directory
- Update wikilinks with correct paths

#### Step 3: Missing Images

For truly missing images:
- **Option A:** Download from original Quartz repository
- **Option B:** Create placeholder images
- **Option C:** Replace image wikilinks with text or remove

#### Step 4: Update Wikilink Syntax

Current Obsidian wikilink syntax:
```markdown
![[quartz-layout-desktop.png|800]]
```

May need to convert to standard markdown:
```markdown
![Quartz Desktop Layout](../assets/quartz-layout-desktop.png)
```

Or ensure Quartz handles Obsidian image syntax.

---

## PHASE 5: Validation (1 hour)

### After All Fixes

1. **Re-run link analysis:**
   ```bash
   python3 /home/user/SteamEngine25/analyze_links.py
   ```

2. **Build Quartz site:**
   ```bash
   npx quartz build
   ```

3. **Check for warnings/errors** in build output

4. **Test locally:**
   ```bash
   npx quartz build --serve
   ```
   - Browse to common pages
   - Click on previously broken links
   - Verify they now work

5. **Check external links** (optional):
   ```bash
   npm install -g markdown-link-check
   find /home/user/SteamEngine25/content /home/user/SteamEngine25/docs -name "*.md" -exec markdown-link-check {} \;
   ```

---

## Automation Scripts

### Script 1: Backup Before Changes

```bash
#!/bin/bash
# backup-before-link-fixes.sh

REPO="/home/user/SteamEngine25"
BACKUP_DIR="/home/user/SteamEngine25-backup-$(date +%Y%m%d-%H%M%S)"

echo "Creating backup at $BACKUP_DIR"
cp -r "$REPO" "$BACKUP_DIR"
echo "Backup complete!"
```

### Script 2: Find and Replace Wikilinks

```bash
#!/bin/bash
# fix-doc-wikilinks.sh

DOCS_DIR="/home/user/SteamEngine25/docs"

# Backup first!
git add -A
git commit -m "Before wikilink fixes"

# Fix common patterns in features/
find "$DOCS_DIR/features" -name "*.md" -type f -exec sed -i 's|\[\[configuration\]\]|[[../configuration]]|g' {} +
find "$DOCS_DIR/features" -name "*.md" -type f -exec sed -i 's|\[\[layout\]\]|[[../layout]]|g' {} +
find "$DOCS_DIR/features" -name "*.md" -type f -exec sed -i 's|\[\[authoring content\]\]|[[../authoring content]]|g' {} +

# Add more patterns as needed...

echo "Done! Check git diff to review changes"
```

### Script 3: Validate All Fixes

```bash
#!/bin/bash
# validate-link-fixes.sh

REPO="/home/user/SteamEngine25"

echo "Running link analysis..."
python3 "$REPO/analyze_links.py" | tee "$REPO/link-analysis-after-fixes.txt"

echo ""
echo "Building Quartz site..."
cd "$REPO"
npx quartz build 2>&1 | tee "$REPO/quartz-build-log.txt"

echo ""
echo "Results saved to:"
echo "  - link-analysis-after-fixes.txt"
echo "  - quartz-build-log.txt"
```

---

## Prioritized Task List

### Must Do (Critical)

- [ ] Fix 3 malformed markdown links (5 min)
- [ ] Create `/content/calendar/index.md` (10 min)
- [ ] Test Quartz wikilink resolution strategy (15 min)

### Should Do (High Priority)

- [ ] Fix all 248 documentation wikilinks (3-4 hours)
- [ ] Fix 34 content wikilinks (1-2 hours)
- [ ] Locate and fix missing images (2-3 hours)

### Could Do (Medium Priority)

- [ ] Validate external links (1 hour)
- [ ] Create link maintenance documentation (30 min)
- [ ] Set up automated link checking in CI/CD (1-2 hours)

### Nice to Have (Low Priority)

- [ ] Optimize wikilink structure across entire site
- [ ] Create link style guide for future content
- [ ] Add link validation to pre-commit hooks

---

## Expected Outcomes

After completing all fixes:

- **Wikilink success rate:** 73.9% → **99%+**
- **Internal link success rate:** 35.7% → **100%**
- **Build warnings:** Current unknown → **0 link-related warnings**
- **User experience:** Broken navigation → **Fully functional internal linking**

---

## Tools & Resources

**Analysis Tools:**
- `/home/user/SteamEngine25/analyze_links.py` - Link analysis script
- `markdown-link-check` - External link validator
- VS Code with Regex find/replace

**Documentation:**
- [Quartz Documentation](https://quartz.jzhao.xyz/)
- [Obsidian Wikilink Syntax](https://help.obsidian.md/Linking+notes+and+files/Internal+links)

**Generated Reports:**
- `/home/user/SteamEngine25/link-analysis-report.txt` - Full analysis output
- `/home/user/SteamEngine25/link-analysis-detailed.md` - Detailed breakdown
- `/home/user/SteamEngine25/link-analysis-summary.md` - Executive summary
- `/home/user/SteamEngine25/broken-wikilinks-by-file.md` - File-by-file breakdown
- `/home/user/SteamEngine25/LINK-FIXES-ACTION-PLAN.md` - This document

---

## Questions to Answer Before Starting

1. **Quartz Configuration:** How does your Quartz instance handle wikilink paths?
2. **Image Location:** Where should images be stored in your Quartz setup?
3. **Content Organization:** Do you want to restructure content organization before fixing links?
4. **Backup Strategy:** Have you backed up the repository before making bulk changes?

---

## Git Workflow Recommendation

```bash
# 1. Create a new branch for link fixes
git checkout -b fix/broken-links

# 2. Make incremental commits
git add docs/advanced/architecture.md
git commit -m "fix: correct malformed Wikipedia link in architecture.md"

git add content/calendar/index.md
git commit -m "feat: add missing calendar index page"

# 3. Fix docs in batches
git add docs/features/
git commit -m "fix: correct wikilink paths in features directory"

# 4. Validate before merging
npx quartz build
python3 analyze_links.py

# 5. Merge when ready
git checkout main
git merge fix/broken-links
```

---

**Ready to start? Begin with Phase 1 (30 minutes) for immediate critical fixes!**
