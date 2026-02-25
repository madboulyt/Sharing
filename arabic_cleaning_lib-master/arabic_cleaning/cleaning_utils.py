import json
from functools import partial
from typing import Callable, List, Optional, Tuple, Union

from tqdm import tqdm  # type: ignore

from .constents import PUNCTUATION_SET
from .quality_filters import (
    passed_arabic_words_filter,
    passed_bullets_filter,
    passed_ellipsis_filter,
    passed_stopwords_filter,
    passed_symbol_ratio_filter,
    passed_word_length_filter,
    passed_word_range_filter,
)
from .text_cleansing import (
    correct_hamazat,
    fix_bad_encoding,
    hindi_numbers_to_arabic,
    insert_space_for_nonarabic,
    mask_email,
    mask_url,
    mask_user_mention,
    normalize_similar_chars,
    reduce_multiple_spaces,
    remove_bad_chars,
    remove_diacritics_tatweel,
    remove_html,
    remove_non_digit_repetition,
    remove_redundant_punct,
)

all_cleansers: List[Callable[[str], str]] = [
    fix_bad_encoding,
    remove_bad_chars,
    remove_diacritics_tatweel,
    normalize_similar_chars,
    remove_html,
    mask_url,
    mask_email,
    mask_user_mention,
    hindi_numbers_to_arabic,
    remove_redundant_punct,
    remove_non_digit_repetition,
    insert_space_for_nonarabic,
    correct_hamazat,
    reduce_multiple_spaces,
]
FILTERS_TYPE = Callable[[List[List[str]]], Tuple[bool, float]]


all_filters: List[FILTERS_TYPE] = [
    partial(passed_word_range_filter, min_=128, max_=100000),
    partial(passed_word_length_filter, min_=3, max_=10),
    partial(passed_symbol_ratio_filter, threshold_ratio=0.3),
    partial(passed_bullets_filter, threshold_ratio=0.9),
    partial(passed_ellipsis_filter, threshold_ratio=0.3),
    partial(passed_stopwords_filter, threshold=2),
    partial(passed_arabic_words_filter, threshold_ratio=0.5),
]


def doc_to_lines(doc: str) -> List[List[str]]:
    """
    Convert a string document into a list of list of tokens spliting first by line and
    then by space.

    Example:
        >>> doc_to_lines("Hello world\nI like the world\nGoodbye world.")
        [['Hello', 'world'], ['I', 'like', 'the', 'world'], ['Goodbye', 'world.']]
    """
    lined_doc = doc.split("\n")
    lined_doc_list = [l.split() for l in lined_doc]
    return lined_doc_list


def cleanse_document(
    doc: str, cleansers: Optional[List[Callable[[str], str]]] = None
) -> str:
    """
    Cleanse a string docuemnt by applying the list of cleansers.
    If `cleansers` is None, it uses all the default cleansers.
    """
    use_cleansers: List[Callable[[str], str]] = []
    if cleansers is None:
        use_cleansers = all_cleansers
    else:
        use_cleansers = cleansers
    for cleanser in use_cleansers:
        doc = cleanser(doc)
    return doc


def filter_document(
    doc: str, filters: Optional[List[FILTERS_TYPE]] = None
) -> List[Tuple[str, bool, float]]:
    """
    Filter a string docuemnt by applying the list of filters.
    If `filters` is None, it uses all the default filters.
    """
    use_filters: List[FILTERS_TYPE] = []
    if filters is None:
        use_filters = all_filters
    else:
        use_filters = filters

    doc_lines = doc_to_lines(doc)
    filter_results = []
    for filter_ in use_filters:
        passed, details = filter_(doc_lines)
        filter_name = ""
        if isinstance(filter_, partial):
            filter_name = filter_.func.__name__
        else:
            filter_name = filter_.__name__
        filter_results.append((filter_name, passed, details))
    return filter_results


