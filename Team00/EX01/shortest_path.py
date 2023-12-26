import argparse
from collections import deque
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote
from typing import Any, Dict, List, Optional, Set


def parse_args():
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_path)
    wiki_file = os.environ.get(
        "WIKI_FILE", os.path.join(os.path.dirname(__file__), '../EX00/wiki.json'))

    parser = argparse.ArgumentParser(
        description="Find the shortest path from [start] to [end] for data from .json")
    parser.add_argument(
        "-f",
        "--from",
        type=str,
        dest="start",
        help="Page to start from",
        required=True
    )
    parser.add_argument(
        "-t",
        "--to",
        type=str,
        dest="end",
        help="Destination page",
        required=True
    )
    parser.add_argument(
        "-v",
        '--verbose',
        help="Print path between pages",
        action='store_true'
    )
    parser.add_argument(
        "-n",
        "--non-directed",
        dest="bidirected",
        help="Treat all links as 'non-directed' or 'bidirected'",
        action='store_true'
    )
    parser.add_argument(
        "file",
        type=str,
        default=wiki_file,
        nargs="?",
        help="A file to load data from",
    )
    return parser.parse_args()


def shortest_path(graph: Dict[str, Set[str]], start: str, end: str) -> Optional[List[str]]:
    # Breadth-First Search
    # queue to keep track of nodes and paths
    queue = deque([(start, [start])])
    # set of visited nodes
    visited = set(start)

    while queue:
        node, path = queue.popleft()
        if node == end:
            return path

        if node in graph:
            # get the non-visited links
            not_visited = set(graph[node]) - visited
            # add them to the queue with updated path
            queue.extend((next_node, path + [next_node])
                         for next_node in not_visited)
            # mark them as visited
            visited.update(not_visited)

    return None


def open_json(file: Optional[str]) -> Any:
    msg = "Database not found"
    if file is None:
        print(msg)
        return
    try:
        with open(file) as file:
            return json.load(file)
    except Exception as e:
        print(msg)


def get_graph(data: List[Dict[str, Any]], bidirected: bool) -> Dict[str, Set[str]]:
    graph = {item['page']: set(item['links']) for item in data}
    if bidirected:
        for node, links in list(graph.items()):
            for link in links:
                if link in graph:
                    graph[link].add(node)
                else:
                    graph[link] = {node}

    return graph


if __name__ == "__main__":
    args = parse_args()
    json = open_json(args.file)
    if not json:
        exit(1)
    graph = get_graph(json, args.bidirected)
    path = shortest_path(graph, quote(args.start), quote(args.end))
    if path:
        if args.verbose:
            print(' -> '.join(path))
        else:
            print(len(path) - 1)
    else:
        print('Path not found')
