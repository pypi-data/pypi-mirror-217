import importlib
import json
import os
from pathlib import Path

import thttp


class FeedItem:
    def __init__(self, id, url, title, content_text, content_html, date_published, authors=[]):
        self.id = id
        self.url = url
        self.title = title
        self.content_text = content_text
        self.content_html = content_html
        self.date_published = date_published
        self.authors = authors


def fetch_existing_feeditems(url):
    response = thttp.request(url)
    if response.status == 200 and response.json:
        for item in response.json.get("items"):
            yield FeedItem(
                item.get("id"),
                item.get("url"),
                item.get("title"),
                item.get("content_text"),
                item.get("content_html"),
                item.get("date_published"),
                item.get("authors"),
            )
    else:
        return []


def feed_item_as_json(item):
    j = {
        "id": item.id,
        "url": item.url,
    }

    optional_fields = ["title", "content_text", "content_html", "date_published", "authors"]
    for field in optional_fields:
        if getattr(item, field):
            j[field] = getattr(item, field)

    return j


def load_settings(module_name):
    default_settings = {
        "FEED_FUNCTION": None,
        "FEED_FILENAME": "out/feed.json",
        "FEED_URL": None,
        "FEED_TITLE": "Generated JSON Feed",
        "FEED_HOMEPAGE_URL": None,
        "FEED_ICON": None,
        "FEED_VERSION": "1.1",
        "FEED_MAX_ITEMS": 100,
    }

    settings = default_settings

    if module_name:
        settings_module = importlib.import_module(module_name)

        for k, v in default_settings.items():
            settings[k] = getattr(settings_module, k, v)

    return settings


def load_feed_function(fn_str):
    module_name, fn = fn_str.rsplit(".", 1)
    fn_module = importlib.import_module(module_name)
    fn = getattr(fn_module, fn)
    return fn


def json_feed(
    title,
    icon,
    home_page_url,
    feed_url,
    items,
    existing_items,
    *,
    max_items=100,
    version="1.1",
):
    feed_items = []
    existing_item_ids = [item.id for item in existing_items]

    for item in items:
        if item.id not in existing_item_ids:
            feed_items.append(item)

    feed_items.extend(existing_items)
    feed_items = feed_items[:max_items]

    feed = {
        "version": f"https://jsonfeed.org/version/{version}",
        "title": title,
        "icon": icon,
        "home_page_url": home_page_url,
        "feed_url": feed_url,
        "items": [feed_item_as_json(item) for item in feed_items],
    }

    # remove empty values
    feed = {k: v for k, v in feed.items() if v is not None}
    return feed


def generate(*, settings=None):
    feed_path = Path(settings["FEED_FILENAME"])
    feed_directory = Path(os.path.dirname(feed_path))
    feed_directory.mkdir(parents=True, exist_ok=True)

    if settings["FEED_URL"]:
        existing_items = list(fetch_existing_feeditems(settings["FEED_URL"]))
    else:
        existing_items = []

    if settings["FEED_FUNCTION"]:
        fn = load_feed_function(settings["FEED_FUNCTION"])
        items = fn()
    else:
        items = []

    feed = json_feed(
        settings["FEED_TITLE"],
        settings["FEED_ICON"],
        settings["FEED_HOMEPAGE_URL"],
        settings["FEED_URL"],
        items,
        existing_items,
        version=settings["FEED_VERSION"],
        max_items=settings["FEED_MAX_ITEMS"],
    )

    with open(feed_path, "w") as f:
        f.write(json.dumps(feed, indent=2))
