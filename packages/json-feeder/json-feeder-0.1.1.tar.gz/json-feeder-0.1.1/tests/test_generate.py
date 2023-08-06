import json
import os
import tempfile
from unittest import TestCase, mock

import thttp

from feeder.feeder import generate

JSONFEED_ORG_JSONFEED = {
    "version": "https://jsonfeed.org/version/1",
    "title": "JSON Feed",
    "icon": "https://micro.blog/jsonfeed/avatar.jpg",
    "home_page_url": "https://www.jsonfeed.org/",
    "feed_url": "https://www.jsonfeed.org/feed.json",
    "items": [
        {
            "id": "http://jsonfeed.micro.blog/2020/08/07/json-feed-version.html",
            "title": "JSON Feed version 1.1",
            "content_html": '<p>We&rsquo;ve updated the spec to <a href="https://jsonfeed.org/version/1.1">version 1.1</a>. It’s a minor update to JSON Feed, clarifying a few things in the spec and adding a couple new fields such as <code>authors</code> and <code>language</code>.</p>\n\n<p>For version 1.1, we&rsquo;re starting to move to the more specific MIME type <code>application/feed+json</code>. Clients that parse HTML to discover feeds should prefer that MIME type, while still falling back to accepting <code>application/json</code> too.</p>\n\n<p>The <a href="https://jsonfeed.org/code/">code page</a> has also been updated with several new code libraries and apps that support JSON Feed.</p>\n',  # noqa
            "date_published": "2020-08-07T11:44:36-05:00",
            "url": "https://www.jsonfeed.org/2020/08/07/json-feed-version.html",
        },
        {
            "id": "http://jsonfeed.micro.blog/2017/05/17/announcing-json-feed.html",
            "title": "Announcing JSON Feed",
            "content_html": '\n\n<p>We —\xa0Manton Reece and Brent Simmons —\xa0have noticed that JSON has become the developers’ choice for APIs, and that developers will often go out of their way to avoid XML. JSON is simpler to read and write, and it’s less prone to bugs.</p>\n\n<p>So we developed JSON Feed, a format similar to <a href="http://cyber.harvard.edu/rss/rss.html">RSS</a> and <a href="https://tools.ietf.org/html/rfc4287">Atom</a> but in JSON. It reflects the lessons learned from our years of work reading and publishing feeds.</p>\n\n<p><a href="https://jsonfeed.org/version/1">See the spec</a>. It’s at version 1, which may be the only version ever needed. If future versions are needed, version 1 feeds will still be valid feeds.</p>\n\n<h4 id="notes">Notes</h4>\n\n<p>We have a <a href="https://github.com/manton/jsonfeed-wp">WordPress plugin</a> and, coming soon, a JSON Feed Parser for Swift. As more code is written, by us and others, we’ll update the <a href="https://jsonfeed.org/code">code</a> page.</p>\n\n<p>See <a href="https://jsonfeed.org/mappingrssandatom">Mapping RSS and Atom to JSON Feed</a> for more on the similarities between the formats.</p>\n\n<p>This website —\xa0the Markdown files and supporting resources —\xa0<a href="https://github.com/brentsimmons/JSONFeed">is up on GitHub</a>, and you’re welcome to comment there.</p>\n\n<p>This website is also a blog, and you can subscribe to the <a href="https://jsonfeed.org/xml/rss.xml">RSS feed</a> or the <a href="https://jsonfeed.org/feed.json">JSON feed</a> (if your reader supports it).</p>\n\n<p>We worked with a number of people on this over the course of several months. We list them, and thank them, at the bottom of the <a href="https://jsonfeed.org/version/1">spec</a>. But — most importantly — <a href="http://furbo.org/">Craig Hockenberry</a> spent a little time making it look pretty. :)</p>\n',  # noqa
            "date_published": "2017-05-17T10:02:12-05:00",
            "url": "https://www.jsonfeed.org/2017/05/17/announcing-json-feed.html",
        },
    ],
}


class GenerateFeedTestCase(TestCase):
    def test_generate_jsonfeed_feed(self):
        with tempfile.TemporaryDirectory(dir=os.getcwd(), prefix="generate_jsonfeed_feed") as dir:
            settings = {
                "FEED_FILENAME": f"{dir}/feed_jsonfeed.org.json",
                "FEED_TITLE": "JSON Feed",
                "FEED_ICON": "https://micro.blog/jsonfeed/avatar.jpg",
                "FEED_HOMEPAGE_URL": "https://www.jsonfeed.org/",
                "FEED_URL": "https://www.jsonfeed.org/feed.json",
                "FEED_VERSION": "1",
                "FEED_FUNCTION": None,
                "FEED_MAX_ITEMS": 100,
            }

            mock_return_value = thttp.Response(None, None, JSONFEED_ORG_JSONFEED, 200, None, None, None)
            with mock.patch("feeder.feeder.thttp.request", return_value=mock_return_value):
                generate(settings=settings)

            original_feed = JSONFEED_ORG_JSONFEED

            with open(f"{dir}/feed_jsonfeed.org.json", "r") as f:
                generated_feed = json.loads(f.read())

            self.assertDictEqual(original_feed, generated_feed)

    def test_generate_feed_with_items(self):
        with tempfile.TemporaryDirectory(dir=os.getcwd(), prefix="feed_with_items") as dir:
            settings = {
                "FEED_FILENAME": f"{dir}/feed_with_items.json",
                "FEED_TITLE": "Test Feed",
                "FEED_ICON": None,
                "FEED_HOMEPAGE_URL": "https://www.example.org/",
                "FEED_URL": None,
                "FEED_VERSION": "1.1",
                "FEED_FUNCTION": dir.split("/")[-1] + ".core.fn",
                "FEED_MAX_ITEMS": 100,
            }

            with open(dir + "/core.py", "w") as f:
                f.write("from feeder.feeder import FeedItem\n\n")
                f.write("def fn():\n")
                f.write(
                    "    return [FeedItem('https://example.org', 'https://example.org', 'Example', None, '<p>example.org</p>', '2023‐07‐04T00:25:39+00:00')]"  # noqa
                )
                f.flush()
                os.fsync(f.fileno())

            generate(settings=settings)

            with open(f"{dir}/feed_with_items.json", "r") as f:
                generated_feed = json.loads(f.read())

            self.assertEqual(generated_feed["home_page_url"], "https://www.example.org/")
            self.assertTrue("feed_url" not in generated_feed)
            self.assertEqual(len(generated_feed["items"]), 1)
