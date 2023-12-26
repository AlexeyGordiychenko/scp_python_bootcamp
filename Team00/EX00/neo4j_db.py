import argparse
import json
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import time
from datetime import timedelta


def parse_args() -> str:
    parser = argparse.ArgumentParser(
        description="Load data from .json to neo4j")
    parser.add_argument(
        "file",
        type=str,
        default="wiki.json",
        nargs="?",
        help="A file to load data from",
    )
    args = parser.parse_args()
    return args.file


def neo4j(file: str) -> None:
    driver = get_db_driver()
    if driver:
        graph = open_json(file)
        if graph:
            run_query(driver, graph)
        driver.close()


def get_db_driver() -> GraphDatabase.driver:
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_path)
    neo4j_pwd = os.environ.get("S21_NEO4J_PASS", None)

    if neo4j_pwd:
        try:
            return GraphDatabase.driver(
                "bolt://localhost:7687", auth=("neo4j", neo4j_pwd))
        except Exception as e:
            print(f'Couldn\'t connect to the neo4j database: {e}')
    else:
        print('Please, provide neo4j password in the .env file')


def open_json(file: str) -> dict:
    try:
        with open(file) as file:
            return json.load(file)
    except Exception as e:
        print(f"Couldn\'t read the json file: {e}")


def run_query(driver: GraphDatabase.driver, graph: dict) -> None:
    try:
        with driver.session() as session:
            time_start = time.time()
            session.run("""
                UNWIND $graph AS graph
                MERGE (a:Page {title: graph.page})
                WITH a, graph.links AS links
                UNWIND links AS link
                MERGE (b:Page {title: link})
                MERGE (a)-[r:LINKS_TO]->(b)
            """, graph=graph)
            print(
                f'Executed successfully in {timedelta(seconds=int(time.time() - time_start))}')
    except Exception as e:
        print(f"Couldn't add data to the neo4j: {e}")


if __name__ == "__main__":
    neo4j(parse_args())
