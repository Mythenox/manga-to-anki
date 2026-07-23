# TODO: add support for slang terms? (words like ムズい aren't properly parsed)
# TODO: use parts of speech to add appropriate tags for anki (na-adjective, i-adjective, etc)

#TODO: Fix deinflect and use it
#      Store words in deinflected form (probably use @cached_property?) 

from typing import Union, Optional, List, Literal, Tuple
from sudachipy import tokenizer, dictionary, Morpheme, SplitMode, MorphemeList
from process_page import get_bubble_text
from constants import KATAKANA_TO_HIRAGANA, KATAKANA, FILLER

"""
Strings that can be parsed as SplitMode
"""
SplitModeStr = Literal["A", "a", "B", "b", "C", "c"]
POS = Tuple[str, str, str, str, str, str]

def main():
    """images = [f"sample/yfnu7-7({i}).png" for i in range(13)]
    text_list: list[str] = get_bubble_text(images)
    tokens = []
    for dialogue in text_list:
        dialogue_tokens = tokenize_text(dialogue)
        tokens.extend(dialogue_tokens)
    print(tokens)
    print(len(tokens))"""

    mode = tokenizer.Tokenizer.SplitMode.C
    a = tokenize("本当に腕折れる", mode)
    for item in a:
        print(item.surface)
    """k = tokenize_text(k.get_base_form())[0]
    print(k.get_reading())"""
    

class Word:
    def __init__(
            self,
            morpheme: Morpheme,
            excerpt: str # text from which this token came
    ) -> None:
        self.surface: str = morpheme.surface()
        self.part_of_speech: POS = morpheme.part_of_speech()
        self.normalized_form: str = morpheme.normalized_form()
        self.dictionary_form: str = morpheme.dictionary_form()
        self.reading_form: str = morpheme.reading_form()
        self.excerpt: str = excerpt

        #m.surface()
        #m.l1, m.l2, m.l3, m.l4, = m.part_of_speech()[:5]
        #m.dictionary_form()
        #m.reading_form()
        #m.excerpt
    
    def is_vocab(self) -> bool:
        """Returns true for nouns
        (exluding names of places (except countries) and people),
        adjectives and verbs."""
        if self.part_of_speech[0] == "名詞":
            # return false if name of location (except for countries)
            if self.part_of_speech[2] == "地域":
                return self.part_of_speech[3] == "国"
            # otherwise, return false if name of a person, true for every other noun
            return self.part_of_speech[2] != "人名"
        else:
            return (
                self.part_of_speech[0] == "動詞" or
                self.part_of_speech[0] == "副詞"
            )

    @property
    def eng_POS(self) -> str:
        if self.part_of_speech[0] == "名詞":
            return "noun"
        elif self.part_of_speech[0] == "動詞":
            return "verb"
        elif self.part_of_speech[0] == "副詞":
            return "adverb"
        elif self.part_of_speech[0] == "形状詞":
            return "na-adjective"
        return "i-adjective"
    
    def __repr__(self) -> str:
        return (
            "{surface=" + f"{self.surface}, "
            + f"l1_part={self.part_of_speech[0]}, "
            + f"base_form={self.dictionary_form}"
            + f'excerpt="{self.excerpt}'+ "}"
        )
    
    def __eq__(self, other) -> bool:
        return self.surface == other.surface and self.part_of_speech[0] == other.part_of_speech[0]
    
    def __hash__(self) -> int:
        return hash((self.surface, self.part_of_speech[0]))

def tokenize(
        text: str,
        mode: Union[SplitMode, SplitModeStr, None] = tokenizer.Tokenizer.SplitMode.C,
        out: Optional[MorphemeList] = None
) -> List[Word]:
    tokenizer_obj = dictionary.Dictionary().create()
    morphemes = tokenizer_obj.tokenize(text, mode)
    return [Word(morpheme, text) for morpheme in morphemes]

"""
def tokenize_text(excerpt: str, seen_words: set[str] = set()) -> set[PyToken]:
    tokenizer = JTokenizer()
    j_tokens = tokenizer.tokenize(excerpt)
    py_tokens: set[PyToken] = set()
    for j_token in j_tokens:
        token = PyToken(j_token, excerpt)
        if (
            token.base_form not in seen_words and
            token.surface not in FILLER
        ):
            py_tokens.add(token)
            seen_words.add(token.base_form)
    return deinflect_tokens(py_tokens)
"""
 
def deinflect_tokens(tokens: set[PyToken]) -> set[PyToken]:
    return {
        retokenize(token)
        if token.base_form != token.surface
        else token
        for token in tokens
    }

if __name__ == "__main__":
    main()