# HTML/JSX Patterns Reference Guide

This document extracts and explains all the reusable HTML/JSX patterns from the Quartz static site generator. These patterns can be adapted for use in other projects.

---

## Table of Contents

1. [Understanding the Component System](#understanding-the-component-system)
2. [Layout & Structure Patterns](#layout--structure-patterns)
3. [Navigation Patterns](#navigation-patterns)
4. [Content Display Patterns](#content-display-patterns)
5. [Sidebar Patterns](#sidebar-patterns)
6. [Interactive Patterns](#interactive-patterns)
7. [Utility/Layout Helper Patterns](#utilitylayout-helper-patterns)
8. [SVG Icon Patterns](#svg-icon-patterns)
9. [CSS Architecture](#css-architecture)
10. [Best Practices](#best-practices)

---

## Understanding the Component System

### What is a Component?

A **component** is a reusable piece of UI code. Think of it like a LEGO brick - you can combine many components to build a complete page.

### Basic Component Structure

Every component in this project follows this pattern:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

// Simple component (no configuration options)
const MyComponent: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return <div class={displayClass}>Hello World</div>
}

export default (() => MyComponent) satisfies QuartzComponentConstructor
```

### Component with Options

When you need configurable components:

```tsx
interface Options {
  title: string
  showIcon: boolean
}

const defaultOptions: Options = {
  title: "Default Title",
  showIcon: true,
}

export default ((userOpts?: Partial<Options>) => {
  const opts = { ...defaultOptions, ...userOpts }

  const MyComponent: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    return (
      <div class={displayClass}>
        {opts.showIcon && <span>Icon</span>}
        <h1>{opts.title}</h1>
      </div>
    )
  }

  return MyComponent
}) satisfies QuartzComponentConstructor
```

### Attaching CSS and JavaScript

Components can include their own styles and scripts:

```tsx
import style from "./styles/mycomponent.scss"
// @ts-ignore
import script from "./scripts/mycomponent.inline"

const MyComponent: QuartzComponent = (props) => {
  return <div>...</div>
}

// CSS that loads with the component
MyComponent.css = style

// JavaScript that runs BEFORE the DOM is ready (for critical setup)
MyComponent.beforeDOMLoaded = `
  console.log("Running before DOM ready")
`

// JavaScript that runs AFTER the DOM is ready (for interactivity)
MyComponent.afterDOMLoaded = script
```

### Component Props Explained

Every component receives these props:

| Prop | Type | Description |
|------|------|-------------|
| `ctx` | BuildCtx | Build context information |
| `cfg` | GlobalConfiguration | Site configuration (title, locale, etc.) |
| `fileData` | QuartzPluginData | Current page's metadata and content |
| `allFiles` | QuartzPluginData[] | All pages in the site |
| `displayClass` | string | Either "mobile-only" or "desktop-only" |
| `children` | Component[] | Child components to render |
| `tree` | Node | The HTML syntax tree |
| `externalResources` | StaticResources | CSS/JS resources |

---

## Layout & Structure Patterns

### 1. HTML Head Pattern

**Purpose:** Defines meta tags, fonts, stylesheets, and SEO information.

```tsx
// Pattern: HTML <head> with SEO meta tags
<head>
  <title>{title}</title>
  <meta charSet="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  {/* Open Graph (for social media sharing) */}
  <meta property="og:title" content={title} />
  <meta property="og:type" content="website" />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={imageUrl} />

  {/* Twitter Card */}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={title} />
  <meta name="twitter:description" content={description} />
  <meta name="twitter:image" content={imageUrl} />

  {/* Favicon */}
  <link rel="icon" href="/static/icon.png" />

  {/* Google Fonts (optional) */}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" />
  <link rel="stylesheet" href={googleFontUrl} />

  {/* Stylesheets */}
  {css.map(resource => <link rel="stylesheet" href={resource} />)}

  {/* Scripts (before DOM ready) */}
  {scripts.map(script => <script src={script} />)}
</head>
```

**When to use:** Every page needs a `<head>` section for proper SEO and resource loading.

---

### 2. Body Wrapper Pattern

**Purpose:** Simple container for page content with attached functionality.

```tsx
// Pattern: Main body wrapper
<div id="quartz-body">
  {children}
</div>
```

**Key insight:** The simplest components just wrap children in a container. The magic happens through attached CSS and JavaScript.

---

### 3. Header Pattern

**Purpose:** Page header with flexbox layout.

```tsx
// Pattern: Flexbox header
{children.length > 0 ? (
  <header>
    {children}
  </header>
) : null}
```

**CSS:**
```css
header {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 2rem 0;
  gap: 1.5rem;
}

header h1 {
  margin: 0;
  flex: auto;  /* Takes remaining space */
}
```

**Key insight:** Use conditional rendering - don't render empty containers.

---

### 4. Footer Pattern

**Purpose:** Page footer with links and attribution.

```tsx
// Pattern: Footer with dynamic links
<footer class={displayClass}>
  <p>
    Created with <a href="https://example.com">Framework</a> © {year}
  </p>
  <ul>
    {Object.entries(links).map(([text, link]) => (
      <li>
        <a href={link}>{text}</a>
      </li>
    ))}
  </ul>
</footer>
```

**Usage:**
```tsx
Component.Footer({
  links: {
    "GitHub": "https://github.com/user/repo",
    "Twitter": "https://twitter.com/user",
  }
})
```

---

## Navigation Patterns

### 1. Breadcrumb Navigation Pattern

**Purpose:** Shows the user's location in the site hierarchy.

```tsx
// Pattern: Breadcrumb navigation
<nav class="breadcrumb-container" aria-label="breadcrumbs">
  {crumbs.map((crumb, index) => (
    <div class="breadcrumb-element">
      <a href={crumb.path}>{crumb.displayName}</a>
      {index !== crumbs.length - 1 && (
        <p>{` ${spacerSymbol} `}</p>
      )}
    </div>
  ))}
</nav>
```

**Example Output:**
```
Home > Projects > My Project
```

**Key concepts:**
- Uses `<nav>` with `aria-label` for accessibility
- Spacer symbol is configurable (default: "❯")
- Last item doesn't get a spacer

---

### 2. File Explorer/Tree Pattern

**Purpose:** Collapsible folder tree for site navigation.

```tsx
// Pattern: File explorer with templates
<div
  class="explorer"
  data-behavior="link"         // What happens on click
  data-collapsed="collapsed"   // Default folder state
  data-savestate="true"        // Remember user's collapsed state
>
  {/* Mobile toggle button */}
  <button type="button" class="explorer-toggle mobile-explorer" data-mobile={true}>
    <svg class="lucide-menu">
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  </button>

  {/* Desktop collapsible section */}
  <button type="button" class="title-button explorer-toggle desktop-explorer">
    <h2>Explorer</h2>
    <svg class="fold">
      <polyline points="6 9 12 15 18 9" />
    </svg>
  </button>

  {/* Content container */}
  <div class="explorer-content" role="group">
    <ul class="explorer-ul" />
  </div>

  {/* Templates for dynamic rendering */}
  <template id="template-file">
    <li>
      <a href="#"></a>
    </li>
  </template>

  <template id="template-folder">
    <li>
      <div class="folder-container">
        <svg class="folder-icon">
          <polyline points="6 9 12 15 18 9" />
        </svg>
        <div>
          <button class="folder-button">
            <span class="folder-title"></span>
          </button>
        </div>
      </div>
      <div class="folder-outer">
        <ul class="content"></ul>
      </div>
    </li>
  </template>
</div>
```

**Key concepts:**
- Uses `data-*` attributes to pass configuration to JavaScript
- Uses `<template>` elements for dynamic content (cloned via JS)
- Separate mobile and desktop toggle buttons
- `aria-controls` links buttons to their controlled content

---

## Content Display Patterns

### 1. Article Title Pattern

**Purpose:** Display the main title of a page.

```tsx
// Pattern: Conditional title rendering
const title = fileData.frontmatter?.title

if (title) {
  return <h1 class="article-title">{title}</h1>
} else {
  return null  // Don't render if no title
}
```

**CSS:**
```css
.article-title {
  margin: 2rem 0 0 0;
}
```

**Key insight:** Always check if data exists before rendering.

---

### 2. Content Metadata Pattern

**Purpose:** Display page metadata (date, reading time, tags).

```tsx
// Pattern: Metadata with segments
<p class="content-meta">
  {/* Date segment */}
  {fileData.dates && (
    <Date date={getDate(cfg, fileData)} locale={cfg.locale} />
  )}

  {/* Reading time segment */}
  {showReadingTime && (
    <span>{readingTime} min read</span>
  )}
</p>
```

**Key concepts:**
- Uses an array of segments for flexibility
- Segments can be text or JSX elements
- CSS handles separators (commas) via `show-comma` attribute

---

### 3. Page List Pattern

**Purpose:** Display a list of pages with metadata and tags.

```tsx
// Pattern: Page list with tags
<ul class="section-ul">
  {pages.map((page) => (
    <li class="section-li">
      <div class="section">
        {/* Date */}
        <p class="meta">
          {page.dates && <Date date={date} locale={locale} />}
        </p>

        {/* Title with link */}
        <div class="desc">
          <h3>
            <a href={pageUrl} class="internal">
              {page.title}
            </a>
          </h3>
        </div>

        {/* Tags */}
        <ul class="tags">
          {page.tags.map((tag) => (
            <li>
              <a class="internal tag-link" href={`/tags/${tag}`}>
                {tag}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </li>
  ))}
</ul>
```

**Key concepts:**
- Use `class="internal"` for internal links (enables SPA navigation)
- Semantic HTML: `<ul>` for lists, `<h3>` for titles
- Tags are also a nested list

---

## Sidebar Patterns

### 1. Table of Contents Pattern

**Purpose:** Dynamic navigation for page sections.

#### Modern Style (Collapsible)
```tsx
// Pattern: Modern TOC with button toggle
<div class="toc">
  <button
    type="button"
    class="toc-header"
    aria-controls="toc-content-id"
    aria-expanded={!collapsed}
  >
    <h3>Table of Contents</h3>
    <svg class="fold">
      <polyline points="6 9 12 15 18 9" />
    </svg>
  </button>

  <ul id="toc-content-id" class="toc-content">
    {tocEntries.map((entry) => (
      <li class={`depth-${entry.depth}`}>
        <a href={`#${entry.slug}`} data-for={entry.slug}>
          {entry.text}
        </a>
      </li>
    ))}
  </ul>
</div>
```

#### Legacy Style (Details/Summary)
```tsx
// Pattern: Legacy TOC using native HTML collapsible
<details class="toc" open={!collapsed}>
  <summary>
    <h3>Table of Contents</h3>
  </summary>
  <ul>
    {tocEntries.map((entry) => (
      <li class={`depth-${entry.depth}`}>
        <a href={`#${entry.slug}`} data-for={entry.slug}>
          {entry.text}
        </a>
      </li>
    ))}
  </ul>
</details>
```

**Key concepts:**
- `depth-1`, `depth-2`, etc. classes for indentation
- `data-for` attribute links to heading IDs
- `aria-controls` and `aria-expanded` for accessibility
- Native `<details>/<summary>` provides no-JS collapsibility

---

### 2. Backlinks Pattern

**Purpose:** Show pages that link to the current page.

```tsx
// Pattern: Backlinks list
<div class="backlinks">
  <h3>Backlinks</h3>
  <ul>
    {backlinks.length > 0 ? (
      backlinks.map((file) => (
        <li>
          <a href={fileUrl} class="internal">
            {file.title}
          </a>
        </li>
      ))
    ) : (
      <li>No backlinks found</li>
    )}
  </ul>
</div>
```

**Key insight:** Always provide fallback content for empty states.

---

### 3. Graph Visualization Pattern

**Purpose:** Interactive knowledge graph showing page connections.

```tsx
// Pattern: Graph with local and global views
<div class="graph">
  <h3>Graph View</h3>

  {/* Local graph (connections to current page) */}
  <div class="graph-outer">
    <div
      class="graph-container"
      data-cfg={JSON.stringify(localGraphConfig)}
    />

    {/* Button to show global graph */}
    <button class="global-graph-icon" aria-label="Global Graph">
      <svg viewBox="0 0 55 55">
        {/* Complex path for network icon */}
      </svg>
    </button>
  </div>

  {/* Global graph (all pages) */}
  <div class="global-graph-outer">
    <div
      class="global-graph-container"
      data-cfg={JSON.stringify(globalGraphConfig)}
    />
  </div>
</div>
```

**Key concepts:**
- Pass complex configuration via `data-cfg` as JSON string
- JavaScript parses `data-cfg` and renders using D3.js
- Separate containers for local/global views

---

## Interactive Patterns

### 1. Search Pattern

**Purpose:** Full-text search with preview.

```tsx
// Pattern: Search with modal
<div class="search">
  {/* Trigger button */}
  <button class="search-button">
    <svg viewBox="0 0 19.9 19.7">
      <title>Search</title>
      <g class="search-path" fill="none">
        <path stroke-linecap="square" d="M18.5 18.3l-5.4-5.4" />
        <circle cx="8" cy="8" r="7" />
      </g>
    </svg>
    <p>Search</p>
  </button>

  {/* Search modal container */}
  <div class="search-container">
    <div class="search-space">
      <input
        autocomplete="off"
        class="search-bar"
        name="search"
        type="text"
        aria-label="Search"
        placeholder="Search..."
      />
      <div class="search-layout" data-preview={enablePreview} />
    </div>
  </div>
</div>
```

**Key concepts:**
- Button triggers modal/overlay
- `autocomplete="off"` prevents browser suggestions
- Results rendered dynamically into `.search-layout`

---

### 2. Dark Mode Toggle Pattern

**Purpose:** Switch between light and dark themes.

```tsx
// Pattern: Theme toggle with sun/moon icons
<button class="darkmode">
  {/* Sun icon (shown in dark mode, switches to light) */}
  <svg class="dayIcon" viewBox="0 0 35 35" aria-label="Dark mode">
    <title>Dark mode</title>
    <path d="M6,17.5C6,16.672..." />  {/* Sun with rays */}
  </svg>

  {/* Moon icon (shown in light mode, switches to dark) */}
  <svg class="nightIcon" viewBox="0 0 100 100" aria-label="Light mode">
    <title>Light mode</title>
    <path d="M96.76,66.458..." />  {/* Crescent moon */}
  </svg>
</button>
```

**JavaScript approach:**
```js
// beforeDOMLoaded (runs immediately, prevents flash)
const theme = localStorage.getItem("theme") ?? "light"
document.documentElement.setAttribute("data-theme", theme)

// Click handler
button.onclick = () => {
  const current = document.documentElement.getAttribute("data-theme")
  const next = current === "light" ? "dark" : "light"
  document.documentElement.setAttribute("data-theme", next)
  localStorage.setItem("theme", next)
}
```

**Key concepts:**
- Two SVG icons, CSS shows/hides based on theme
- `beforeDOMLoaded` prevents flash of wrong theme
- Theme stored in `localStorage`

---

### 3. Reader Mode Toggle Pattern

**Purpose:** Simplified reading view (hides sidebars).

```tsx
// Pattern: Reader mode toggle
<button class="readermode">
  <svg class="readerIcon" viewBox="0 0 24 24" aria-label="Reader mode">
    <title>Reader mode</title>
    <g transform="translate(-1.8, -1.8) scale(1.15, 1.2)">
      <path d="M8.989..." />  {/* Open book icon */}
    </g>
  </svg>
</button>
```

**Key concepts:**
- Similar pattern to dark mode
- Toggles a class on `<body>` that CSS uses to hide/show elements

---

## Utility/Layout Helper Patterns

### 1. Flex Container Pattern

**Purpose:** Compose multiple components in a flexible row/column.

```tsx
// Pattern: Configurable flexbox container
<div
  class="flex-component"
  style={`flex-direction: ${direction}; flex-wrap: ${wrap}; gap: ${gap};`}
>
  {components.map((c) => (
    <div style={`
      flex-grow: ${c.grow ? 1 : 0};
      flex-shrink: ${c.shrink ? 1 : 0};
      flex-basis: ${c.basis ?? 'auto'};
      order: ${c.order ?? 0};
      align-self: ${c.align ?? 'center'};
    `}>
      <c.Component {...props} />
    </div>
  ))}
</div>
```

**Usage:**
```tsx
Component.Flex({
  components: [
    { Component: Component.Search(), grow: true },
    { Component: Component.Darkmode() },
    { Component: Component.ReaderMode() },
  ],
  direction: "row",
  gap: "1rem",
})
```

---

### 2. Spacer Pattern

**Purpose:** Create flexible empty space.

```tsx
// Pattern: Simple spacer
<div class="spacer"></div>
```

**CSS:**
```css
.spacer {
  flex: 1 1 auto;  /* Grow to fill available space */
}
```

---

### 3. Mobile/Desktop Only Patterns

**Purpose:** Show components only on specific screen sizes.

```tsx
// Pattern: Higher-order component for responsive display
const MobileOnly = (component: QuartzComponent) => {
  return (props) => <Component displayClass="mobile-only" {...props} />
}

const DesktopOnly = (component: QuartzComponent) => {
  return (props) => <Component displayClass="desktop-only" {...props} />
}
```

**CSS:**
```css
@media (min-width: 1000px) {
  .mobile-only { display: none !important; }
}

@media (max-width: 999px) {
  .desktop-only { display: none !important; }
}
```

**Usage:**
```tsx
Component.MobileOnly(Component.Spacer())   // Only on mobile
Component.DesktopOnly(Component.TableOfContents())  // Only on desktop
```

---

### 4. Overflow List Pattern

**Purpose:** List that shows gradient when content is cut off.

```tsx
// Pattern: List with overflow indicator
<ul class="overflow" id="unique-id">
  {children}
  <li class="overflow-end" />  {/* Sentinel element */}
</ul>
```

**JavaScript:**
```js
// Detect when sentinel is visible/hidden
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    const parentUl = entry.target.parentElement
    if (entry.isIntersecting) {
      parentUl.classList.remove("gradient-active")
    } else {
      parentUl.classList.add("gradient-active")
    }
  }
})

const end = document.querySelector(".overflow-end")
observer.observe(end)
```

**Key concepts:**
- Hidden sentinel element at end of list
- IntersectionObserver detects if sentinel is visible
- If not visible, content is overflowing - show gradient

---

## SVG Icon Patterns

### Hamburger Menu Icon
```tsx
<svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="4" x2="20" y1="6" y2="6" />
  <line x1="4" x2="20" y1="12" y2="12" />
  <line x1="4" x2="20" y1="18" y2="18" />
</svg>
```

### Chevron/Arrow Icon
```tsx
<svg width="14" height="14" viewBox="5 8 14 8" fill="none" stroke="currentColor" stroke-width="2">
  <polyline points="6 9 12 15 18 9" />
</svg>
```

### Search Icon
```tsx
<svg viewBox="0 0 19.9 19.7">
  <g fill="none">
    <path stroke-linecap="square" d="M18.5 18.3l-5.4-5.4" />
    <circle cx="8" cy="8" r="7" />
  </g>
</svg>
```

### Common SVG Attributes
```tsx
<svg
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"              // No fill (outline only)
  stroke="currentColor"    // Uses CSS color
  stroke-width="2"
  stroke-linecap="round"   // Rounded line ends
  stroke-linejoin="round"  // Rounded corners
>
```

---

## CSS Architecture

### CSS Custom Properties (Variables)

```css
:root {
  /* Colors */
  --light: #faf8f8;
  --dark: #282828;
  --gray: #b8b8b8;

  /* Typography */
  --bodyFont: 'Source Sans Pro', sans-serif;
  --headerFont: 'Schibsted Grotesk', sans-serif;
  --codeFont: 'IBM Plex Mono', monospace;

  /* Spacing */
  --pagePadding: 2rem;
  --gap: 1rem;
}

/* Dark mode overrides */
[data-theme="dark"] {
  --light: #282828;
  --dark: #faf8f8;
}
```

### Component Scoping Pattern

Each component's CSS is scoped by class name:

```css
/* explorer.scss */
.explorer {
  /* Component container styles */
}

.explorer .explorer-toggle {
  /* Nested element styles */
}

.explorer .folder-container {
  /* More nested styles */
}
```

---

## Best Practices

### 1. Accessibility

```tsx
// Use semantic HTML
<nav aria-label="breadcrumbs">...</nav>
<button aria-controls="menu-id" aria-expanded={isOpen}>...</button>

// Provide text alternatives
<svg aria-label="Search"><title>Search</title>...</svg>
<img alt="Description of image" />

// Use proper heading hierarchy
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### 2. Performance

```tsx
// Conditional rendering - don't render empty elements
{items.length > 0 && <ul>...</ul>}

// Return null for empty components
if (!data) return null

// Use beforeDOMLoaded for critical setup (prevents flash)
Component.beforeDOMLoaded = `
  // Runs immediately, before page renders
`
```

### 3. Data Attributes

```tsx
// Pass configuration to JavaScript
<div
  data-collapsed="true"
  data-config={JSON.stringify(complexConfig)}
>

// Read in JavaScript
const collapsed = element.dataset.collapsed === "true"
const config = JSON.parse(element.dataset.config)
```

### 4. Template Elements

```tsx
// Define templates in HTML
<template id="template-item">
  <li><a href="#"></a></li>
</template>

// Clone in JavaScript
const template = document.getElementById("template-item")
const clone = template.content.cloneNode(true)
clone.querySelector("a").href = url
clone.querySelector("a").textContent = title
container.appendChild(clone)
```

### 5. Event Delegation

```js
// Instead of adding listeners to each item
document.addEventListener("nav", () => {
  // Handle navigation events
})

// Use delegation for dynamic content
container.addEventListener("click", (e) => {
  if (e.target.matches(".item-button")) {
    // Handle click
  }
})
```

---

## Quick Reference: Component Patterns Summary

| Pattern | HTML Element | Key Classes | Purpose |
|---------|--------------|-------------|---------|
| Head | `<head>` | - | SEO, resources |
| Body | `<div>` | `#quartz-body` | Content wrapper |
| Header | `<header>` | - | Page header |
| Footer | `<footer>` | - | Page footer |
| Breadcrumbs | `<nav>` | `.breadcrumb-container` | Navigation path |
| Explorer | `<div>` | `.explorer` | File tree |
| Article Title | `<h1>` | `.article-title` | Page title |
| Content Meta | `<p>` | `.content-meta` | Date, reading time |
| Page List | `<ul>` | `.section-ul` | List of pages |
| TOC | `<div>` | `.toc` | Table of contents |
| Backlinks | `<div>` | `.backlinks` | Incoming links |
| Graph | `<div>` | `.graph` | Knowledge graph |
| Search | `<div>` | `.search` | Search interface |
| Darkmode | `<button>` | `.darkmode` | Theme toggle |
| Reader Mode | `<button>` | `.readermode` | Reading mode |
| Flex | `<div>` | `.flex-component` | Layout container |
| Spacer | `<div>` | `.spacer` | Empty space |
| Mobile Only | - | `.mobile-only` | Mobile display |
| Desktop Only | - | `.desktop-only` | Desktop display |
| Overflow List | `<ul>` | `.overflow` | Scrollable list |

---

## Using These Patterns in Other Projects

1. **Copy the component structure** - The TypeScript component pattern works with any JSX framework
2. **Adapt for your framework** - Convert JSX to React, Vue, Svelte, etc.
3. **Extract the CSS** - The SCSS patterns work standalone
4. **Use the JavaScript patterns** - Data attributes, IntersectionObserver, localStorage work everywhere

Example conversion to React:

```tsx
// Quartz pattern
const Breadcrumbs: QuartzComponent = ({ fileData }) => {
  return <nav class="breadcrumb-container">...</nav>
}
Breadcrumbs.css = style

// React equivalent
import "./breadcrumbs.css"
function Breadcrumbs({ path }) {
  return <nav className="breadcrumb-container">...</nav>
}
```

---

*This document was generated by analyzing the Quartz v4 codebase. All patterns are production-tested and can be freely adapted for other projects.*
