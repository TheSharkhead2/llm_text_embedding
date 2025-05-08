"""
Preprocessing for https://www.kaggle.com/datasets/nulldata/medium-post-titles
"""

import os
import argparse
import pandas as pd
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Medium post title dataset preprocessing"
    )

    parser.add_argument(
        "--dataset_path",
        default="data/medium_post_titles.csv",
        type=str,
        help="Path to downloaded dataset."
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
    df = pd.read_csv(args.dataset_path)

    ai_filtered = df[df["category"] == "artificial-intelligence"]
    ai_titles = [
        row["title"] for _, row in ai_filtered.iterrows()
    ]

    all_titles = [
        row["title"] for _, row in df.iterrows()
    ]

    ai_titles_output = os.path.join(args.o, "ai_titles.txt")
    all_titles_output = os.path.join(args.o, "all_titles.txt")

    with open(ai_titles_output, 'w', encoding="utf-8") as f:
        for title in ai_titles:
            f.write(title + "\n")
        # for title
    # with open() as f

    with open(all_titles_output, 'w', encoding="utf-8") as f:
        for title in all_titles:
            f.write(title + "\n")
        # for title
    # with open() as f
# def main


if __name__ == "__main__":
    args = parse_args()
    main(args)
# if

