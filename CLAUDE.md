# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Pelican-based static site generator for a personal blog at ryanmo.co. The site focuses on tech posts, automation tutorials, and personal lists/collections.

## Build Commands

### Development
- `make html` - Generate the site for development
- `make serve` - Serve the site locally at http://localhost:8000
- `make devserver` - Generate and serve with auto-reload
- `make regenerate` - Regenerate on file changes
- `make clean` - Remove generated files

### Production
- `make publish` - Generate site with production settings
- `make deploy` - Build and deploy via rsync
- `make rsync_upload` - Upload to production server
- `make github` - Deploy to GitHub Pages

### Docker
- `docker build -t ryanmoco .` - Build Docker image
- Site is built automatically during Docker image creation

## Architecture

### Content Structure
- **Posts**: Located in `content/posts/` with subdirectories for categories (Tech, Lists)
- **Pages**: Static pages in `content/pages/` (About, 404)
- **Images**: All images stored in `content/images/`
- **Downloads**: Files for download in `content/downloads/`

### Configuration
- **Development config**: `configs/pelicanconf.py`
- **Production config**: `configs/publishconf.py` 
- **Theme**: Currently using 'orange' theme from `theme/orange/`
- **Plugins**: Custom plugins in `plugins/` directory

### Key Plugins
- **drafts_page**: Adds drafts template when TESTING=True
- **json_feed**: Generates JSON Feed for RSS compatibility
- **code_replacement**: Handles code block processing
- **tag_cloud**: Generates tag cloud functionality
- **summary**: Manages article summaries

### URL Structure
- Articles: `YYYY/MM/DD/slug/`
- Categories: `category/slug/`
- Tags: `tag/slug/`
- Pages: `slug/`


### Custom Features
- List posts automatically use 'lists' template
- Multiple social media integrations
- Custom markdown processing with code highlighting
- JSON feed generation for categories and tags
- Automatic drafts page in development mode

## File Organization
- Content metadata automatically injects author as 'Ryan M'
- List posts in `posts/Lists/` get special template treatment
- Static files copied from `content/extra/` to root (robots.txt, etc.)
- Images and downloads preserved with original paths