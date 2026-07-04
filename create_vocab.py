from jisho_fetch import *
from pytoken import *
from kana import HIRAGANA, KATAKANA, KATAKANA_TO_HIRAGANA

# filter out vocab with jlpt_rating < jlpt_filter if "n{i}" passed from command line, where i in {1,2,3,4}

class Tango:
    def __init__(
            self,
            word: str,
            reading: str | None,
            excerpt: str,
            part_of_speech: str
    ) -> None:
        self.word = word
        self.jisho_html: str | None = self.init_jisho_html()
        self.eng_meaning: str | None = self.init_eng_meaning()
        self.jlpt_rating: int | None = self.init_jlpt_rating()
        self.reading = reading
        self.excerpt = excerpt
        self.part_of_speech = part_of_speech

    def init_jisho_html(self) -> str | None:
        html = get_html(f"https://jisho.org/word/{self.word}")
        return html 

    def init_eng_meaning(self):
        if self.jisho_html is None:
            return None
        return get_tango_english_meaning(self.jisho_html)
    
    def init_jlpt_rating(self):
        if self.jisho_html is None:
            return None
        return get_tango_jlpt_rating(self.jisho_html)
    
    def get_word(self):
        return self.word
    
    def get_eng_meaning(self):
        return self.eng_meaning
    
    def get_jlpt_rating(self):
        return self.jlpt_rating
    
    def get_reading(self):
        return self.reading
    
    
class Kanji:
    def __init__(
            self,
            character: str,
            excerpt: str,
            part_of_speech: str
    ) -> None:
        self.character: str = character
        self.jisho_html: str | None = self.get_jisho_html()
        self.eng_meaning: str | None = self.get_eng_meaning()
        self.reading: str | None = self.get_reading()
        self.jlpt_rating: int | None = self.get_jlpt_rating()
        self.excerpt = excerpt
        self.part_of_speech = part_of_speech

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
        kanji_list: list[Kanji] = [
            Kanji(character, token.get_excerpt(), token.get_part_of_speech())
            for character in token.get_surface_form()
            if is_kanji(character)
        ]
        if len(kanji_list) == 0:
            return None
        return kanji_list
    if token.is_vocab():
        return Tango(
            token.get_surface_form(),
            to_hiragana(token.reading),
            token.get_excerpt(),
            token.get_part_of_speech()
        )
    return None
    
def is_kanji(character: str) -> bool:
    return not (character in HIRAGANA or character in KATAKANA)

def is_kango(word: str) -> bool:
    for character in word:
        if not is_kanji(character):
            return False
    return True

def to_hiragana(reading: str) -> str:
    return "".join(KATAKANA_TO_HIRAGANA[ch] if ch in KATAKANA else ch for ch in reading)