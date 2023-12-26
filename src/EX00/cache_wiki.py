import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
import logging
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from typing import Set, Dict, List, Tuple
import itertools


def parse_args() -> Tuple[str, int]:
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


def parse_pages(starting_page: str, depth: int, result: List[Dict[str, List[str]]], limit: int, parsed: Set[str] = set()) -> None:
    page_links = parse_page(starting_page, depth)
    result.append({'page': starting_page, 'links': list(page_links)})
    if len(parsed) > limit or depth < 1:
        return
    page_links_not_parsed = page_links.difference(parsed)
    links_it = itertools.islice(page_links_not_parsed, min(
        limit-len(parsed), len(page_links_not_parsed)))
    parsed.update(page_links_not_parsed)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for link in links_it:
            executor.submit(parse_pages, link, depth -
                            1, result, limit, parsed)


def parse_page(page: str, depth: int) -> Set[str]:
    try:
        response = requests.get(f'https://en.wikipedia.org/wiki/{page}')
        response.raise_for_status()
        logging.info(f"page parsed: {page}, level: {depth}")
    except Exception as e:
        logging.error(f'could not parse page: {page}, level: {depth}')
        return set()

    soup = BS(response.text, 'lxml')
    links = soup.find(id="bodyContent").find_all("a", href=True)
    return set(link['href'].split('/')[-1].split('#')[0]
               for link in links
               if link['href'].startswith('/wiki/') and ':' not in link['href'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    starting_page, depth = parse_args()
    result: List[Dict[str, List[str]]] = []
    limit = 1000
    parse_pages(starting_page, depth, result=result, limit=limit)
    if len(result) >= limit:
        logging.info('Limit reached')
    json.dump(result, open(os.path.join(
        os.path.dirname(__file__), 'wiki.json'), 'w'), indent=4)
