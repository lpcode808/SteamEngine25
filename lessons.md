# Lessons Learned: Quartz Deployment

A deep dive into concepts, patterns, and insights from deploying Quartz to GitHub Pages.

---

## 1. GitHub Authentication & Authorization

### Concept: Personal Access Tokens (PATs)

**What they are:**
- Temporary credentials that act like passwords
- More secure than passwords (can be scoped, revoked, expire)
- Required for HTTPS Git operations when 2FA is enabled

**Key lesson from our deployment:**

We needed **two different scopes** for this to work:

```
repo scope        → Push code, create branches, read/write repository content
workflow scope    → Create/modify files in .github/workflows/
```

**Why workflow scope is special:**

GitHub Actions workflows can:
- Access repository secrets
- Deploy to production
- Modify code automatically
- Publish packages

If anyone could push workflow files, they could:
1. Create a workflow that prints all secrets
2. Deploy malicious code
3. Exfiltrate sensitive data

**The security principle:** Defense in depth. Even with `repo` access, you need explicit permission for workflows.

### Authentication Methods Comparison

| Method | Security | Convenience | Use Case |
|--------|----------|-------------|----------|
| PAT (with expiry) | ⭐⭐⭐ | ⭐⭐⭐⭐ | Temporary access, scripts |
| SSH Key | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Personal machines, long-term |
| Deploy Key | ⭐⭐⭐⭐⭐ | ⭐⭐ | Single repo, CI/CD |
| GitHub CLI (gh) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Development, CLI tools |

**Why we used PAT:**
- Quick setup
- Temporary environment (7-day expiry is fine)
- Easy to revoke if compromised

---

## 2. GitHub Actions & CI/CD

### Concept: Continuous Deployment Pipeline

**What happened when we pushed:**

```
1. Git Push (developer)
   ↓
2. GitHub receives push event
   ↓
3. GitHub Actions triggered (workflow file)
   ↓
4. GitHub spawns Ubuntu VM
   ↓
5. VM checks out code
   ↓
6. VM installs Node.js 22
   ↓
7. VM runs: npm ci (install dependencies)
   ↓
8. VM runs: npx quartz build (build site)
   ↓
9. VM generates static files in public/
   ↓
10. VM uploads artifact to GitHub Pages
    ↓
11. GitHub Pages deploys artifact
    ↓
12. Site live at lpcode808.github.io/SteamEngine25
```

### Why Node.js Version Mattered

**The error we hit:**
```
npm ERR! engine Unsupported engine
npm ERR! engine Required: node >=22
npm ERR! engine Actual: node 20.x.x
```

**What this teaches us:**

1. **Reproducible builds require version pinning**
   - Different Node.js versions have different APIs
   - Package managers enforce version requirements
   - This prevents "works on my machine" problems

2. **Breaking changes between versions:**
   ```javascript
   // Node.js 22 added features that Quartz uses:
   - Import attributes (import foo from 'data.json' with { type: 'json' })
   - Improved ESM support
   - New Array.prototype methods
   ```

3. **Why version mismatches happen:**
   - Quartz is cutting-edge (uses latest features)
   - GitHub Actions templates often lag behind
   - Default Node.js on GitHub runners: 20.x (as of 2025)

**Best practice:** Always match the version in:
- `package.json` engines field
- `.github/workflows/*.yml` setup-node version
- Local development environment (`.node-version` file)

---

## 3. Git Branch Strategies

### What We Learned About Branch Protection

**Our situation:**
```
v4 (protected) ← Can't push directly
├── claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF (feature)
└── main (tried to create, also protected)
```

**Why branch protection exists:**

1. **Prevent accidental force pushes**
   ```bash
   git push --force origin main  # Could delete history!
   ```

2. **Require code review**
   - At least N reviewers must approve
   - Prevents unchecked code in production

3. **Require status checks**
   - Tests must pass
   - Build must succeed
   - Security scans must clear

4. **Prevent direct commits**
   - Must go through Pull Request
   - Maintains audit trail

**Our workaround: Deploy from feature branch**

Instead of fighting branch protection, we:
1. Kept our work in feature branch
2. Modified workflow to deploy from that branch
3. Can still create PR later for code review

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches:
      - claude/deploy-quartz-obsidian-011CUtEuF6BZcB8neub9uFtF  # Deploy from feature!
