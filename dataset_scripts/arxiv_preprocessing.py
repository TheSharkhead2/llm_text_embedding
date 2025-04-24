"""
Preprocessing for https://www.kaggle.com/datasets/Cornell-University/arxiv  
"""

import os
import argparse
import json
import pandas as pd
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        prog="arXiv kaggle dataset processing"
    )

    parser.add_argument(
        "--dataset_path",
        default="data/arxiv.json",
        type=str,
        help="Path to download dataset"
    )

    parser.add_argument(
        "--chunk_size",
        default=10_000,
        type=int,
        help="Chunks to read articles in by"
    )

    parser.add_argument(
        "--categories",
        nargs='*',
        help="arXiv categories which should be included. If not specified, no filtering will occur"
    )
    parser.add_argument(
        "-o",
        type=str,
        required=True,
        help="Output directory"
    )

    args = parser.parse_args()    

    return args
# def parse_args


def main(args):
    chunks = pd.read_json(
        args.dataset_path, lines=True, chunksize=args.chunk_size
    )

    all_doc_titles = []
    all_doc_abstracts = []
    all_metadata = []

    for chunk in chunks:
        if args.categories is not None:
            relevant_articles = chunk[
                chunk["categories"].apply(
                    lambda cat: not set(args.categories).isdisjoint(set(cat.split()))
                )
            ]
        else:
            relevant_articles = chunk
        # if

        # I love how they have new lines in these strings LIKASFGIPUSHUD
        document_titles = [
            row["title"].replace("\n", " ").replace("   ", " ").replace("  ", " ")
            for _, row in relevant_articles.iterrows()
        ]
        document_abstracts = [
            row["abstract"].replace("\n", " ").replace("   ", " ").replace("  ", " ")
            for _, row in relevant_articles.iterrows()
        ]

        all_doc_titles += document_titles
        all_doc_abstracts += document_abstracts

        metadata = [
            {
                "title": row["title"],
                "id": row["id"],
                "categories": row["categories"]
            }
            for _, row in relevant_articles.iterrows()
        ]

        all_metadata += metadata
    # for chunk

    # save
    titles_output = os.path.join(args.o, "arxiv_titles.txt")
    abstract_output = os.path.join(args.o, "arxiv_abstracts.txt")
    metadata_output = os.path.join(args.o, "metadata.npy")

    np.save(metadata_output, all_metadata)

    with open(titles_output, 'w', encoding="utf-8") as f:
        for title in all_doc_titles:
            f.write(title + "\n")
        # for title
    # with open() as f

    with open(abstract_output, 'w', encoding="utf-8") as f:
        for abstract in all_doc_abstracts:
            f.write(abstract + "\n")
        # for abstract
    # with open() as f
# def main


if __name__ == "__main__":
    args = parse_args()

    main(args)
# if

