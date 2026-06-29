"""Process image to text, adding words as cards to an anki deck based on a filter
(default will be N3+ or N4+?). Also add kanji only mode, where it will only add kanji.
Add option to ask for user confirmation, where declined words will be remembered
and ignored in the future. If supplied with a parent deck, words present in the parent
deck will be ignored to avoid redundancy."""