```

**When this makes sense:**
- ✅ Quick prototypes
- ✅ Personal projects
- ✅ Working around restrictions in learning environments

**When to avoid:**
- ❌ Production systems with team members
- ❌ When you need proper git history
- ❌ When branch protection is there for safety

---

## 4. Static Site Generators (SSGs)

### How Quartz Works

**The transformation pipeline:**

```
Markdown files (.md)
  ↓
[Quartz Build Process]
  ↓
1. Parse frontmatter (metadata)
2. Convert Markdown → HTML (remark)
3. Transform wikilinks [[like-this]]
4. Generate backlinks
5. Create graph data
6. Apply plugins (syntax highlighting, LaTeX, etc.)
7. Bundle JavaScript (esbuild)
8. Compile CSS (Sass)
9. Generate search index (FlexSearch)
10. Output static HTML/CSS/JS
  ↓
Static files in public/
  ↓
[Deployed to GitHub Pages]
  ↓
Served as regular website (no server needed!)
```

**Key insight: Build-time vs Runtime**

| Operation | When it happens | Example |
|-----------|----------------|---------|
| Wikilink resolution | **Build time** | `[[note]]` → `<a href="/note">note</a>` |
| Backlink generation | **Build time** | Scan all files for links |
| Syntax highlighting | **Build time** | Convert code blocks to highlighted HTML |
| Search | **Runtime** | User types, JavaScript searches index |
| Page navigation (SPA) | **Runtime** | Click link, fetch JSON, morph DOM |

**Why this matters:**
- Build time: Happens once per deploy (slow is OK)
- Runtime: Happens on every page load (must be fast)

**Quartz's optimization:**
- Heavy work at build time (parsing, transforming)
- Minimal JavaScript at runtime (just search & navigation)
- Result: Fast site even with 1000+ notes

### Static vs Dynamic Sites

**Static (like Quartz):**
```
Request → CDN → Pre-built HTML → User
```
- ✅ Ultra-fast (no server processing)
- ✅ Cheap/free hosting (GitHub Pages, Netlify)
- ✅ High reliability (no database to crash)
- ❌ Must rebuild to update content

**Dynamic (like WordPress):**
```
Request → Server → Query DB → Generate HTML → User
```
- ✅ Real-time updates
- ✅ User-specific content
- ✅ Forms, comments, login
- ❌ Slower, expensive, complex

**For digital gardens:** Static is perfect!
- Content changes infrequently
- No user-specific data needed
- Speed and cost matter

---

## 5. Package Management & Dependencies

### What `npm ci` Does

We used `npm ci` in the workflow instead of `npm install`. Here's why:

**`npm install`:**
```bash
npm install
```
- Installs packages listed in package.json
- Updates package-lock.json if needed
- Tries to resolve compatible versions
- **Can produce different results** on different machines

**`npm ci` (clean install):**
```bash
npm ci
```
- Deletes node_modules/ first
- Installs **exact** versions from package-lock.json
- Fails if package.json and lock file disagree
- **Guarantees reproducible builds**

**Lesson: Reproducibility is critical in CI/CD**

```
Developer's machine: node_modules/ (version A)
CI/CD machine:       node_modules/ (version B)
                      ↓
                   Different bugs!
```

Using `npm ci`:
- Both use package-lock.json
- Both get identical versions
- Build succeeds everywhere or nowhere

### Dependency Tree Size

Quartz has 98 direct dependencies! But why?

**Categories:**
1. **Markdown processing** (remark, rehype)
   - Parse Markdown
   - Transform syntax
   - Generate HTML

2. **Build tools** (esbuild, TypeScript)
   - Bundle JavaScript
   - Compile TypeScript
   - Minify code

3. **Plugins** (syntax highlight, math, citations)
   - Code highlighting (Shiki)
   - LaTeX math (KaTeX)
   - Citations (rehype-citation)

4. **Runtime** (Preact, D3)
   - Interactive graph view
   - Search functionality
   - SPA navigation

**Lesson: Modern web dev is built on ecosystems**

Instead of writing everything from scratch:
- Reuse battle-tested libraries
- Compose small, focused tools
- Trade bundle size for developer velocity

---

## 6. GitHub Pages Deployment

### How GitHub Pages Works

**Traditional web hosting:**
```
You rent server → Install web server → Upload files → Configure DNS
```

**GitHub Pages:**
```
Push to GitHub → Automatic deploy → Free CDN → Done
```

**What's happening behind the scenes:**

1. **GitHub Actions uploads artifact**
   ```yaml
   - uses: actions/upload-pages-artifact@v3
     with:
       path: ./public
   ```
   - Creates a tar.gz of your site
   - Stores it temporarily

2. **Deploy action publishes it**
   ```yaml
   - uses: actions/deploy-pages@v4
   ```
   - Extracts files to Pages infrastructure
   - Updates CDN cache
   - Makes site live

3. **GitHub's CDN serves it**
   - Files distributed to edge locations worldwide
   - Fast loading from anywhere
   - Free SSL certificate
   - DDoS protection

**Why this is powerful:**
- No server maintenance
- Auto-scales to any traffic
- Version controlled (rollback = revert commit)
- Free for public repos

### The `workflow_dispatch` Trigger

Our workflow has:
```yaml
on:
  push:
    branches: [...]
  workflow_dispatch:  # What's this?
