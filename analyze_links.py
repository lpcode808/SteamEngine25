#!/usr/bin/env python3
"""
Analyze markdown files for broken links in a Quartz-based site.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import unquote

# Repository root
REPO_ROOT = Path("/home/user/SteamEngine25")

# Regex patterns
WIKILINK_PATTERN = r'\[\[([^\]]+?)\]\]'  # [[link]] or [[link|display]]
MARKDOWN_LINK_PATTERN = r'\[([^\]]+)\]\(([^\)]+)\)'  # [text](url)

def get_all_markdown_files():
    """Get all markdown files in content/ and docs/ directories."""
    md_files = []
    for directory in ['content', 'docs']:
        dir_path = REPO_ROOT / directory
        if dir_path.exists():
            md_files.extend(dir_path.rglob('*.md'))
    return md_files

def extract_wikilinks(content):
    """Extract wikilinks from content."""
    matches = re.findall(WIKILINK_PATTERN, content)
    wikilinks = []
    for match in matches:
        # Split by | to handle [[link|display text]]
        link = match.split('|')[0].strip()
        # Remove anchor links
        link = link.split('#')[0].strip()
        if link:
            wikilinks.append(link)
    return wikilinks

def extract_markdown_links(content):
    """Extract markdown links from content."""
    matches = re.findall(MARKDOWN_LINK_PATTERN, content)
    return [(text.strip(), url.strip()) for text, url in matches]

def find_wikilink_file(wikilink, repo_root):
    """
    Find if a wikilink corresponds to an existing file.
    Quartz supports case-insensitive matching and looks for files in content/.
    """
    # Normalize the wikilink
    target = wikilink.strip()

    # Search in content directory
    content_dir = repo_root / 'content'

    # Try exact match with .md extension
    possible_paths = [
        content_dir / f"{target}.md",
        content_dir / target,  # Maybe already has .md
    ]

    # Also search recursively for the file name
    for md_file in content_dir.rglob('*.md'):
        # Check if the file name (without .md) matches
        if md_file.stem == target:
            return md_file
        # Check if the full relative path matches
        rel_path = md_file.relative_to(content_dir)
        # Without extension
        if str(rel_path.with_suffix('')) == target:
            return md_file
        # With extension
        if str(rel_path) == target:
            return md_file

    return None

def find_markdown_link_file(url, source_file, repo_root):
    """Find if an internal markdown link corresponds to an existing file."""
    # Skip external links
    if url.startswith('http://') or url.startswith('https://'):
        return None, 'external'

    # Skip mailto, anchor-only, and other special protocols
    if url.startswith('mailto:') or url.startswith('#') or url.startswith('data:'):
        return None, 'skip'

    # Remove query strings and anchors
    url = url.split('?')[0].split('#')[0]

    if not url:
        return None, 'skip'

    # URL decode
    url = unquote(url)

    # Handle relative paths
    if url.startswith('/'):
        # Absolute path from repo root
        target = repo_root / url.lstrip('/')
    else:
        # Relative to current file
        target = source_file.parent / url

    # Normalize the path
    try:
        target = target.resolve()
    except:
        return None, 'invalid'

    # Check if file exists
    if target.exists():
        return target, 'found'

    # Try adding .md if not present
    if not target.suffix:
        md_target = target.with_suffix('.md')
        if md_target.exists():
            return md_target, 'found'

    return None, 'not_found'

def analyze_file(file_path, repo_root):
    """Analyze a single markdown file for links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            content = ''.join(lines)
    except Exception as e:
        return {
            'error': str(e),
            'wikilinks': [],
            'markdown_links': [],
            'external_links': []
        }

    # Extract wikilinks
    wikilinks = []
    for line_num, line in enumerate(lines, 1):
        matches = re.finditer(WIKILINK_PATTERN, line)
        for match in matches:
            link_text = match.group(1)
            link = link_text.split('|')[0].strip()
            link = link.split('#')[0].strip()
            if link:
                wikilinks.append({
                    'link': link,
                    'raw': match.group(0),
                    'line': line_num
                })

    # Extract markdown links
    markdown_links = []
    external_links = []
    for line_num, line in enumerate(lines, 1):
        matches = re.finditer(MARKDOWN_LINK_PATTERN, line)
        for match in matches:
            text = match.group(1).strip()
            url = match.group(2).strip()

            if url.startswith('http://') or url.startswith('https://'):
                external_links.append({
                    'text': text,
                    'url': url,
                    'line': line_num
                })
            elif not url.startswith('mailto:') and not url.startswith('#') and not url.startswith('data:'):
                markdown_links.append({
                    'text': text,
                    'url': url,
                    'raw': match.group(0),
                    'line': line_num
                })

    return {
        'wikilinks': wikilinks,
        'markdown_links': markdown_links,
        'external_links': external_links
    }

