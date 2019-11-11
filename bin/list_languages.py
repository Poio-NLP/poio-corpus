import json
import os

import poiolib

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    langinfo = poiolib.LangInfo()

    with open(
        os.path.join(SCRIPT_DIR, "..", "config.json"), "r", encoding="utf-8"
    ) as f:
        languages = json.load(f)["languages"]

    for l in languages.keys():
        print("{}: {}".format(l, langinfo.langname_for_iso(l)))


if __name__ == "__main__":
    main()
