import streamlit as st

import arabic_cleaning
from arabic_cleaning.text_cleansing import (
    correct_hamazat,
    fix_bad_encoding,
    hindi_numbers_to_arabic,
    normalize_similar_chars,
    reduce_multiple_spaces,
    remove_bad_chars,
    remove_diacritics_tatweel,
    remove_non_digit_repetition,
    remove_redundant_punct,
)

all_cleansers = [
    fix_bad_encoding,
    remove_bad_chars,
    remove_diacritics_tatweel,
    normalize_similar_chars,
    hindi_numbers_to_arabic,
    remove_redundant_punct,
    remove_non_digit_repetition,
    correct_hamazat,
    reduce_multiple_spaces,
]
from arabic_cleaning.cleaning_utils import clean_and_filter_docs


def main():
    """NER Streamlit App"""

    st.title("Text cleaning")
    st.sidebar.title(f"arabic_cleaning_lib version: {arabic_cleaning.__version__}")
    text = st.text_area(label="Text to be cleaned", placeholder="Enter your text here")
    if text != "":
        st.text_area(
            label="output_text",
            value=clean_and_filter_docs([text], all_cleansers, [])[0],
        )


if __name__ == "__main__":
    main()
