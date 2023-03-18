#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
@File   :   language_detect.py
@Author :   Zhenhe Zhang
@Date   :   2023/3/18
@Notes  :   language detection dev by fasttext. https://fasttext.cc/docs/en/language-identification.html
"""

# import fasttext
import re
import unicodedata
from typing import List


"""
@Notes  :   Language Identification by two models
"""
class LanguageIdentifier():
    def __init__(self, model_cjk, model_non_cjk):
        self.model_cjk = fasttext.load_model(model_cjk)
        self.model_non_cjk = fasttext.load_model(model_non_cjk)

    def is_cjk_character(self, char):
        ch = ord(char)
        if ch >= 0x4e00 and ch <= 0x9fff:  # [4e00-9fff]: CJK Unified Ideographs
            return True
        elif ch >= 0x2e80 and ch <= 0x2eff:  # [2e80-2eff]: Radical supply in CJK
            return True
        elif ch >= 0x2f00 and ch <= 0x2fdf:  # [2f00-2fdf]: Kangxi Radicals
            return True
        elif ch >= 0x2ff0 and ch <= 0x2fff:  # [2f00-2fff]: Ideograpic Description Characters
            return True
        elif ch >= 0x3000 and ch <= 0x303f:  # [3000-303f]: CJK symbols and punctuation
            return True
        elif ch in [0x201c, 0x201d, 0xff0c, 0xff01, 0xff1f, 0xff1b, 0xff1a, 0xff08, 0xff09, 0xff3b, 0xff3d]:
            # [“, ”, ，, ！, ？, ；, ：, （, ）, 【, 】] ref: https://en.wikipedia.org/wiki/Chinese_punctuation
            return True
        else:
            return False

    def split_cjk(self, txt):
        output = ""
        previous_ch = ""
        for ch in txt:
            if self.is_cjk_character(ch) or (len(previous_ch) > 0 and self.is_cjk_character(previous_ch)):
                output += ch + " "
            else:
                output += ch
            previous_ch = ch
        return output.strip()

    def split_non_cjk(self, txt):
        output = ""
        for ch in txt:
            if ch == " ":
                output += "% "
            else:
                output += ch + " "
        output = "% " + output + "%"
        return output

    # When more than half non-whitespace chars are cjk, the whole is considered cjk.
    def is_input_cjk(self, txt, threshold=0.5):
        num_cjk = 0
        total_ch = 0
        for chunk in txt.split(" "):
            prev_is_non_cjk = False
            for ch in chunk:
                if self.is_cjk_character(ch):
                    num_cjk += 1
                    total_ch += 1
                    if prev_is_non_cjk:
                        total_ch += 1
                        prev_is_non_cjk = False
                else:
                    prev_is_non_cjk = True
            if prev_is_non_cjk:
                total_ch += 1

        if total_ch == 0:
            return False
        return num_cjk / total_ch >= threshold

    def predict(self, txt):
        result = ()
        if self.is_input_cjk(txt):
            result = self.model_cjk.predict(self.split_cjk(txt), k=1)
        else:
            result = self.model_non_cjk.predict(self.split_non_cjk(txt), k=1)
        return result


"""
@Notes  :   Constants
"""
SUCCESS = 0
FAILED = -1
LID_MAX_LENGTH = 512
LID_MIN_LENGTH = 16
LID_MAX_SEGMENTS = 100
CHINESE = 'zh'
ENGLISH = 'en'
OTHERS = 'others'

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


def language_detect(text: str, model_cjk: str, model_non_cjk: str, min_confidence=0.90, target_langid='en') -> str:
    '''
    :param text: input texture
    :param model_cjk: Languages with CJK (e.g. Chinese, Korean, Japanese and etc.)
    :param model_non_cjk: Languages without CJK (e.g. English and etc.)
    :param min_confidence: minimum confidence of acceptance
    :param target_langid: target language id
    :return: language id
    '''

    # New a Language Identifier
    lid = LanguageIdentifier(model_cjk=model_cjk, model_non_cjk=model_non_cjk)
    # Preprocess input
    sentence_list = input.split('\n')
    lid_input_list = text_split(input=sentence_list, max_length=LID_MAX_LENGTH, max_segments=LID_MAX_SEGMENTS)

    # Prepare running model
    language_tag_list = []
    for input_list in lid_input_list:
        for in_text in input_list:
            text_non_symbol = remove_symbols(in_text)
            # specialcase1: only symbols(e.g. punctuations), specialcase2: length less than LID_MIN_LENGTH
            if text_non_symbol != '' and len(text_non_symbol) >= LID_MIN_LENGTH:
                result = lid.predict(txt=in_text)
                language_id = result[0][0][9:]
                language_score = result[1][0]
                if language_id == 'zh' or language_id == 'en':
                    language_tag_list.append(language_id)
                else:
                    if language_score > min_confidence:
                        language_tag_list.append(language_id)
    return language_tag_list



if __name__ == "__main__":
    text = 'It’s an interesting bet from Sinema. After all, Democrats usually don’t run a candidate'
    model_cjk = 'lid_cjk.bin'
    model_non_cjk = 'lid_non_cjk.bin'
    print(language_detect(text=text, model_cjk=model_cjk, model_non_cjk=model_non_cjk))
