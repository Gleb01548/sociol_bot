import time

import pandas as pd
from tqdm import tqdm
from loguru import logger
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md


records = pd.read_csv("./data/parsing_href.csv").to_dict(orient="records")

base_url = "https://wciom.ru"


with sync_playwright() as p:
    browser = p.chromium.launch()
    for index, record in enumerate(tqdm(records)):
        url = f"{base_url}/{record["href"]}"

        page = browser.new_page()

        for i in range(10):
            try:
                page.goto(url, wait_until="load", timeout=50_000)
                break
            except Exception as e:
                logger.info(f"Ошибка: {e}")
                time.sleep(20)
                continue
        else:
            page.goto(url, wait_until="load", timeout=50_000)

        html_content = page.content()

        with open(
            f'data/pages/{index}_{record["title"][:60]}.html', "w", encoding="utf-8"
        ) as file:
            file.write(html_content)

        page.close()
        time.sleep(3)
