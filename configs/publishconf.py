from __future__ import unicode_literals
import os
import sys
sys.path.append(os.curdir)

from configs.pelicanconf import *

DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False

SITEURL = "https://ryanmo.co"
RELATIVE_URLS = False

FEEDPRESS_RSS = "http://feedpress.me/ryanmoco"
FEED_ALL_RSS = "feed.xml"
CATEGORY_FEED_RSS = "feeds/category/{slug}.rss.xml"
TAG_FEED_RSS = "feeds/tag/{slug}.rss.xml"
RSS_FEED_SUMMARY_ONLY = False


EXTRA_PATH_METADATA = {
    "extra/pihole-facebook.txt": {"path": "pihole/pihole-facebook.txt"},
    "extra/pihole-whatsapp.txt": {"path": "pihole/pihole-whatsapp.txt"},
    "extra/pihole-extras.txt": {"path": "pihole/pihole-extras.txt"},
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/redirect-rules.map": {"path": "redirect-rules.map"},
    "extra/CNAME": {"path": "CNAME"},
}

# Social widget
SOCIAL = (
    ("Github", "http://www.github.com/rjames86"),
    ("RSS", FEEDPRESS_RSS),
)

PLUGINS.extend(
    [
        "taglist",
        "all_articles_json",
    ]
)
STATIC_PATHS.append("json")

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}"

# Theme

TESTING = False
# DISQUS_SITENAME = "rjames86"

# Plugins

# JSON Feed
SITE_FAVICON = SITEURL + "/images/favicon.png"
