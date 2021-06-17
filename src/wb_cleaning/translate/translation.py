# import services.googletrans_client as gt
import json
from functools import lru_cache
from pathlib import Path
import requests
import googletrans
from googletrans import client as gt

from wb_cleaning import dir_manager
assert googletrans.__version__ == "3.1.0-alpha"

_trans = gt.Translator()


language_codes_path = Path(dir_manager.get_data_dir(
    "whitelists", "language", "language_codes.json"))

if not language_codes_path.exists():
    result = requests.get(
        "https://translate.shell.com/api/Translate/GetLanguages")
    result = result.json()

    language_codes = [{"name": o["item1"], "code": o["item2"]}
                      for o in result]

    with open(language_codes_path, "w") as open_file:
        json.dump(language_codes, open_file)

else:
    with open(language_codes_path) as open_file:
        language_codes = json.load(open_file)


@lru_cache(maxsize=1024)
def translate(text, src='auto', dest='en', with_extra_data=False):
    global _trans

    try:
        result = _trans.translate(text, dest=dest, src=src)
    except:
        # Try to re-aquire new instance.
        _trans = gt.Translator()
        result = _trans.translate(text, dest=dest, src=src)

    payload = dict(
        origin=result.origin,
        translated=result.text,
        src=result.src,
        dest=result.dest,
    )

    if with_extra_data:
        payload['extra_data'] = result.extra_data

    return payload


@lru_cache(maxsize=1024)
def translate_shell(text, src='auto', dest='en'):
    url = "https://translate.shell.com/api/translate/translate"
    data = dict(
        language=text,
        text=dest,
    )

    try:
        res = requests.post(url, json=data)
        result = res.json()
        translated = result.get("text")
        detected_src = result.get("languageDetect")

        clang = list(filter(lambda x: x["name"]
                     == detected_src, language_codes))
        print(text, translated, clang)
        if clang:
            detected_src = clang[0]["code"]
        else:
            detected_src = None

        if src != "auto" and src != detected_src:
            translated = None
    except:
        translated = None
        detected_src = None
        src = src

    payload = dict(
        origin=text,
        translated=translated,
        src=src,
        dest=dest,
        detected_src=detected_src,
    )

    return payload


def translate_list(texts, src='auto', dest='en'):
    text = "\n".join(texts)
    output = translate_shell(text, src=src, dest=dest)

    translated = output.get("translated") or []
    if translated:
        translated = [i.strip() for i in translated.split("\n")]

    return translated
