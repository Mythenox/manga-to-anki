from bs4 import BeautifulSoup, Tag
import requests

#TODO: Coroutines
#TODO: too much data needed, make classes

def get_html(url: str) -> str | None:
    resp = requests.get(url, headers={"User-Agent": "JishoQuery"})
    content_header: str | None = resp.headers.get('content-type')
    if resp.status_code >= 400:
        resp.raise_for_status()
    elif content_header is None or 'text/html' not in content_header:
        raise Exception("invalid content type")
    page_html = resp.text
    return page_html

def get_word_jlpt_rating(word: str) -> int | None:
    html: str | None = get_html(f"https://jisho.org/search/{word}%23words")
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("span", class_="concept_light-tag label")
    if result is None:
        return None
    jlpt_rating = int(result.text[-1])
    return jlpt_rating

def get_kanji_jlpt_rating(character: str) -> int | None:
    html: str | None = get_html(f"https://jisho.org/search/{character}%23kanji")
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    parent_div = soup.find("div", class_="jlpt")
    if isinstance(parent_div, Tag):
        result = parent_div.strong
        if isinstance(result, Tag):
            jlpt_rating = int(result.text[-1])
            return jlpt_rating
        return None
    return None

def get_word_english_meaning(word: str) -> str:
    pass

def get_kanji_english_meaning(character: str) -> str:
    pass

print(get_kanji_jlpt_rating("凡"))