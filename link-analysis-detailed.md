# Broken Links Analysis Report
## Quartz-Based Site: SteamEngine25

**Generated:** 2025-11-13

---

## Executive Summary

- **Total Files Analyzed:** 123 markdown files
- **Total Wikilinks Found:** 1,081
- **Broken Wikilinks:** 282 (73.9% success rate)
- **Total Internal Markdown Links:** 70
- **Broken Internal Markdown Links:** 45 (35.7% success rate)
- **Total External Links:** 159 (not validated)

---

## Critical Issues

### 1. Missing `calendar/index.md`

**Impact:** HIGH - Referenced in 6 files

This is a missing index file for the calendar directory. Files referencing it:
- `/content/atlas/Atlas MOC.md` (line 65)
- `/content/calendar/Journey MOC.md` (line 118)
- `/content/calendar/consolidated.md` (line 1237)
- `/content/calendar/timeline.md` (line 119)
- `/content/efforts/Project Storyarc.md` (line 148)
- `/content/index.md` (lines 21, 71)

**Recommendation:** Create `/content/calendar/index.md` or update references to point to an existing calendar file like `Journey MOC.md`.

---

### 2. Broken Relative Path References in Content

**Impact:** MEDIUM - 45 broken internal markdown links

Many content files use relative paths with anchors (e.g., `../calendar/consolidated.md#day-01`). The file `consolidated.md` exists, but the anchor validation wasn't performed.

**Files Affected:**
- `/content/atlas/concepts/4Ms Framework.md` - 10 broken links to consolidated.md anchors
- `/content/atlas/concepts/AI Gemini Integration.md` - 4 broken links
- `/content/atlas/concepts/AI Integration.md` - 3 broken links
- `/content/atlas/concepts/AI Magic School Bot.md` - 3 broken links
- `/content/atlas/concepts/Design Thinking.md` - 8 broken links
- `/content/atlas/connections/Community Engagement.md` - 6 broken links
- `/content/efforts/Dollhouse Design.md` - 8 broken links

**Recommendation:** Verify that the anchor tags exist in `consolidated.md` for all day references (#day-01, #day-02, etc.).

---

### 3. Documentation Wikilinks (docs/)

**Impact:** HIGH - 248 broken wikilinks in documentation

The documentation files use wikilinks extensively but many don't resolve. Common patterns:

#### Missing Plugin/Feature Cross-References
Many docs reference plugins and features without the full path:
- `[[configuration]]` - used 34 times
- `[[layout]]` - used 10 times
- `[[authoring content]]` - used 7 times
- `[[build]]` - used 3 times

These may need to be:
- Full paths: `[[docs/configuration]]`
- Or relative paths: `[[../configuration]]`

#### Missing Image Files
- `[[quartz transform pipeline.png]]` - referenced in configuration.md
- `[[giscus-example.png]]`, `[[giscus-repo.png]]`, etc. - in comments.md
- `[[dns records.png]]` - in hosting.md
- `[[social-image-preview-light.png]]`, `[[social-image-preview-dark.png]]` - in social images.md
- And many more layout diagrams

**Recommendation:**
1. Check if images exist in a different location
2. Update wikilink syntax to include proper paths
3. Consider using markdown image syntax instead: `![alt](path/to/image.png)`

---

### 4. Content Wikilinks (content/)

**Impact:** MEDIUM - 34 broken wikilinks in content

Common issues:
- References to `calendar/index` (6 occurrences) - file doesn't exist
- Cross-references between concepts, tools, and connections - may need path corrections

---

## Detailed Breakdown by Category

### Broken Wikilinks by Directory

| Directory | Broken Links | Total Links | Success Rate |
|-----------|--------------|-------------|--------------|
| content/ | 34 | ~150 | ~77% |
| docs/ | 248 | ~931 | ~73% |

### Most Common Missing References

1. `[[configuration]]` - 34 occurrences
2. `[[layout]]` - 10 occurrences
3. `[[calendar/index]]` - 6 occurrences
4. `[[authoring content]]` - 7 occurrences
5. Various concept files in content/ - multiple occurrences

### Files with Most Broken Links

1. `/docs/configuration.md` - 23 broken wikilinks
2. `/docs/index.md` - 16 broken wikilinks
3. `/content/atlas/concepts/4Ms Framework MOC.md` - 20 broken wikilinks
4. `/content/atlas/concepts/Design Thinking MOC.md` - 16 broken wikilinks

---

## Broken Links by Type

### Type 1: Missing Files
Files that genuinely don't exist:
- `/content/calendar/index.md`
- Various plugin tag pages in docs/tags/

### Type 2: Incorrect Paths
Wikilinks that reference files with wrong paths:
- Most docs/ wikilinks need full paths or proper relative paths
- Some cross-directory references in content/

### Type 3: Missing Images
Image files referenced but not found:
- PNG files for documentation screenshots
- Diagram images

### Type 4: Malformed Markdown Links
- `/docs/advanced/architecture.md` line 12: Unclosed parenthesis in link
- `/docs/configuration.md` line 43: Unclosed parenthesis in link
- `/docs/layout.md` line 38: Wrong filename `component.md` should be `layout-components.md`

---

## Recommendations

### Immediate Actions

1. **Create missing index file:**
   - Create `/content/calendar/index.md` or update all references

2. **Fix malformed markdown links:**
   - Fix unclosed parentheses in docs/advanced/architecture.md
   - Fix unclosed parentheses in docs/configuration.md
   - Update component.md to layout-components.md in docs/layout.md

3. **Verify anchor links:**
   - Check that all `#day-XX` anchors exist in consolidated.md
   - Update or create missing anchors

### Medium-term Actions

1. **Standardize wikilink paths in docs/:**
   - Decide on a linking strategy (full paths vs relative)
   - Update all docs/ wikilinks to use consistent paths
   - Consider using Quartz's path resolution features

2. **Locate missing images:**
   - Search for PNG files that may be in different directories
   - Update image paths or add missing images
   - Consider using markdown syntax for images

3. **Fix cross-references in content/:**
   - Update wikilinks in atlas/ subdirectories
   - Ensure all MOC (Map of Content) files have correct links

### Long-term Actions

1. **Implement link validation in CI/CD:**
   - Add automated link checking to prevent future broken links
   - Use tools like `markdown-link-check` or similar

2. **Documentation:**
   - Create a linking guidelines document
   - Document the preferred wikilink syntax for this Quartz site

---

## External Links Summary

**Total External Links:** 159

External links were cataloged but not validated. They reference:
- Documentation sites (GitHub, MDN, etc.)
- Tool websites (Obsidian, Quartz, etc.)
- Showcase sites
- Third-party services

**Recommendation:** Use a link checker tool to validate external links periodically, as they can become outdated over time.

---

## Files Reference

### Content Files Analyzed
- 47 files in `/content/` directory
- Including: atlas/, calendar/, efforts/ subdirectories
- Main index: `/content/index.md`

### Documentation Files Analyzed
- 76 files in `/docs/` directory
- Including: advanced/, features/, plugins/, tags/ subdirectories
- Main index: `/docs/index.md`

---

## Next Steps

1. Review this report and prioritize fixes based on impact
2. Fix critical issues first (missing calendar/index.md, malformed links)
3. Systematically address wikilink path issues in docs/
4. Verify anchor references in consolidated.md
5. Re-run analysis after fixes to verify improvements

---

**Report generated by link analysis script**
**Location:** `/home/user/SteamEngine25/analyze_links.py`
**Full output:** `/home/user/SteamEngine25/link-analysis-report.txt`