def chunck_document(
    doc: str,
    chunk_max_size: Optional[int] = 768,
    sep: str = " ",
    apply_backward_stepping: bool = True,
) -> List[str]:
    """
    Split a string document into `chunk_max_size` with optional punctuation backtracking
    """
    if chunk_max_size is None:
        return [doc]
    tokenized_doc = doc.strip().split(sep)
    chunks = []
    from_ = 0
    to_ = chunk_max_size
    if not apply_backward_stepping:
        return [
            " ".join(tokenized_doc[from_ : from_ + chunk_max_size])
            for from_ in range(0, len(tokenized_doc), chunk_max_size)
        ]

    while to_ < len(tokenized_doc):
        step_back_counter = 0
        # while the token at `to_` is has at least one charater or the last charater
        # is not a punctuation and `to_` > 0, contintue backtracking
        while (
            len(tokenized_doc[to_]) == 0
            or tokenized_doc[to_][-1] not in PUNCTUATION_SET
        ) and to_ > 0:
            to_ -= 1
            step_back_counter += 1
            if step_back_counter > chunk_max_size // 4:
                break
        to_ += 1
        chunk = " ".join(tokenized_doc[from_:to_])
        chunks.append(chunk)
        from_ = to_
        to_ += chunk_max_size

    to_ = len(tokenized_doc)
    chunk = " ".join(tokenized_doc[from_:to_])
    chunks.append(chunk)
    return chunks


def clean_and_filter_docs(
    docs: List[str],
    cleansers: Optional[List[Callable[[str], str]]] = None,
    filters: Optional[List[FILTERS_TYPE]] = None,
    keep_filters_with_docs: bool = False,
    n_jobs=1,
) -> List[Union[str, Tuple[str, List[Tuple[str, bool, float]]]]]:
    filtered_and_cleansed_docs: List[
        Union[str, Tuple[str, List[Tuple[str, bool, float]]]]
    ] = []
    for doc in tqdm(docs):
        doc = cleanse_document(doc, cleansers=cleansers)
        docs_filters = filter_document(doc, filters=filters)
        if keep_filters_with_docs:
            filtered_and_cleansed_docs.append((doc, docs_filters))
        else:
            remove_doc = False
            for filter_ in docs_filters:
                if not filter_[1]:
                    remove_doc = True
                    break
            if not remove_doc:
                filtered_and_cleansed_docs.append(doc)
    return filtered_and_cleansed_docs


def clean_and_filter_json_docs(
    in_jsonl_path: str,
    text_field: str,
    out_jsonl_path: str,
    cleansers: Optional[List[Callable[[str], str]]] = None,
    filters: Optional[List[FILTERS_TYPE]] = None,
    keep_filters_with_docs: bool = False,
    n_jobs=1,
    chunk_max_size: Optional[int] = None,
    sep: str = " ",
    apply_backward_stepping: bool = True,
):
    with open(out_jsonl_path, "w") as f_out:
        with open(in_jsonl_path, "r") as f_in:
            for line in tqdm(f_in):
                doc = json.loads(line)
                doc_id = doc.get("id", in_jsonl_path)
                file_chunks = chunck_document(
                    doc[text_field],
                    chunk_max_size=chunk_max_size,
                    sep=sep,
                    apply_backward_stepping=apply_backward_stepping,
                )
                for chunk_id, chunk_doc in enumerate(file_chunks):
                    cleaned_docs = clean_and_filter_docs(
                        [chunk_doc],
                        cleansers=cleansers,
                        filters=filters,
                        keep_filters_with_docs=keep_filters_with_docs,
                        n_jobs=n_jobs,
                    )
                    if len(cleaned_docs) != 0:
                        if keep_filters_with_docs:
                            doc[text_field] = cleaned_docs[0][0]
                            doc["filters"] = cleaned_docs[0][1]
                        else:
                            doc[text_field] = cleaned_docs[0]
                        doc["id"] = f"chunk_{chunk_id}_{doc_id}"
                        f_out.write(json.dumps(doc, ensure_ascii=False))
                        f_out.write("\n")
