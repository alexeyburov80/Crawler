from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
import re

visited = set()

def crawl(start_url, domain, depth=1):

    print("depth: {}\nstart_url: {}\ndomain: {}".format(depth, start_url, domain))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        text = _crawl_page(page, start_url, domain, depth)
        browser.close()

        return text


def _crawl_page(page, url, domain, depth):
    if depth == 0 or url in visited:
        return ""

    visited.add(url)

    try:
        page.goto(url, wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(1000)
    except Exception:
        return ""

    try:
        text = page.inner_text("body")
        text = re.sub(r'\d+', '', text)
    except Exception:
        text = ""

    links = []

    try:
        anchors = page.query_selector_all("a[href]")
        for a in anchors:
            href = a.get_attribute("href")
            if href:
                next_url = urljoin(url, href)
                if urlparse(next_url).netloc == domain:
                    links.append(next_url)
    except Exception:
        pass

    for link in links:
        text += " " + _crawl_page(page, link, domain, depth - 1)

    return text