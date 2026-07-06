"""Process image to text, adding words as cards to an anki deck based on a filter
(default will be N3+ or N4+?). Also add kanji only mode, where it will only add kanji.
Add option to ask for user confirmation, where declined words will be remembered
and ignored in the future. If supplied with a parent deck, words present in the parent
deck will be ignored to avoid redundancy."""

#TODO: use coroutines?

import cv2
from pytoken import tokenize_text
from create_vocab import create_vocab
from process_page import get_bubble_text

def main():
    # text = "そもそもどうしてそんな結論になったの？"
    # text = "自分で持続ですか？って聞いてたから大丈夫だと思うけど"
    images = [f"sample/yfnu7-7({i}).png" for i in range(13)]
    text_list: list[str] = get_bubble_text(images)
    tokens = set()
    for dialogue in text_list:
        dialogue_tokens = tokenize_text(dialogue, {token.base_form for token in tokens})
        tokens.update(dialogue_tokens)
    # tokens = tokenize_text(text)
    for token in tokens:
        vocab = create_vocab(token, kanji_mode=True)
        if vocab:
            print(vocab)
    

if __name__ == "__main__":
    main()