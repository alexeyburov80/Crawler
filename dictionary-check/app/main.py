import os
from urllib.parse import urlparse
from dotenv import load_dotenv

from crawler import crawl
from lemmatizer import normalize_text
from db import init_db, check_word
from logs import logger

load_dotenv()

def main():
    init_db()

    start_urls = os.getenv("START_URLS")
    depth = int(os.getenv("CRAWL_DEPTH", 1))

    if not start_urls:
        raise ValueError("START_URLS not defined in .env")

    urls = [u.strip() for u in start_urls.split(",")]
    print(f"\nurls: {urls}")
    for start_url in urls:
        logger.info(f"Processing site: {start_url}")

        domain = urlparse(start_url).netloc
        text = crawl(start_url, domain, depth=depth)
        lemmas = normalize_text(text)

        for word in lemmas:
           check_word(word)


if __name__ == "__main__":
    main()