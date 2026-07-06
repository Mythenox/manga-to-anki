from functools import cached_property
from jisho_fetch import *
from pytoken import *
from constants import HIRAGANA, KATAKANA, KATAKANA_TO_HIRAGANA, KANJI
from infer import infer_reading

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
        self.reading = reading
        self.excerpt = excerpt
        self.part_of_speech = part_of_speech

    @cached_property
    def jisho_html(self) -> str | None:
        try:
            html = fetch_word_html(f"https://jisho.org/search/{self.word}")
        except Exception:
            return None
        return html 

    @cached_property
    def eng_meaning(self):
        if self.jisho_html is None:
            return None
        return get_tango_english_meaning(self.jisho_html)
    
    @cached_property
    def jlpt_rating(self):
        if self.jisho_html is None:
            return None
        return get_tango_jlpt_rating(self.jisho_html)
    
    def __repr__(self) -> str:
        return "{" + f"word={self.word}, reading={self.reading}, type={self.part_of_speech}, JLPT N{self.jlpt_rating}" + "}"
    
    
class Kanji:
    def __init__(
            self,
            character: str,
            context_surface: str,
            context_reading: str,
            excerpt: str,
            index: int
    ) -> None:
        self.character: str = character
        self.context_surface = context_surface
        self.context_reading = context_reading
        self.excerpt = excerpt
        self.index = index

    @cached_property
    def jisho_html(self) -> str | None:
        html = get_html(f"https://jisho.org/search/{self.character}%23kanji")
        return html 

    @cached_property
    def eng_meaning(self):
        if self.jisho_html is None:
            return None
        return get_kanji_english_meaning(self.jisho_html)
    
    @cached_property
    def jlpt_rating(self):
        if self.jisho_html is None:
            return None
        return get_kanji_jlpt_rating(self.jisho_html)
    
    @cached_property
    def reading(self) -> str | None:
        if self.jisho_html is None:
            return None
        possible_readings: dict[str, list[str]] | None = get_kanji_readings(self.jisho_html)
        if possible_readings is None:
            return None
        return infer_reading(
            self.context_reading,
            possible_readings,
            self.index,
            self.context_surface
        )
    
    def __repr__(self) -> str:
        return "{" + f"character={self.character}, reading={self.reading}, context={self.context_surface}, JLPT N{self.jlpt_rating}" + "}"
    

def create_vocab(
        token: PyToken,
        kanji_mode: bool = False,
) -> Tango | list[Kanji] | None:
    # run in kanji mode if "-k" passed from command line
    # can return a single Tango, list of Kanji, empty list, or None
    if kanji_mode:
        kanji_list: list[Kanji] = [
            Kanji(character, token.surface, token.reading, token.excerpt, token.surface.index(character))
            for character in token.surface
            if character in KANJI
        ]
        if len(kanji_list) == 0:
            return None
        return kanji_list
    if token.is_vocab():
        return Tango(
            token.surface,
            to_hiragana(token.reading),
            token.excerpt,
            token.part_of_speech
        )
    return None

def is_kango(word: str) -> bool:
    for character in word:
        if character not in KANJI:
            return False
    return True

def to_hiragana(reading: str) -> str:
    return "".join(KATAKANA_TO_HIRAGANA[ch] if ch in KATAKANA else ch for ch in reading)