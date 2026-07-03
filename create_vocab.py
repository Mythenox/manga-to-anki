from jisho_fetch import *
from pytoken import *
from kana import HIRAGANA, KATAKANA

# filter out vocab with jlpt_rating < jlpt_filter if "n{i}" passed from command line, where i in {1,2,3,4}

class Tango:
    def __init__(self, word: str) -> None:
        self.word: str = word
        self.jisho_html: str | None = self.get_jisho_html()
        self.eng_meaning: str | None = self.get_eng_meaning()
        self.jlpt_rating: int | None = self.get_jlpt_rating()
        self.is_kango: bool = is_kango(word)
        self.furigana: str | None = self.get_furigana()

    def get_jisho_html(self) -> str | None:
        html = get_html(f"https://jisho.org/word/{self.word}")
        return html 

    def get_eng_meaning(self):
        if self.jisho_html is None:
            return None
    
    def get_jlpt_rating(self):
        raise NotImplementedError
    
    def get_furigana(self):
        if not self.is_kango:
            return None
    
    
class Kanji:
    def __init__(self, character: str) -> None:
        self.character: str = character
        self.jisho_html: str | None = self.get_jisho_html()
        self.eng_meaning: str | None = self.get_eng_meaning()
        self.reading: str | None = self.get_reading()
        self.jlpt_rating: int | None = self.get_jlpt_rating()

    def get_jisho_html(self) -> str | None:
        html = get_html(f"https://jisho.org/search/{self.character}%23kanji")
        return html

    def get_reading(self):
        pass
    
    def get_eng_meaning(self):
        raise NotImplementedError
    
    def get_jlpt_rating(self):
        raise NotImplementedError
    

def create_vocab(
        token: PyToken,
        kanji_mode: bool = False,
) -> Tango | list[Kanji] | None:
    # run in kanji mode if "-k" passed from command line
    # can return a single Tango, list of Kanji, empty list, or None
    if kanji_mode:
        kanji_list: list[Kanji] = []
        for character in token.get_surface_form():
            if is_kanji(character):
                kanji = Kanji(character)
                kanji_list.append(kanji)
        if len(kanji_list) == 0:
            return None
        return kanji_list
    if token.is_vocab():
        return Tango(token.base_form)
    return None
    
def is_kanji(character: str) -> bool:
    return not (character in HIRAGANA or character in KATAKANA)

def is_kango(word: str) -> bool:
    for character in word:
        if not is_kanji(character):
            return False
    return True

print(is_kango("明治"))