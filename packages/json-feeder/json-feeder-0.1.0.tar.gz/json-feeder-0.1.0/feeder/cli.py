import sys


def parse_args(args):
    result = {
        a.split("=")[0]: int(a.split("=")[1])
        if "=" in a and a.split("=")[1].isnumeric()
        else a.split("=")[1]
        if "=" in a
        else True
        for a in args
        if "--" in a
    }
    result["[]"] = [a for a in args if not a.startswith("--")]
    return result


SETTINGS_FILE = """# settings for feeder

FEED_FILENAME = "out/feed.json"
FEED_FUNCTION = "feed.get_items"
FEED_VERSION = "1.1"

FEED_TITLE = ""
FEED_URL = ""
FEED_HOMEPAGE_URL = ""
FEED_ICON = ""
"""

GENERATE_FILE = """from feeder.feeder import generate, load_settings
import os


if __name__ == "__main__":
    settings_module_name = os.environ.get("FEEDER_SETTINGS_MODULE", "settings")
    settings = load_settings(settings_module_name)
    generate(settings=settings)
"""

FEED_FILE = """from feeder.feeder import FeedItem

def get_items():
    return []
"""


def cli():
    args = parse_args(sys.argv[1:])

    if args["[]"][0] == "startfeed":
        with open("settings.py", "w") as f:
            f.write(SETTINGS_FILE)

        with open("generate.py", "w") as f:
            f.write(GENERATE_FILE)

        with open("feed.py", "w") as f:
            f.write(FEED_FILE)
