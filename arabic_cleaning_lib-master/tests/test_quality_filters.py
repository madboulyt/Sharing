import numpy as np

from arabic_cleaning.cleaning_utils import doc_to_lines
from arabic_cleaning.quality_filters import (
    passed_arabic_words_filter,
    passed_bullets_filter,
    passed_ellipsis_filter,
    passed_stopwords_filter,
    passed_symbol_ratio_filter,
    passed_word_length_filter,
    passed_word_range_filter,
)


def test_passed_word_range_filter():
    assert passed_word_range_filter(
        doc_to_lines("w1  w2 \nw3n\nw4\t\tw5\tw6 w7 w8 w9 w10"),
        3,
        10,
    ) == (True, 10)
    assert passed_word_range_filter(
        doc_to_lines("w1  w2 \nw3n\nw4\t\tw5\tw6 w7 w8 w9 w10 w11, w12"),
        3,
        10,
    ) == (False, 12)
    assert passed_word_range_filter(doc_to_lines(""), 3, 10) == (False, 0)
    assert passed_word_range_filter(doc_to_lines(" "), 3, 10) == (False, 0)
    assert passed_word_range_filter([]) == (False, 0)


def test_passed_word_length_filter():
    assert passed_word_length_filter(doc_to_lines("ww3 1 w2 wwww5"), 2, 4) == (
        True,
        2.75,
    )
    assert passed_word_length_filter(doc_to_lines("1 1 1"), 2, 4) == (False, 1)
    assert passed_word_length_filter(
        doc_to_lines("wwww5 wwww5 wwww5 wwww5 wwww5"), 2, 4
    ) == (
        False,
        5,
    )
    assert passed_word_length_filter(doc_to_lines(""), 2, 4) == (False, -1)
    assert passed_word_length_filter(doc_to_lines("  "), 2, 4) == (False, -1)
    assert passed_word_length_filter([]) == (False, -1)


def test_passed_symbol_ratio_filter():
    assert passed_symbol_ratio_filter(
        doc_to_lines("!@#$%^dfd dfd### sds @#213"), 0.1
    ) == (
        False,
        2.5,
    )
    assert passed_symbol_ratio_filter(doc_to_lines("wwwwwwwww@ d d d d"), 0.2) == (
        True,
        0.2,
    )
    assert passed_symbol_ratio_filter(doc_to_lines(""), 0.2) == (False, -1)
    assert passed_symbol_ratio_filter(doc_to_lines("  "), 0.2) == (False, -1)
    assert passed_symbol_ratio_filter([]) == (False, -1)


def test_passed_bullets_filter():
    doc1 = """
        - w w w
        - w w w
    """
    assert passed_bullets_filter(doc_to_lines(doc1), 0.9) == (False, 1)
    doc2 = """
    w w w w w w
    w w w w w w
    w w w w w w
        - w w w
        - w w w
    """
    assert passed_bullets_filter(doc_to_lines(doc2), 0.9) == (True, 0.4)
    assert passed_bullets_filter(doc_to_lines(""), 0.9) == (False, -1)
    assert passed_bullets_filter(doc_to_lines("  "), 0.9) == (False, -1)
    assert passed_bullets_filter([]) == (False, -1)


def test_passed_ellipsis_filter():
    doc1 = """
        - w w w…
        - w w w…
    """
    assert passed_ellipsis_filter(doc_to_lines(doc1), 0.3) == (False, 1.0)
    doc2 = """
    w w w w w w
    w w w w w w
    w w w w w w
    w w w w w w
    w w w w w w
        - w w w…
        - w w w…
    """
    passed_passed_ellipsis_filter, ratio_of_ellipsis = passed_ellipsis_filter(
        doc_to_lines(doc2), 0.3
    )
    assert passed_passed_ellipsis_filter
    expected_ratio_of_ellipsis = 0.2857142857142857
    assert np.isclose(ratio_of_ellipsis, expected_ratio_of_ellipsis)
    assert passed_ellipsis_filter(doc_to_lines(""), 0.3) == (False, -1)
    assert passed_ellipsis_filter(doc_to_lines("  "), 0.3) == (False, -1)
    assert passed_ellipsis_filter([]) == (False, -1)


def test_passed_stopwords_filter():
    doc1 = """
    ذهب محمد إلى لقاء الرئيس في مكتبه.
    """
    assert passed_stopwords_filter(doc_to_lines(doc1), 2) == (True, 2)
    assert passed_stopwords_filter(doc_to_lines(doc1), 4) == (False, 2)
    assert passed_stopwords_filter(doc_to_lines(""), 4) == (False, 0)
    assert passed_stopwords_filter([]) == (False, 0)


def test_passed_arabic_words_filter():
    doc1 = "ذهب محمد الي  ss ss ss ss ss ss ss سيdd"
    passed_ar_words_filter, num_ar_words = passed_arabic_words_filter(
        doc_to_lines(doc1), 0.6
    )
    assert not passed_ar_words_filter
    expected_num_ar_words = 0.272727
    assert np.isclose(num_ar_words, expected_num_ar_words)

    doc1 = "ذهب محمد الي  ss ss ss ss ss ss ss سيdd"
    passed_ar_words_filter, num_ar_words = passed_arabic_words_filter(
        doc_to_lines(doc1), 0.1
    )

    assert passed_ar_words_filter
    assert np.isclose(num_ar_words, expected_num_ar_words)
    assert passed_arabic_words_filter(doc_to_lines("مد ل"), 0.1) == (True, 1.0)

    assert passed_arabic_words_filter(doc_to_lines(""), 0.1) == (False, -1)
    assert passed_arabic_words_filter(doc_to_lines("  "), 0.1) == (False, -1)
    assert passed_arabic_words_filter([]) == (False, -1)
