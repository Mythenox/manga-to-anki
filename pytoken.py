# Wrapper class because Java is scary
# TODO: add support for slang terms? (words like ムズい aren't properly parsed)
# TODO: use parts of speech to add appropriate tags for anki (na-adjective, i-adjective, etc)

from typing import Any
import jpype, jpype.imports
from process_page import get_bubble_text

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

    a = tokenize_text("映画")
    k = a[0]
    print(k.get_base_form())
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
    
    def get_surface_form(self):
        return self.surface

    def get_l1_part(self):
        return self.l1_part
    
    def get_l2_part(self):
        return self.l2_part
    
    def get_l3_part(self):
        return self.l3_part
    
    def get_l4_part(self):
        return self.l4_part

    def get_base_form(self):
        return self.base_form
    
    def get_reading(self):
        return self.reading
    
    def get_pronunciation(self):
        return self.pronunciation
    
    def is_vocab(self) -> bool:
        """Returns true for nouns
        (exluding names of places (except countries) and people),
        adjectives and verbs."""
        if self.get_l1_part() == "名詞":
            # return false if name of location (except for countries)
            if self.get_l3_part() == "地域":
                return self.get_l4_part() == "国"
            # otherwise, return false if name of a person, true for every other noun
            return self.get_l3_part() != "人名"
        else:
            return (
                self.get_l1_part() == "動詞" or
                self.get_l1_part() == "副詞"
            )
    
    def __repr__(self) -> str:
        return (
            "{surface=" + f"{self.surface}, "
            + f"l1_part={self.l1_part}, "
            + f"base_form={self.base_form}"
            + f'excerpt="{self.excerpt}'+ "}"
        )


def tokenize_text(excerpt: str) -> list[PyToken]:
    tokenizer = JTokenizer()
    j_tokens = tokenizer.tokenize(excerpt)
    py_tokens: list[PyToken] = []
    for j_token in j_tokens:
        token = PyToken(j_token, excerpt)
        py_tokens.append(token)
    return py_tokens
    
def fix_tokens(tokens: list[PyToken]):
    for token in tokens:
        if token.get_base_form != token.get_reading():
            pass

if __name__ == "__main__":
    main()