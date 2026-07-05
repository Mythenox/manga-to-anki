from kana import HIRAGANA, KATAKANA, KATAKANA_TO_HIRAGANA

def to_hiragana(reading: str) -> str:
    return "".join(KATAKANA_TO_HIRAGANA[ch] if ch in KATAKANA else ch for ch in reading)

# infer_reading() does not work for 熟字訓 (words like 今日 and 大人)

def infer_reading(
        token_reading: str,
        possible_readings: dict[str,list[str]],
        index: int,
        surface: str
) -> str:
    context: str = to_hiragana(token_reading)
    candidates = [
        reading for sublist in possible_readings.values()
        for reading in sublist
        if to_hiragana(reading) in context
    ]
    if len(candidates) == 1:
        return candidates[0]
    kango_length = len(surface)
    for reading in candidates:
        normalized_reading = to_hiragana(reading)
        if index == 0:
            if context.startswith(normalized_reading):
                remaining = context.removeprefix(normalized_reading)
                # if there isn't at least 1 character remaining per remaining kanji (kango_length - 1), it is invalid
                if len(remaining) >= kango_length - 1:
                    return reading
        elif index == len(surface) - 1:
            if context.endswith(normalized_reading):
                remaining = context.removesuffix(normalized_reading)
                # if there isn't at least 1 character remaining per remaining kanji (kango_length - 1), it is invalid
                if len(remaining) >= kango_length - 1:
                    return reading
        else:
            # in this case, the reading must be contained a substring not starting at the beginning or ending at the end of the original string.
            proper_substring: str = context[1:-1]
            if len(reading) > len(proper_substring):
                raise Exception("big oopsie has occurred") # hopefully this isn't even possible
            if normalized_reading in proper_substring:
                return reading
    return token_reading # this happens in the case of 熟字訓


def apply_rendaku():
    pass
    
def apply_handakuon():
    pass

def apply_sokuon():
    pass
    