#!/usr/bin/env python3

import argparse
import json
import subprocess
import tempfile
import tqdm

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", nargs="+",
    default=[
        "data/CCrawl.de-en/train.tok.en",
        "data/CCrawl.de-en/train.tok.de"
    ]
)
args.add_argument(
    "-o", "--output", nargs="+",
    default=[
        "data/model_morfessor/train.en",
        "data/model_morfessor/train.de"
    ]
)
args.add_argument("-n", "--number-of-lines", type=int, default=100000)
# recursive, viterbi
args.add_argument("-m", "--model", default="data/model_morfessor/model.pkl")
# morfessor, flatcat    
args.add_argument("--morfessor", default="morfessor")
args = args.parse_args()

observed_vocabulary = set()
total_subwords = 0

for input_fname, output_fname in zip(args.input, args.output):
    with tempfile.NamedTemporaryFile() as fname1, tempfile.NamedTemporaryFile() as fname2:
        fname1 = fname1.name
        fname2 = fname2.name
        with open(fname1, "w") as f:
            data_in = open(input_fname, "r").readlines()[:args.number_of_lines]
            f.writelines(data_in)
    
        txt_train_command = f"\
            {args.morfessor}-segment {fname1} \
            --load {args.model} \
            --output {fname2} \
            "

        print("RUNNING", " ".join(txt_train_command.split()))
        subprocess.run(txt_train_command, shell=True)

        segmented_words = open(fname2, "r").readlines()
        with open(output_fname, "w") as fout:
            data_out = open(input_fname, "r").readlines()
            cur_line = []

            new_line = []
            for word in tqdm.tqdm(segmented_words):
                while not cur_line:
                    if new_line:
                        fout.write(" ".join(new_line) + "\n")
                        new_line = []
                    cur_line = data_in.pop(0).rstrip().split(" ")
                    cur_line = [x for x in cur_line if len(x) > 0]

                subwords = word.split()
                total_subwords += sum(len(subw) for subw in subwords)
                observed_vocabulary |= set(subwords)
                new_word = " @@".join(subwords)
                orig_word = "".join(subwords)
                assert cur_line.pop(0) == orig_word
                new_line.append(new_word)

        print("So far observed", len(observed_vocabulary), "subwords")

print("Emitted", total_subwords, "subwords")