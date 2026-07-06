# Wrapper class because Java is scary
# TODO: add support for slang terms? (words like ムズい aren't properly parsed)
# TODO: use parts of speech to add appropriate tags for anki (na-adjective, i-adjective, etc)

from typing import Any
import jpype, jpype.imports
from process_page import get_bubble_text
from constants import KATAKANA_TO_HIRAGANA, KATAKANA, FILLER

kuromoji_jar = "./target/dependency/kuromoji-core-0.9.0.jar"
ipadic_jar = "./target/dependency/kuromoji-ipadic-0.9.0.jar"
jpype.startJVM(classpath=[kuromoji_jar, ipadic_jar])
JTokenizer = jpype.JClass('com.atilika.kuromoji.ipadic.Tokenizer')
JToken = jpype.JClass('com.atilika.kuromoji.ipadic.Token')


def main():
    """images = [f"sample/yfnu7-7({i}).png" for i in range(13)]
    text_list: list[str] = get_bubble_text(images)
    tokens = []
    for dialogue in text_list:
        dialogue_tokens = tokenize_text(dialogue)
        tokens.extend(dialogue_tokens)
    print(tokens)
    print(len(tokens))"""

    a = tokenize_text("感じ")
    for item in a:
        print(item.reading)
    """k = tokenize_text(k.get_base_form())[0]
    print(k.get_reading())"""
    

class PyToken:
    def __init__(
            self,
            j_token: object,
            excerpt: str # text from which this token came
    ) -> None:
        self.surface: str = str(j_token.getSurface()) # pyright: ignore[reportAttributeAccessIssue]
        self.l1_part: str = str(j_token.getPartOfSpeechLevel1()) # pyright: ignore[reportAttributeAccessIssue]
        self.l2_part: str = str(j_token.getPartOfSpeechLevel2()) # pyright: ignore[reportAttributeAccessIssue]
        self.l3_part: str = str(j_token.getPartOfSpeechLevel3()) # pyright: ignore[reportAttributeAccessIssue]
        self.l4_part: str = str(j_token.getPartOfSpeechLevel4()) # pyright: ignore[reportAttributeAccessIssue]
        self.base_form: str = str(j_token.getBaseForm()) # pyright: ignore[reportAttributeAccessIssue]
        self.reading: str = str(j_token.getReading()) # pyright: ignore[reportAttributeAccessIssue]
        self.pronunciation: str = str(j_token.getPronunciation()) # pyright: ignore[reportAttributeAccessIssue]
        self.excerpt: str = excerpt
    
    def is_vocab(self) -> bool:
        """Returns true for nouns
        (exluding names of places (except countries) and people),
        adjectives and verbs."""
        if self.l1_part == "名詞":
            # return false if name of location (except for countries)
            if self.l3_part == "地域":
                return self.l4_part == "国"
            # otherwise, return false if name of a person, true for every other noun
            return self.l3_part != "人名"
        else:
            return (
                self.l1_part == "動詞" or
                self.l1_part == "副詞"
            )
    
    @property
    def part_of_speech(self) -> str:
        if self.l1_part == "名詞":
            if self.l2_part == "形容動詞語幹":
                return "na-adjective"
            return "noun"
        elif self.l1_part == "動詞":
            return "verb"
        elif self.l1_part == "副詞":
            return "adverb"
        return "i-adjective"
    
    def __repr__(self) -> str:
        return (
            "{surface=" + f"{self.surface}, "
            + f"l1_part={self.l1_part}, "
            + f"base_form={self.base_form}"
            + f'excerpt="{self.excerpt}'+ "}"
        )
    
    def __eq__(self, other) -> bool:
        return self.surface == other.surface and self.l1_part == other.l1_part
    
    def __hash__(self) -> int:
        return hash((self.surface, self.l1_part))


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

def retokenize(original_token: PyToken) -> PyToken:
    #TODO: bugged behavior with ありえる, tokenizes into ある and える
    print(f"Retokenizing {original_token.surface}...")
    tokenizer = JTokenizer()
    j_tokens = list(tokenizer.tokenize(original_token.base_form))
    # if len(j_tokens) > 1:
    #     raise Exception("too many elements")
    j_token = j_tokens[0]
    return PyToken(j_token, original_token.excerpt)
    
def deinflect_tokens(tokens: set[PyToken]) -> set[PyToken]:
    return {
        retokenize(token)
        if token.base_form != token.surface
        else token
        for token in tokens
    }

if __name__ == "__main__":
    main()