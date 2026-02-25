from typing import List, Tuple

import arabicstopwords.arabicstopwords as stp
import numpy as np
import pyarabic.araby as araby

from .constents import BULLETS_CHARS, SYMBOLS


def passed_word_range_filter(
    lined_doc: List[List[str]],
    min_: int = 128,
    max_: int = 100000,
) -> Tuple[bool, float]:
    """
    Fails when a document does not have between `min_` and `max_` words (inclusive)
    """

    word_count = sum([len(l) for l in lined_doc])

    if word_count >= min_ and word_count <= max_:
        return True, word_count
    else:
        return False, word_count


def passed_word_length_filter(
    lined_doc: List[List[str]],
    min_: int = 3,
    max_: int = 10,
) -> Tuple[bool, float]:
    """
    Fails a document has average word length between `min_` and `max_` (inclusive)
    """

    word_lengths = []

    for line in lined_doc:
        word_lengths += [len(t) for t in line]

    if len(word_lengths) == 0:
        return False, -1

    avg = float(np.mean(word_lengths))

    if avg >= min_ and avg <= max_:
        return True, avg

    else:
        return False, avg


def passed_symbol_ratio_filter(
    lined_doc: List[List[str]],
    threshold_ratio: float = 0.3,
) -> Tuple[bool, float]:
    """
    Fails when a document has symbol-to-word ratio greater than `threshold_ratio`
    - references:
        - https://onlymyenglish.com/symbol-name-list-english/
        - https://en.wikipedia.org/wiki/List_of_typographical_symbols_and_punctuation_marks
    """

    doc_word_count = 0.0
    doc_symbol_count = 0.0

    for l in lined_doc:
        doc_word_count += len(l)
        for w in l:
            for c in w:
                if c in SYMBOLS:
                    doc_symbol_count += 1

    if doc_word_count == 0:
        return False, -1.0

    ratio = doc_symbol_count / doc_word_count
    if ratio > threshold_ratio:
        return False, ratio
    else:
        return True, ratio


def passed_bullets_filter(
    lined_doc: List[List[str]],
    threshold_ratio: float = 0.9,
) -> Tuple[bool, float]:
    """
    Fails when a document has more than `threshold_ratio` of lines starting with a bullet point.
    - references:
        - https://altcodeunicode.com/alt-codes-bullet-point-symbols/
    """

    num_bullet_lines = 0
    num_empty_lines = 0

    for line in lined_doc:
        line_str = " ".join(line)
        line_str = line_str.strip("\t").strip(" ")
        if len(line_str) == 0:
            num_empty_lines += 1
            continue
        if line_str.strip("\t").strip(" ")[0] in BULLETS_CHARS:
            num_bullet_lines += 1

    lines_count = len(lined_doc) - num_empty_lines
    if lines_count == 0:
        return False, -1

    ratio = num_bullet_lines / lines_count
    if ratio > threshold_ratio:
        return False, ratio
    else:
        return True, ratio


def passed_ellipsis_filter(
    lined_doc: List[List[str]],
    threshold_ratio: float = 0.3,
) -> Tuple[bool, float]:
    """
    Fails when a document has more than `threshold_ratio` of ellipsis.
    """
    num_ellipsis_lines = 0
    num_empty_lines = 0

    for line in lined_doc:
        line_str = " ".join(line)
        line_str = line_str.strip("\t").strip(" ")
        if len(line_str) == 0:
            num_empty_lines += 1
            continue
        if line_str.strip("\t").strip(" ")[-1] == "…":
            num_ellipsis_lines += 1

    lines_count = len(lined_doc) - num_empty_lines
    if lines_count == 0:
        return False, -1

    ratio = num_ellipsis_lines / lines_count
    if ratio > threshold_ratio:
        return False, ratio
    else:
        return True, ratio


def passed_stopwords_filter(
    lined_doc: List[List[str]],
    threshold: int = 2,
) -> Tuple[bool, float]:
    """
    Fails when a document doesn't have at least `threshold` of stop words (a text with
    very few stopwords indicates incoherent text).
    """

    stopwords_count = 0

    for line in lined_doc:
        for token in line:
            if stp.is_stop(token):
                stopwords_count += 1

    if stopwords_count >= threshold:
        return True, stopwords_count
    else:
        return False, stopwords_count


def passed_arabic_words_filter(
    lined_doc: List[List[str]],
    threshold_ratio: float = 0.5,
) -> Tuple[bool, float]:
    """
    - Fails when the document has a ratio of arabic words below the `threshold_ratio`.
    """
    arabic_words_count = 0
    doc_words_count = 0

    for line in lined_doc:
        for token in line:
            if len(token) < 2:
                continue
            doc_words_count += 1
            if araby.is_arabicword(token):
                arabic_words_count += 1

    if doc_words_count == 0:
        return False, -1

    ratio = arabic_words_count / doc_words_count

    if ratio >= threshold_ratio:
        return True, ratio
    else:
        return False, ratio
