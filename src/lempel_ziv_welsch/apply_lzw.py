#!/usr/bin/env python3

import argparse
import json
from lzw import BaseLZW

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="data/CCrawl.de-en/train.tok.en",
)
args.add_argument(
    "-o", "--output",
    default="data/model_lzw/train.en"
)
args.add_argument(
    "-vi", "--vocab-input",
    default="data/model_lzw/model.vocab"
)
args.add_argument(
    "-n", "--number-of-lines",
    type=int, default=1000000
)
args.add_argument("--logfile", default=None)
args = args.parse_args()

print("Loading data")
with open(args.input, "r") as f:
    data = [x.rstrip("\n") for x in f.readlines()[:args.number_of_lines]]

print("Applying BPE")
model = BaseLZW()

model.load(args.vocab_input)
data = model.encode(data)

# save to file
with open(args.output, "w") as f:
    for line in data:
        f.write(line + "\n")

total_subwords = sum(line.count(" ") + 1 for line in data)
print("Outputting", total_subwords, "total subwords")
observed_subwords = set(w for line in data for w in line.split())
print("Observing", len(observed_subwords), "subwords")
total_unks = sum((" " + line).count(" UNK") for line in data)
print(
    f"Total of {total_unks} UNKs outputted",
    f"({total_unks/total_subwords:.4%} of all subwords)"
)

logline = {
    "model": args.vocab_input,
    "method": "lzw",
    # "vocab_size": len(model.merge_operations),
    "total_subwords": total_subwords,
    "total_unks": total_unks,
    "number_of_lines": args.number_of_lines,
    "output": args.output,
    "input": args.input,
}
print(logline)
if args.logfile is not None:
    with open(args.logfile, "a") as f:
        f.write(json.dumps(logline)+"\n")