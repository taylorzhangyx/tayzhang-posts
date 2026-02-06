#!/usr/bin/env python3
"""
Migration script to convert flat markdown posts to folder-based structure.

Each post becomes a folder containing:
- README.md (post content)
- img/ (downloaded images)
- audio/ (placeholder for future audio files)
"""

import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse


def get_image_extension(url: str, content_type: str = None) -> str:
    """Determine image extension from URL or content type."""
    # Try to get from URL path
    parsed = urlparse(url)
    path_ext = Path(parsed.path).suffix.lower()
    if path_ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
        return path_ext

    # Fallback to content type
    if content_type:
        type_map = {
            'image/png': '.png',
            'image/jpeg': '.jpg',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
        }
        return type_map.get(content_type, '.png')

    return '.png'


def download_image(url: str, dest_path: Path) -> bool:
    """Download image from URL to destination path."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.headers.get('Content-Type', '')
            ext = get_image_extension(url, content_type)

            # Update dest_path with correct extension if needed
            if dest_path.suffix != ext:
                dest_path = dest_path.with_suffix(ext)

            with open(dest_path, 'wb') as f:
                f.write(response.read())

            return True, dest_path
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"  Failed to download {url}: {e}")
        return False, dest_path


def convert_hashnode_syntax(content: str) -> str:
    """Convert Hashnode-specific markdown syntax to standard markdown."""

    # Remove align="..." attributes from images
    # Pattern: ![alt](url align="center") -> ![alt](url)
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+?)\s+align="[^"]*"\)',
        r'![\1](\2)',
        content
    )

    # Convert Hashnode details blocks to standard HTML details
    # <details data-node-type="hn-details-summary"><summary>...</summary>
    content = re.sub(
        r'<details[^>]*data-node-type="hn-details-summary"[^>]*>',
        '<details>',
        content
    )

    # Remove data-type="detailsContent" from divs
    content = re.sub(
        r'<div[^>]*data-type="detailsContent"[^>]*>',
        '<div>',
        content
    )

    # Keep <mark> tags as-is (valid HTML in markdown)

    return content


def fix_known_issues(content: str, filename: str) -> str:
    """Fix known markdown syntax issues in specific files."""

    if '2023-05-05-golang-gin-openapi-codegen-docs' in filename:
        # Fix incomplete link: [Github\](https://github.com/taylorzh
        content = re.sub(
            r'\[Github\\\]\(https://github\.com/taylorzh(?![a-zA-Z0-9])',
            '[Github](https://github.com/taylorzhangyx',
            content
        )

    return content


def extract_image_urls(content: str) -> list:
    """Extract all image URLs from markdown content."""
    # Match ![alt](url) patterns, capturing the URL
    # Also handle cases with align attributes
    pattern = r'!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)'
    urls = re.findall(pattern, content)

    # Filter to only http(s) URLs (not relative paths)
    return [url for url in urls if url.startswith('http')]


def migrate_post(md_file: Path, posts_dir: Path) -> dict:
    """Migrate a single markdown post to folder structure."""

    # Read original content
    content = md_file.read_text(encoding='utf-8')

    # Create folder name (remove .md extension)
    folder_name = md_file.stem
    post_folder = posts_dir / folder_name
    img_folder = post_folder / 'img'
    audio_folder = post_folder / 'audio'

    # Create directories
    post_folder.mkdir(exist_ok=True)
    img_folder.mkdir(exist_ok=True)
    audio_folder.mkdir(exist_ok=True)

    # Add .gitkeep to audio folder (empty placeholder)
    (audio_folder / '.gitkeep').touch()

    stats = {
        'name': folder_name,
        'images_found': 0,
        'images_downloaded': 0,
        'images_failed': 0,
    }

    # Extract and download images
    image_urls = extract_image_urls(content)
    stats['images_found'] = len(image_urls)

    url_to_local = {}
    for i, url in enumerate(image_urls, 1):
        img_name = f"img-{i:03d}"
        img_path = img_folder / img_name

        success, final_path = download_image(url, img_path)
        if success:
            # Store mapping for URL replacement
            relative_path = f"./img/{final_path.name}"
            url_to_local[url] = relative_path
            stats['images_downloaded'] += 1
            print(f"  Downloaded: {final_path.name}")
        else:
            # Keep original URL as fallback
            url_to_local[url] = url
            stats['images_failed'] += 1

    # Replace image URLs in content
    for original_url, new_path in url_to_local.items():
        # Escape special regex characters in URL
        escaped_url = re.escape(original_url)
        content = re.sub(escaped_url, new_path, content)

    # Convert Hashnode syntax
    content = convert_hashnode_syntax(content)

    # Fix known issues
    content = fix_known_issues(content, folder_name)

    # Write README.md
    readme_path = post_folder / 'README.md'
    readme_path.write_text(content, encoding='utf-8')

    return stats


def main():
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    posts_dir = repo_root / 'posts'

    if not posts_dir.exists():
        print(f"Error: posts directory not found at {posts_dir}")
        sys.exit(1)

    # Find all markdown files (not directories)
    md_files = sorted([f for f in posts_dir.glob('*.md') if f.is_file()])

    if not md_files:
        print("No markdown files found to migrate.")
        sys.exit(0)

    print(f"Found {len(md_files)} posts to migrate\n")

    total_stats = {
        'posts': 0,
        'images_found': 0,
        'images_downloaded': 0,
        'images_failed': 0,
    }

    for md_file in md_files:
        print(f"Migrating: {md_file.name}")
        stats = migrate_post(md_file, posts_dir)

        total_stats['posts'] += 1
        total_stats['images_found'] += stats['images_found']
        total_stats['images_downloaded'] += stats['images_downloaded']
        total_stats['images_failed'] += stats['images_failed']

        print(f"  -> {stats['name']}/ (images: {stats['images_downloaded']}/{stats['images_found']})\n")

    print("=" * 50)
    print("Migration Complete!")
    print(f"  Posts migrated: {total_stats['posts']}")
    print(f"  Images found: {total_stats['images_found']}")
    print(f"  Images downloaded: {total_stats['images_downloaded']}")
    print(f"  Images failed (kept external): {total_stats['images_failed']}")
    print("\nNext steps:")
    print("  1. Review the migrated folders")
    print("  2. Delete original .md files if satisfied")
    print("  3. Commit changes")


if __name__ == '__main__':
    main()
