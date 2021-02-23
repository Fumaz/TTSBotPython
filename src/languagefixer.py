import json
import os

if __name__ == '__main__':
    languages = os.listdir('../languages/')
    english = json.load(open('../languages/en_US.json', 'r'))

    for language in languages:
        lang = json.load(open('../languages/' + language, 'r'))

        for k, v in english.items():
            if k not in lang:
                lang[k] = v

        json.dump(lang, open('../languages/' + language, 'w'))
