import os
import sys
import argparse
import nltk
import hashlib
import json
import jieba
import codecs


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
    for line in text.split("\n"):
        line_hash = hash_text(line)
        if line_hash in visit_lines:
            dup_line += 1
            dup_line_chars += len(line)
        visit_lines[line_hash] = True
        line_count += 1

    if float(dup_line) / line_count > duplicate_line_fraction:
        return True

    if float(dup_line_chars) / len(text) > duplicate_line_character_faction:
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
            if char_count * (repeat - 1) / len(text) > threshold:
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

        if sum(mark) / float(len(text)) > threshold:
            return True
    return False


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
