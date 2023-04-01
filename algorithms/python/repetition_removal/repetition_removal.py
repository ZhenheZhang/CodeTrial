import os
import sys
import argparse
import nltk
import hashlib
import json
import jieba
import codecs
import re
import unicodedata
from typing import List


def hash_text(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def is_repetition_detect(text: str,
                         duplicate_line_fraction=0.3,
                         duplicate_line_character_faction=0.2
                         ):
    """
    Check if there is repeated content within the input text.
    This function implements "Repetition Removal" as described in Gopher
    https://arxiv.org/abs/2112.11446

    Args:
        text (str): input text.
        duplicate_line_fraction (float, optional): Duplicate row deduplication threshold. Defaults to 0.3.
        duplicate_line_character_faction (float, optional): Threshold for the proportion of repeated line characters.
                                                            Defaults to 0.2.

    Returns:
        bool: If there is repeated content in the input text.
    """

    line_count = 0
    dup_line = 0
    dup_line_chars = 0
    visit_lines = {}

    text_length = len(add_delim_space(text).split())
    for line in text.split("\n"):
        line_length = len(add_delim_space(line).split())
        line_hash = hash_text(line)
        if line_hash in visit_lines:
            dup_line += 1
            dup_line_chars += line_length
        visit_lines[line_hash] = True
        line_count += 1

    if float(dup_line) / line_count > duplicate_line_fraction:
        return True

    if float(dup_line_chars) / text_length > duplicate_line_character_faction:
        return True

    top_ngram_character_fractions = [
        (2, 0.2),
        (3, 0.18),
        (4, 0.16),
    ]
    for ngram, threshold in top_ngram_character_fractions:
        word_list = list(jieba.cut(text))
        bgs = nltk.ngrams(word_list, ngram)
        f_dist = nltk.FreqDist(bgs)
        for word_list, repeat in f_dist.items():
            char_count = sum([len(word) for word in word_list])
            if char_count * (repeat - 1) / text_length > threshold:
                return True

    duplicate_ngram_character_fractions = [
        (5, 0.15),
        (6, 0.14),
        (7, 0.13),
        (8, 0.12),
        (9, 0.11),
        (10, 0.10),
    ]
    for ngram, threshold in duplicate_ngram_character_fractions:
        fdist = {}
        word_list = list(jieba.cut(text))
        mark = [0] * len(word_list)
        for i in range(len(word_list) - ngram + 1):
            bag = tuple(word_list[i: i + ngram])
            if bag in fdist:
                for j in range(i, i + ngram):
                    mark[j] = len(word_list[j])
                fdist[bag] += 1
            else:
                fdist[bag] = 1

        if sum(mark) / float(text_length) > threshold:
            return True
    return False


"""
@Notes  :   String Utilities
"""
def remove_symbols(input: str) -> str:
    """
    :param input: string
    :return: string
    """
    return "".join(
        " " if unicodedata.category(c)[0] in "MSP" else c for c in unicodedata.normalize("NFKC", input)
    )

def text_split(input: List[str], max_length: int, max_segments: int) -> List[List[str]]:
    split_list = []
    for text in input:
        try:
            text = add_delim_space(text).split()
            split_list.append([' '.join(text[i: i + max_length]) for i in range(0, len(text), max_length)])
            if len(split_list) > max_segments:
                split_list = []
        except:
            raise RuntimeError('Split text failed at {}'.format(text))
    return split_list

# Chinese token splitor
def add_delim_space(text: str) -> str:
    """
    :param text: string
    :return: string
    """
    PAT_ZH_SPACE = re.compile(r'(?<=[\u4e00-\u9fff])(?=[\u4e00-\u9fff])|(?<=[\u4e00-\u9fff])(?=[\da-zA-Z])|(?<=[\da-zA-Z])(?=[\u4e00-\u9fff])')
    PAT_SPACE = re.compile(r'\s+')
    text = PAT_ZH_SPACE.sub(' ', text)
    text = PAT_SPACE.sub(' ', text)
    return text


def main():
    parser = argparse.ArgumentParser("Repetition removal")
    parser.add_argument("--input", default="samples.jsonl", help="")
    parser.add_argument("--output_healthy_docs", default="healthy_docs.jsonl", help="output file for healthy lines")
    parser.add_argument("--output_bad_docs", default="bad_docs.jsonl", help="output file for bad lines")
    args = parser.parse_args()


'''Example of usage

    bad_lines_file = codecs.open(args.output_bad_docs, "w", "utf-8")
    healthy_lines_file = codecs.open(args.output_healthy_docs, "w", "utf-8")

    with open(args.input, 'r', encoding='utf8') as fin:
        for line in fin.readlines():
            try:
                j_seg = json.loads(line)
                if j_seg.get("text"):
                    text = j_seg["text"]
                else:
                    continue
            except RuntimeError:
                continue

            if is_repetition_detect(text=text):
                print(json.dumps(text, ensure_ascii=False), file=bad_lines_file)
            else:
                print(json.dumps(text, ensure_ascii=False), file=healthy_lines_file)
    return
'''


if __name__ == "__main__":
    main()
