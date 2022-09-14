import requests
from bs4 import BeautifulSoup
import sys


class NoWordError(Exception):
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return f'Sorry, unable to find {self.word}'


class SupportError(Exception):
    def __init__(self, lang):
        self.lang = lang

    def __str__(self):
        return f"Sorry, the program doesn't support {self.lang}"


def main():

    language_dict = {
        '1': 'arabic',
        '2': 'german',
        '3': 'english',
        '4': 'spanish',
        '5': 'french',
        '6': 'hebrew',
        '7': 'japanese',
        '8': 'dutch',
        '9': 'polish',
        '10': 'portuguese',
        '11': 'romanian',
        '12': 'russian',
        '13': 'turkish',
    }

    args = sys.argv
    language_from = args[1]
    language_to = args[2]
    word = args[3]

    open(f'{word}.txt', 'w').close()
    try:
        if language_to == 'all':
            for lang in language_dict.values():
                if lang != language_from:
                    translation, examples = connect(language_from, lang, word)
                    show(word, lang, translation, examples)
        else:
            if language_to not in language_dict.values():
                raise SupportError(language_to)
            translation, examples = connect(language_from, language_to, word)
            show(word, language_to, translation, examples)
    except SupportError as err:
        print(err)
    except NoWordError as err:
        print(err)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')


def connect(l_from, l_to, word):

    link = f'https://context.reverso.net/translation/{l_from}-{l_to}/{word}'
    user_agent = 'Mozilla/5.0'
    r = requests.get(link, headers={'User-Agent': user_agent})
    # print(r.status_code, 'OK')
    # print()
    if r.status_code != 200:
        raise NoWordError(word)

    soup = BeautifulSoup(r.content, 'html.parser')

    find_trans = soup.find_all('span', {'class': "display-term"}, limit=1)
    find_text = soup.find('section', id="examples-content").find_all('span', {'class': "text"}, limit=2)
    translation = [i.text for i in find_trans]
    examples = [i.text.strip() for i in find_text]
    return translation, examples


def show(word, lang, translation, examples):

    with open(f"{word}.txt", 'a') as f:
        print(f'{lang.capitalize()} Translations:')
        print(f'{lang.capitalize()} Translations:', file=f)
        for word in translation:
            print(word)
            print(word, file=f)
        print()
        print(file=f)
        print(f'{lang.capitalize()} Example:')
        print(f'{lang.capitalize()} Example:', file=f)
        # examples = examples[::-1]
        # for i in range(len(examples) // 2):
        for pair in range(2):
            print(examples[-1])
            print(examples.pop(), file=f)
        print()
        print(file=f)


if __name__ == "__main__":
    main()