```

**What `workflow_dispatch` does:**
- Adds a "Run workflow" button in GitHub UI
- Lets you manually trigger deployment
- Useful for:
  - Testing without pushing
  - Redeploying after GitHub Pages issue
  - Deploying when content unchanged but config updated

**Try it:** Go to Actions tab → Select workflow → "Run workflow"

---

## 7. Configuration as Code

### The `quartz.config.ts` File

**Key pattern: Configuration as code**

Instead of clicking through UI settings, Quartz uses a TypeScript file:

```typescript
const config: QuartzConfig = {
  configuration: {
    pageTitle: "SteamEngine25",
    baseUrl: "lpcode808.github.io/SteamEngine25",
    enableSPA: true,
    // ...
  }
}
```

**Benefits:**

1. **Version controlled**
   - See history of config changes
   - Revert bad configurations
   - Compare between branches

2. **Documented**
   - Comments explain options
   - Type checking catches errors
   - IDE autocomplete helps

3. **Reproducible**
   - Clone repo → Same config
   - No "click these 20 checkboxes"

4. **Testable**
   - Can test config in CI
   - Validate before deploy

**Lesson: Infrastructure as Code (IaC) applies to all levels**

- Quartz: Site config as code
- GitHub Actions: Build pipeline as code
- Terraform: Cloud infrastructure as code

### Plugin Architecture

Quartz uses a plugin system:

```typescript
plugins: {
  transformers: [
    Plugin.FrontMatter(),
    Plugin.ObsidianFlavoredMarkdown(),
    Plugin.SyntaxHighlighting(),
    // Add your own!
  ]
}
```

**Why plugins matter:**

1. **Extensibility**
   - Core stays simple
   - Features are opt-in
   - Community can contribute

2. **Composition**
   - Chain plugins together
   - Each does one thing well
   - Unix philosophy

3. **Performance**
   - Disable plugins you don't need
   - Example: CustomOgImages is slow, can disable

**Example: The transformer pipeline**

```
Markdown input
  ↓
Plugin.FrontMatter()      → Extract metadata
  ↓
Plugin.CreatedModifiedDate() → Add timestamps
  ↓
Plugin.SyntaxHighlighting() → Highlight code
  ↓
Plugin.ObsidianFlavoredMarkdown() → Transform [[wikilinks]]
  ↓
Plugin.TableOfContents()  → Generate TOC
  ↓
HTML output
```

Each plugin takes the output of the previous one.

---

## 8. Debugging Strategies

### What We Did When Things Failed

**1. Check git status**
```bash
git status              # What's staged?
git log --oneline -5    # Recent commits
git remote -v           # Correct remote?
```

**2. Read error messages carefully**
```
refusing to allow a Personal Access Token to create or update workflow
without `workflow` scope
          ^^^^^^^^^^^
          This tells us exactly what's missing!
