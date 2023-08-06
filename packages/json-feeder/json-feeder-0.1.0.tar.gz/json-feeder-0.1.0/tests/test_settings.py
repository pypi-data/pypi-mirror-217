import os
import tempfile
from unittest import TestCase

from feeder.feeder import load_settings


class LoadSettingsTestCase(TestCase):
    def test_default_settings(self):
        settings = load_settings(None)
        self.assertEqual(settings["FEED_FILENAME"], "out/feed.json")

    def test_settings_loads_from_module(self):
        with tempfile.TemporaryDirectory(dir=os.getcwd(), prefix="loads_from_module") as dir:
            with open(dir + "/__init__.py", "w") as f:
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())

            with open(dir + "/settings.py", "w") as f:
                f.write("FEED_FILENAME = 'dist/feed.json'")
                f.flush()
                os.fsync(f.fileno())

            module_name = dir.split("/")[-1] + ".settings"
            settings = load_settings(module_name)

            self.assertEqual(settings["FEED_FILENAME"], "dist/feed.json")
