import argparse
import json
import os
from dotenv import load_dotenv
import matplotlib as mpl
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import timedelta


def parse_args():
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_path)
    wiki_file = os.environ.get("WIKI_FILE", None)

    parser = argparse.ArgumentParser(
        description="Visualize data from .json")
    parser.add_argument(
        "file",
        type=str,
        default=wiki_file,
        nargs="?",
        help="A file to load data from",
    )
    args = parser.parse_args()
    return args.file


def open_json(file):
    msg = "Database not found"
    if file is None:
        print(msg)
        return
    try:
        with open(file) as file:
            return json.load(file)
    except Exception as e:
        print(msg)


def visualize(file):
    graph = open_json(file)
    if graph:
        time_start = time.time()
        G = nx.Graph()
        pages = [item['page'] for item in graph]
        G.add_edges_from(
            [
                (item['page'], link)
                for item in graph for link in item['links']
                if link in pages
            ]
        )

        degrees = [G.degree(n) for n in G.nodes()]

        # data for the color of nodes
        low, *_, high = sorted(degrees)
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)

        # a better layout but much more slower
        # pos = nx.kamada_kawai_layout(G)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(90, 90))
        nx.draw(G, pos,
                with_labels=False,
                node_size=[d * 20 for d in degrees],
                font_size=8,
                node_color=[mapper.to_rgba(d) for d in degrees],
                edge_color='gray')
        # set font size depending on the node degree
        for node, (x, y) in pos.items():
            degree = G.degree(node)
            plt.text(x, y, s=node,
                     fontsize=min(max(6, degree/20.0), 14),
                     ha='center',
                     va='center')

        plt.savefig(os.path.join(os.path.dirname(__file__), "graph.png"))
        print(
            f'Saved successfully in {timedelta(seconds=int(time.time() - time_start))}')


if __name__ == "__main__":
    visualize(parse_args())
