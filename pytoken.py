# Wrapper classes because Java is scary

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
        self.base_form: str = str(j_token.getBaseForm()) # pyright: ignore[reportAttributeAccessIssue]
    
    def get_surface_form(self):
        return self.surface

    def get_l1_part(self):
        return self.l1_part

    def get_base_form(self):
        return self.base_form

    def is_kango(self) -> bool:
        return True
    
    def __repr__(self) -> str:
        pass


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