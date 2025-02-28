import os
import time

import pandas as pd
from tqdm import tqdm
from loguru import logger
from playwright.sync_api import sync_playwright
from markdownify import markdownify as md


path_pages = "./data/pages"

records = pd.read_csv("./data/parsing_href.csv").to_dict(orient="records")
dirs = os.listdir(path_pages)

dirs = [(int(i.split("_")[0]), i) for i in dirs]
dirs = sorted(dirs, key=lambda x: x[0])


def pars_block(block):
    text = ""
    for i in block:
        inner_text = i.inner_text().strip()
        if inner_text:
            text += "\n\n"
            text += inner_text
    return text.strip()


def pars_table(block):
    text = ""
    for i in block:
        text += "\n\n"
        text += md(i.inner_html())
    return text.strip()


result = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    for html_file in tqdm(dirs):
        record = {}
        with open(f"{path_pages}/{html_file[1]}", "r", encoding="utf-8") as file:
            html_content = file.read()

        page = browser.new_page()

        for _ in range(10):
            try:
                page.set_content(html_content, wait_until="load")
                break
            except Exception as e:
                logger.info(f"Ошибка: {e}")
                continue

        title_block = page.query_selector_all("h1.post-hdr")
        record["title"] = pars_block(title_block)

        short_block = page.query_selector_all("div.post-short-block")
        record["short"] = pars_block(short_block)

        post_block = page.query_selector_all("div.post-lead")
        record["post"] = pars_block(post_block)

        review_block = page.query_selector_all(
            "div.frame.frame-post-text.frame-layout-0"
        )
        record["review"] = pars_block(review_block)

        method_block = page.query_selector_all("div.cont-type.frame-post-method")
        record["method"] = pars_block(method_block)

        comment_block = page.query_selector_all("div.comment-group")
        record["comment"] = pars_block(comment_block)

        tables_block = page.query_selector_all(
            "div.frame.frame-post-tbl.frame-type-text"
        )
        record["tables"] = pars_table(tables_block)

        result.append(record)
        page.close()

pd.DataFrame(result).to_csv("./data/parsed_data.csv", index=False)
