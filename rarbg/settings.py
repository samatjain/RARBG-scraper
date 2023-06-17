import re
from typing import Optional
from pathlib import Path


BOT_NAME = "rarbg"

SPIDER_MODULES = ["rarbg.spiders"]
NEWSPIDER_MODULE = "rarbg.spiders"

LOG_LEVEL = "INFO"
LOG_SHORT_NAMES = True
FEED_EXPORT_INDENT = 4

FEEDS = {
    "%(search_term)s.auto.csv": {
        "format": "csv",
        "fields": ["title", "url", "upload_date", "magnet"],
    },
}

DOWNLOAD_DELAY = 8
# DOWNLOAD_DELAY= 30


def UserAgentFromWgetRc() -> Optional[str]:
    try:
        data = Path("~/.config/wget/wgetrc").expanduser().read_text()

        results = re.search("user_agent = (.*)", data)
        if not results:
            return None
        user_agent = results.group(1)
    except Exception:
        return None
    return user_agent


USER_AGENT = (
    UserAgentFromWgetRc()
    or "Mozilla/5.0 (X11; Ubuntu; Linux ppc64le; rv:90.0) Gecko/20100101 Firefox/90.0"
)

# HTTPCACHE_ENABLED = True

ROBOTSTXT_OBEY = False


DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": None,
    "rarbg.middlewares.ThreatDefenceRedirectMiddleware": 600,
}

CONCURRENT_REQUESTS = 1

# DOWNLOAD_DELAY = 4

COOKIES_ENABLED = True
