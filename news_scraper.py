"""Module that scrapes stories from the BBC news website.
Returns URL and title when called in API.
"""
# pylint: disable=unused-variable, import-error

from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_html(url):
    """Gets raw HTML of page."""
    with urlopen(url) as page:
        html_bytes = page.read()
        html = html_bytes.decode("utf_8")
        return html


def parse_stories_bs(domain_url, html):
    """Parse stories URL and tile from HTML."""
    stories = []
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.css.select("a")
    for i in soup:
        href_match = (i["href"] and i["href"] not in urls and "news/" in i["href"]
                      and i["href"][-8::].isnumeric() and i["href"][:4] != "http")
        if href_match:
            if (f"{domain_url}{i['href']}", i.text) not in stories and i.text[:5] != "Video":
                stories.append((f"{domain_url}{i['href']}", i.text))
                urls.append(i["href"])
    return stories


if __name__ == "__main__":
    bbc_html_doc = get_html("http://bbc.co.uk/news")
    print(parse_stories_bs("http://bbc.co.uk/news", bbc_html_doc))
