import time

import pandas as pd
from tqdm import tqdm
from playwright.sync_api import sync_playwright

result = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for index in tqdm(range(1, 442)):
        page = browser.new_page()

        page.goto(f"https://wciom.ru/analytical-reviews/page-{index}")

        first_news = page.query_selector("a.news-list-first.mb-20")
        title = first_news.get_attribute("title")
        href = first_news.get_attribute("href")
        result.append({"title": title, "href": href})

        news_element = page.query_selector_all("a.news-list")

        for i in news_element:
            title = i.get_attribute("title")
            href = i.get_attribute("href")
            result.append({"title": title, "href": href})

        page.close()

        time.sleep(10)

    browser.close()

pd.DataFrame(result).to_csv("./data/parsing_href.csv", index=False)
