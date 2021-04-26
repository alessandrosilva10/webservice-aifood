"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`.
"""
import json
import random
import string

default_locale = "en-gb"
cached_strings = {}


def refresh():
    print("Refreshing...")
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


def generate_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(30))


refresh()
