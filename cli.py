import argparse
import textwrap

from config import DEFAULT_MAX_LENGTH, DEFAULT_MIN_LENGTH, MODEL_NAME
from summarizer import LongTextSummarizer


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize long text files.")
    parser.add_argument("input_file", help="Path to input text file")
    parser.add_argument("-o", "--output_file", help="Output file path")
    parser.add_argument("-m", "--model", default=MODEL_NAME,
                        help="Hugging Face model")
    parser.add_argument("--min_length", type=int, default=DEFAULT_MIN_LENGTH)
    parser.add_argument("--max_length", type=int, default=DEFAULT_MAX_LENGTH)
    return parser.parse_args()


def run_summarizer(args):
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    summarizer = LongTextSummarizer(args.model)
    summary = summarizer.summarize(text, args.min_length, args.max_length)

    wrapped = "\n".join(textwrap.wrap(summary, width=80))

    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(wrapped)
        print(f"Summary saved to {args.output_file}")
    else:
        print("\n--- SUMMARY ---\n" + wrapped)
