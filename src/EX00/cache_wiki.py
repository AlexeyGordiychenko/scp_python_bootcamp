import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import logging
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from typing import Set, Dict
import itertools


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cache Wikipedia links from pages")
    parser.add_argument(
        "-p",
        "--page",
        type=str,
        default="Peer-to-peer",
        help="Page name to start gathering links from",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=3,
        help="Maximum depth to go deep down from a link",
    )
    args = parser.parse_args()
    return quote(args.page), args.depth


def parse_pages(starting_page, depth, result, parsed: Set = set(), limit=100):
    page_links = parse_page(starting_page)
    logging.info(f"page parsed: {starting_page}, level: {depth}")
    result[starting_page] = list(page_links)
    if len(parsed) > limit or depth < 1:
        return
    page_links_not_parsed = page_links.difference(parsed)
    links_it = itertools.islice(page_links_not_parsed, min(
        limit-len(parsed), len(page_links_not_parsed)))
    parsed.update(page_links_not_parsed)
    # for link in links_it:
    #     parse_pages(link, depth - 1, result, parsed, limit)
    with ThreadPoolExecutor(max_workers=30) as executor:
        future_to_page = {executor.submit(
            parse_pages, link, depth - 1, result, parsed): link for link in links_it}


def parse_page(page):
    response = requests.get(f'https://en.wikipedia.org/wiki/{page}')
    soup = BS(response.text, 'lxml')
    links = soup.find(id="bodyContent").find_all("a", href=True)
    return set(link['href'].split('/')[-1].split('#')[0]
               for link in links
               if link['href'].startswith('/wiki/') and ':' not in link['href'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    starting_page, depth = parse_args()
    result = dict()
    parse_pages(starting_page, depth, result=result)
    # print(result)
    json.dump(result, open('links.json', 'w'))
