import argparse
import os

from src.TransLocator_main import localize


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Localizing Bugs in Source Code using TransLocator")

    # Add arguments
    parser.add_argument('--br-path', type=str, required=True, help='The file path for input data')
    parser.add_argument('--kw-model-dir', type=str, required=True,
                        help='The directory where the keyword model is stored')
    parser.add_argument('--ce-model-dir', type=str, required=True,
                        help='The directory where the cross-encoder model is stored')
    parser.add_argument('--L', type=int, required=True,
                        help='Keyword length to consider')
    parser.add_argument('--topK_rerank', type=int, required=True, help='Specify how many results to rerank')
    parser.add_argument('--topN', type=int, required=True,
                        help='Specify how many top results to consider for the final output')

    args = parser.parse_args()

    # check if all the required arguments are provided indvidually
    if not args.br_path:
        print("The bug report file path is required")
        exit(1)
    elif not args.kw_model_dir:
        print("The keyword model directory is required")
        exit(1)
    elif not args.ce_model_dir:
        print("The cross-encoder model directory is required")
        exit(1)
    elif not args.topK_rerank:
        print("The value for topK_rerank is required")
        exit(1)
    elif not args.topN:
        print("The value for topN is required")
        exit(1)
    elif not args.L:
        print("The value for L is required")
        exit(1)

    br_path = args.br_path
    kw_model_dir = args.kw_model_dir
    ce_model_dir = args.ce_model_dir
    topK_rerank = args.topK_rerank
    topN = args.topN
    length = args.L


    # validate if the paths are correct
    if not os.path.exists(br_path):
        print("The bug report file path does not exist")
        exit(1)

    if not os.path.exists(kw_model_dir):
        print("The keyword model directory does not exist")
        exit(1)

    if not os.path.exists(ce_model_dir):
        print("The cross-encoder model directory does not exist")
        exit(1)

    if topK_rerank < 1:
        print("The value for topK_rerank must be greater than 0")
        exit(1)

    if topN < 1 or topN > topK_rerank:
        print("The value for topN must be greater than 0 and less than or equal to topK_rerank")
        exit(1)

    if length < 1:
        print("The value for L must be greater than 0")
        exit(1)

    localize(br_path, kw_model_dir, ce_model_dir, topK_rerank, topN, length)

if __name__ == "__main__":
    main()