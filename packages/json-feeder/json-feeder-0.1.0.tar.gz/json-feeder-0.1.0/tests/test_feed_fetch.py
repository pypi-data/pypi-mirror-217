from unittest import TestCase

from feeder.feeder import fetch_existing_feeditems


class FeedFetchingTestCase(TestCase):
    def test_fetch_feed(self):
        items = list(fetch_existing_feeditems("https://www.jsonfeed.org/feed.json"))

        self.assertEqual(len(items), 2)
        self.assertEqual("JSON Feed version 1.1", items[0].title)
        self.assertEqual(items[0].id, "http://jsonfeed.micro.blog/2020/08/07/json-feed-version.html")
        self.assertEqual(items[0].url, "https://www.jsonfeed.org/2020/08/07/json-feed-version.html")
        self.assertIsNotNone(items[0].content_html)
        self.assertIsNone(items[0].content_text)
