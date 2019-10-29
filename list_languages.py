import json

import poiolib


def main():
    langinfo = poiolib.LangInfo()

    with open("config.json", "r", encoding="utf-8") as f:
        languages = json.load(f)["languages"]

    for l in languages:
        print("{}: {}".format(l, langinfo.langname_for_iso(l)))


if __name__ == "__main__":
    main()
