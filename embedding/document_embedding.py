import argparse 
import os
import torch
import numpy as np

# library_parent_path = ".."
# abs_library_parent_path = os.path.abspath(library_parent_path)
# sys.path.insert(0, abs_library_parent_path)

from llm2vec import LLM2Vec


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Document embedding"
    )

    parser.add_argument(
        "--data",
        required=True,
        type=str,
        help="Dataset to embed"
    )
    parser.add_argument(
        "--base_model_path",
        required=True,
        type=str,
        help="base model name or path"
    )
    parser.add_argument(
        "--peft_model_path",
        # required=True,
        type=str,
        help="peft model name or path"
    )
    parser.add_argument(
        "-o",
        required=True,
        type=str,
        help="Output path (directory)"
    )

    args = parser.parse_args()

    return args
# def parse_args


def main(args):
    # get all files in directory
    file_list = os.listdir(args.data)

    document_mapping = {}
    
    for filename in file_list:
        file_path = os.path.join(args.data, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                document_mapping[os.path.basename(filename)] = content
            # with open() as f
        # if
    # for filename
    
    l2v = LLM2Vec.from_pretrained(
        args.base_model_path,
        peft_model_name_or_path=args.peft_model_path,
        device_map="cuda" if torch.cuda.is_available() else "cpu",
        torch_dtype=torch.bfloat16
    )

    document_keys = list(document_mapping.keys())
    documents = [document_mapping[k] for k in document_keys]

    embeddings = l2v.encode(documents)

    embeddings_cpu = [
        embed.cpu() for embed in embeddings
    ]

    keys_path = os.path.join(args.o, "keys.npy")
    embeddings_path = os.path.join(args.o, "embeddings.npy")

    np.save(keys_path, document_keys)
    np.save(embeddings_path, embeddings_cpu)
# def main


if __name__ == "__main__":
    args = parse_args()
    main(args)
# if