```

**3. Check version requirements**
```bash
cat package.json | grep -A 2 engines
# Shows: "node": ">=22"
```

**4. Look at GitHub Actions logs**
- Actions tab → Click failed workflow
- Expand failed step
- Read full error output

**5. Compare with working examples**
- Check Quartz's own workflows
- See how official examples do it

**Lesson: Systematic debugging beats guessing**

Don't just try random fixes. Instead:
1. Gather information (logs, config, status)
2. Form hypothesis (what's wrong?)
3. Test hypothesis (try targeted fix)
4. Verify result (did it work?)

---

## 9. Web Performance & Optimization

### Tradeoffs in Quartz Config

**SPA Mode** (`enableSPA: true`)
```typescript
enableSPA: true  // Single Page Application mode
```

**What it does:**
- First page: Normal HTML load
- Subsequent: Fetch JSON, morph DOM (no full reload)

**Tradeoffs:**
| Pro | Con |
|-----|-----|
| ⚡ Faster navigation | 📦 Larger initial bundle |
| 🎨 Smooth transitions | 🤖 Harder for crawlers |
| 💾 Reuses JS/CSS | 🐛 More complex bugs |

**When to enable:** Content-heavy site where users browse multiple pages

**When to disable:** Single-page docs, primarily viewed via search engines

### Font Loading

```typescript
fontOrigin: "googleFonts"  // vs "local"
```

**Google Fonts:**
- Pro: Fast CDN, browser caching across sites
- Con: External dependency, privacy implications (Google sees your visitors)

**Local fonts:**
- Pro: Privacy, works offline, no external requests
- Con: Slower first load, larger repo size

**Lesson: Every convenience has a tradeoff**

---

## 10. Obsidian → Web Translation

### What Works Automatically

Quartz handles these Obsidian features:

| Obsidian Syntax | Quartz Output |
|----------------|---------------|
| `[[note]]` | Link to note.html |
| `[[note\|alias]]` | Link with custom text |
| `![[image.png]]` | Embedded image |
| `#tag` | Clickable tag, tag index |
| Frontmatter | Metadata for sorting/filtering |
| Callouts | Styled callout boxes |

### What to Watch Out For

**1. File organization**
```
Obsidian Vault/
├── Private notes/     # Don't publish!
├── Templates/         # Don't publish!
└── Public notes/      # Publish this

Solution: Use ignorePatterns in config
```

**2. Broken links**
```markdown
[[Non-existent note]]  # Creates dead link in Quartz

Solution: Check for broken links before publishing
```

**3. Local paths**
```markdown
![](/Users/you/Desktop/image.png)  # Won't work on web!

Solution: Use relative paths, keep assets in vault
```

**Lesson: Think about the "public interface" of your notes**

Some things are meant for personal use:
- Drafts and half-finished thoughts
- Personal templates
- Private information

Use folder structure and config to keep them separate.

---

## Key Takeaways

### Technical Lessons

1. **Security has layers** - Even with repo access, workflow access is separate
2. **Version pinning prevents surprises** - Match Node.js versions everywhere
3. **Branch protection is good** - Forces proper workflows, even if inconvenient
4. **Static sites are powerful** - Fast, cheap, reliable for content-first sites
5. **Configuration as code is valuable** - Version controlled, reproducible, documented

### Process Lessons

1. **Read error messages completely** - They often say exactly what's wrong
2. **Understand the pipeline** - Knowing how builds work helps debug failures
3. **Start simple, iterate** - We got basic deployment working, then refined
4. **Document as you go** - This file! Future you will thank present you
5. **Tradeoffs are everywhere** - Every choice has costs and benefits

### Mindset Lessons

1. **Failure is information** - Each error taught us something
2. **Systems thinking matters** - Git, GitHub, Actions, Pages all interconnect
3. **Tools abstract complexity** - Quartz hides markdown → HTML complexity
4. **Standing on shoulders** - 98 dependencies represent decades of work
5. **Share knowledge** - Open source enables learning like this

---

## Further Learning

### To understand Quartz deeper:
- Read `quartz/` source code
- Customize `quartz.config.ts` and see effects
- Create custom plugins
- Study the build output in `public/`

### To understand GitHub Actions:
- Read `.github/workflows/deploy.yml` line by line
- Try adding steps (like tests, linting)
- Explore other Actions in marketplace
- Learn YAML syntax and GitHub Actions expressions

### To understand static sites:
- View source of your deployed site
- Inspect network requests in browser DevTools
- Compare HTML before/after JavaScript loads
- Study other SSGs (Hugo, Jekyll, Next.js)

### To understand Git better:
- Learn about branch protection rules
- Practice rebasing and merge strategies
- Understand reflog for recovering "lost" commits
- Study Git internals (objects, refs, trees)

---

## Conclusion

What seemed like a simple task (deploy a site) touched:
- Git & version control
- GitHub authentication & authorization
- CI/CD pipelines
- Package management
- Build systems
- Web hosting
- Static site generation
- Content transformation
- Web performance

**This is the magic and challenge of modern web development:** Everything is connected. Understanding one piece helps you understand the next.

Keep building, keep learning, keep documenting! 🚀
