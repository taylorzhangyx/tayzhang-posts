# tayzhang-posts

Blog posts and content for tayzhang personal website.

## Structure

Each post is a self-contained folder:

```
posts/
├── 2023-04-18-mlops-series-1-origin-what-why/
│   ├── README.md      # Post content (markdown)
│   ├── img/           # Images referenced in the post
│   │   ├── img-001.png
│   │   └── img-002.png
│   └── audio/         # Audio files (voice recordings, etc.)
└── 2023-05-05-golang-gin-openapi-codegen-docs/
    ├── README.md
    ├── img/
    └── audio/
```

## Post Format

Each `README.md` uses YAML frontmatter:

```markdown
---
title: "Post Title"
slug: "url-friendly-slug"
description: "Brief description for previews"
author: "Taylor Zhang"
date: YYYY-MM-DD
tags: ["tag1", "tag2"]
published: true
---

# Content starts here...
```

## Adding a New Post

1. Create a folder: `posts/YYYY-MM-DD-post-slug/`
2. Add `README.md` with frontmatter and content
3. Create `img/` folder for images (use relative paths: `./img/image.png`)
4. Create `audio/` folder for audio files
5. Use standard markdown syntax (avoid platform-specific extensions)

## Asset Guidelines

**Images:**
- Store in the post's `img/` folder
- Reference with relative paths: `![alt text](./img/filename.png)`
- Name sequentially: `img-001.png`, `img-002.png`, etc.

**Audio:**
- Store in the post's `audio/` folder
- Reference with relative paths: `./audio/filename.mp3`

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/migrate_posts.py` | Convert flat markdown files to folder structure |
