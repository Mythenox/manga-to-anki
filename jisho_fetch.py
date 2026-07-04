from bs4 import BeautifulSoup, Tag
import requests

#TODO: Coroutines
   

def main():
    html = get_html("https://jisho.org/search/付%23kanji")
    meaning = get_kanji_english_meaning(html)
    print(meaning)


def get_html(url: str) -> str | None:
    resp = requests.get(url, headers={"User-Agent": "JishoQuery"})
    content_header: str | None = resp.headers.get('content-type')
    if resp.status_code >= 400:
        resp.raise_for_status()
    elif content_header is None or 'text/html' not in content_header:
        raise Exception("invalid content type")
    page_html = resp.text
    return page_html


def get_tango_jlpt_rating(html: str) -> int | None:
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("span", class_="concept_light-tag label")
    if isinstance(result, Tag):
        jlpt_rating = int(result.text[-1])
        return jlpt_rating
    return None


def get_kanji_jlpt_rating(html: str) -> int | None:
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


def get_tango_english_meaning(html: str | None) -> str | None:
    # some words have a million different definitions on jisho.org, so I'm gonna compromise and just grab the first one
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("span", class_="meaning-meaning")
    if isinstance(result, Tag):
        meaning = result.text.strip()
        return meaning
    return None
    
    
def get_kanji_english_meaning(html: str | None) -> str | None:
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find("div", class_="kanji-details__main-meanings")
    if isinstance(result, Tag):
        meaning = result.text.strip()
        return meaning
    return None


if __name__ == "__main__":
    main()