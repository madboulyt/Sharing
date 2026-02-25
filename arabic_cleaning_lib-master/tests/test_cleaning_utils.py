import json
from functools import partial

from arabic_cleaning.cleaning_utils import (
    clean_and_filter_docs,
    clean_and_filter_json_docs,
)
from arabic_cleaning.quality_filters import (
    passed_arabic_words_filter,
    passed_bullets_filter,
    passed_ellipsis_filter,
    passed_stopwords_filter,
    passed_symbol_ratio_filter,
    passed_word_length_filter,
    passed_word_range_filter,
)

test_fileters = [
    partial(passed_word_range_filter, min_=1, max_=10),
    partial(passed_word_length_filter, min_=3, max_=10),
    partial(passed_symbol_ratio_filter, threshold_ratio=0.3),
    partial(passed_bullets_filter, threshold_ratio=0.9),
    partial(passed_ellipsis_filter, threshold_ratio=0.3),
    partial(passed_stopwords_filter, threshold=1),
    partial(passed_arabic_words_filter, threshold_ratio=0.5),
]


def test_clean_and_filter_docs(sample_docs, cleaned_docs):
    result = clean_and_filter_docs(sample_docs, filters=test_fileters)
    assert result == cleaned_docs


def test_clean_and_filter_json_docs(cleaned_docs, prepare_jsonl_files):
    in_path, text_fieled, out_path = prepare_jsonl_files
    clean_and_filter_json_docs(
        in_jsonl_path=in_path,
        text_field=text_fieled,
        out_jsonl_path=out_path,
        filters=test_fileters,
    )
    with open(out_path, "r") as f:
        for doc_id, line in enumerate(f):
            assert json.loads(line)[text_fieled] == cleaned_docs[doc_id]
