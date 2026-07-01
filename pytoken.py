# Wrapper classes because Java is scary
# TODO: add support for slang terms? (words like ムズい aren't properly parsed)

from typing import Any
import jpype, jpype.imports

kuromoji_jar = "./target/dependency/kuromoji-core-0.9.0.jar"
ipadic_jar = "./target/dependency/kuromoji-ipadic-0.9.0.jar"
jpype.startJVM(classpath=[kuromoji_jar, ipadic_jar])
JTokenizer = jpype.JClass('com.atilika.kuromoji.ipadic.Tokenizer')
JToken = jpype.JClass('com.atilika.kuromoji.ipadic.Token')


def main():
    tokens = tokenize_text("飯を作った")
    token_1 = tokens[2]
    print(token_1.get_base_form())
    

class PyToken:
    def __init__(
            self,
            j_token: object
    ) -> None:
        self.surface: str = str(j_token.getSurface()) # pyright: ignore[reportAttributeAccessIssue]
        self.l1_part: str = str(j_token.getPartOfSpeechLevel1()) # pyright: ignore[reportAttributeAccessIssue]
        self.l2_part: str = str(j_token.getPartOfSpeechLevel2()) # pyright: ignore[reportAttributeAccessIssue]
        self.l3_part: str = str(j_token.getPartOfSpeechLevel3()) # pyright: ignore[reportAttributeAccessIssue]
        self.l4_part: str = str(j_token.getPartOfSpeechLevel4()) # pyright: ignore[reportAttributeAccessIssue]
        self.base_form: str = str(j_token.getBaseForm()) # pyright: ignore[reportAttributeAccessIssue]
        self.jlpt_class: int # web scraper to get this from jisho.org?
    
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

    def is_kango(self) -> bool:
        return True
    
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
            + f"base_form={self.base_form}" + "}"
        )


def tokenize_text(text: str) -> list[PyToken]:
    tokenizer = JTokenizer()
    j_tokens = tokenizer.tokenize(text)
    py_tokens: list[PyToken] = []
    for j_token in j_tokens:
        token = PyToken(j_token)
        py_tokens.append(token)
    return py_tokens
    

if __name__ == "__main__":
    main()