def main():
    """Main analysis function."""
    print("Analyzing markdown files for broken links...")
    print(f"Repository: {REPO_ROOT}")
    print()

    # Get all markdown files
    md_files = get_all_markdown_files()
    print(f"Found {len(md_files)} markdown files to analyze")
    print()

    # Data structures for results
    broken_wikilinks = []
    broken_markdown_links = []
    all_external_links = set()

    stats = {
        'total_files': len(md_files),
        'total_wikilinks': 0,
        'broken_wikilinks': 0,
        'total_internal_md_links': 0,
        'broken_md_links': 0,
        'total_external_links': 0
    }

    # Analyze each file
    for file_path in sorted(md_files):
        rel_path = file_path.relative_to(REPO_ROOT)
        analysis = analyze_file(file_path, REPO_ROOT)

        if 'error' in analysis:
            print(f"Error analyzing {rel_path}: {analysis['error']}")
            continue

        # Check wikilinks
        for wikilink in analysis['wikilinks']:
            stats['total_wikilinks'] += 1
            target_file = find_wikilink_file(wikilink['link'], REPO_ROOT)
            if target_file is None:
                stats['broken_wikilinks'] += 1
                broken_wikilinks.append({
                    'source': str(rel_path),
                    'link': wikilink['link'],
                    'raw': wikilink['raw'],
                    'line': wikilink['line']
                })

        # Check internal markdown links
        for md_link in analysis['markdown_links']:
            stats['total_internal_md_links'] += 1
            target_file, status = find_markdown_link_file(md_link['url'], file_path, REPO_ROOT)
            if status == 'not_found' or status == 'invalid':
                stats['broken_md_links'] += 1
                broken_markdown_links.append({
                    'source': str(rel_path),
                    'text': md_link['text'],
                    'url': md_link['url'],
                    'raw': md_link['raw'],
                    'line': md_link['line']
                })

        # Collect external links
        for ext_link in analysis['external_links']:
            stats['total_external_links'] += 1
            all_external_links.add((ext_link['url'], str(rel_path), ext_link['line']))

    # Print results
    print("=" * 80)
    print("LINK ANALYSIS REPORT")
    print("=" * 80)
    print()

    # Section 1: Broken Wikilinks
    print("1. BROKEN WIKILINKS")
    print("-" * 80)
    if broken_wikilinks:
        # Group by source file
        by_file = defaultdict(list)
        for item in broken_wikilinks:
            by_file[item['source']].append(item)

        for source in sorted(by_file.keys()):
            print(f"\n{source}:")
            for item in by_file[source]:
                print(f"  Line {item['line']}: [[{item['link']}]]")
        print(f"\nTotal broken wikilinks: {len(broken_wikilinks)}")
    else:
        print("No broken wikilinks found!")
    print()

    # Section 2: Broken Internal Markdown Links
    print("2. BROKEN INTERNAL MARKDOWN LINKS")
    print("-" * 80)
    if broken_markdown_links:
        # Group by source file
        by_file = defaultdict(list)
        for item in broken_markdown_links:
            by_file[item['source']].append(item)

        for source in sorted(by_file.keys()):
            print(f"\n{source}:")
            for item in by_file[source]:
                print(f"  Line {item['line']}: [{item['text']}]({item['url']})")
        print(f"\nTotal broken internal markdown links: {len(broken_markdown_links)}")
    else:
        print("No broken internal markdown links found!")
    print()

    # Section 3: External Links
    print("3. EXTERNAL LINKS")
    print("-" * 80)
    if all_external_links:
        # Group by domain
        by_domain = defaultdict(list)
        for url, source, line in sorted(all_external_links):
            domain = url.split('/')[2] if len(url.split('/')) > 2 else 'unknown'
            by_domain[domain].append((url, source, line))

        for domain in sorted(by_domain.keys()):
            print(f"\n{domain}:")
            for url, source, line in sorted(set(by_domain[domain]))[:10]:  # Limit to 10 per domain
                print(f"  {url}")
                print(f"    (in {source}, line {line})")
            if len(set(by_domain[domain])) > 10:
                print(f"  ... and {len(set(by_domain[domain])) - 10} more")
        print(f"\nTotal external links: {len(all_external_links)}")
    else:
        print("No external links found!")
    print()

    # Section 4: Summary Statistics
    print("4. SUMMARY STATISTICS")
    print("-" * 80)
    print(f"Total markdown files analyzed: {stats['total_files']}")
    print(f"Total wikilinks found: {stats['total_wikilinks']}")
    print(f"Broken wikilinks: {stats['broken_wikilinks']}")
    if stats['total_wikilinks'] > 0:
        print(f"Wikilink success rate: {(1 - stats['broken_wikilinks']/stats['total_wikilinks'])*100:.1f}%")
    print()
    print(f"Total internal markdown links found: {stats['total_internal_md_links']}")
    print(f"Broken internal markdown links: {stats['broken_md_links']}")
    if stats['total_internal_md_links'] > 0:
        print(f"Internal link success rate: {(1 - stats['broken_md_links']/stats['total_internal_md_links'])*100:.1f}%")
    print()
    print(f"Total external links found: {stats['total_external_links']}")
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
