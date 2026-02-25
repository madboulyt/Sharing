import re

import ftfy
import pyarabic.araby as araby
import w3lib.html

from .constents import (
    BAD_CHARS,
    CHARS_REPLACEMENTS,
    HAMZA_MAP,
    SIMILAR_CHARS_MAP,
    arabic,
    ligatures,
)

# regex is taken from arabert
URL_REGEXES = [
    re.compile(
        r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    ),
    re.compile(r"@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS"),
    re.compile(r"http[s]?://[a-zA-Z0-9_\-./~\?=%&]+"),
    re.compile(r"www[a-zA-Z0-9_\-?=%&/.~]+"),
    re.compile(r"[a-zA-Z]+\.com"),
    re.compile(r"(?=http)[^\s]+"),
    re.compile(r"(?=www)[^\s]+"),
    re.compile(r"://"),
]

REDUNDANT_PUNCT_PATTERN = (
    r"([!\"#\$%\'\(\)\*\+,\.:;\-<=·>?@\[\\\]\^_ـ`{\|}~—٪’،؟`୍“؛”ۚ【»؛+«–…‘]{2,})"
)

MULTIPLE_CHAR_PATTERN = re.compile(r"(\D)\1{2,}", re.DOTALL)

USER_MENTION_REGEX = re.compile(r"@[\w\d]+")

EMAIL_REGEXES = [re.compile(r"[\w-]+@([\w-]+\.)+[\w-]+"), re.compile(r"\S+@\S+")]

_HINDI_NUMS = "٠١٢٣٤٥٦٧٨٩" + "۰۱۲۳۴۵۶۷۸۹"
_ARABIC_NUMS = "0123456789" + "0123456789"
HINDI_TO_ARABIC_MAP = str.maketrans(_HINDI_NUMS, _ARABIC_NUMS)


masking_values = {
    "url": ("[رابط]", "[ رابط ]"),
    "email": ("[بريد]", "[ بريد ]"),
    "user_mention": ("[مستخدم]", "[ مستخدم ]"),
}


def remove_bad_chars(doc: str) -> str:
    for char in BAD_CHARS:
        doc = doc.replace(char, " ")

    for from_, to_ in CHARS_REPLACEMENTS:
        doc = doc.replace(from_, to_)

    # doc = unicodedata.normalize("NFKD", doc)
    doc = doc.strip()
    return doc


def reduce_multiple_spaces(doc: str) -> str:
    doc = re.sub(" +", " ", doc)
    doc = re.sub("\r", "\n", doc)
    doc = re.sub("\n+", "\n", doc)
    doc = re.sub("\t+", "\t", doc)
    return doc


def remove_diacritics_tatweel(doc: str) -> str:
    doc = araby.strip_tashkeel(doc)
    doc = araby.strip_tatweel(doc)
    return doc


def mask_url(doc: str) -> str:
    mask = f' {masking_values["url"][0]} '
    for reg in URL_REGEXES:
        doc = reg.sub(mask, doc)
    return doc


def mask_email(doc: str) -> str:
    mask = f' {masking_values["email"][0]} '
    for reg in EMAIL_REGEXES:
        doc = reg.sub(mask, doc)
    return doc


def mask_user_mention(doc: str) -> str:
    mask = f' {masking_values["user_mention"][0]} '
    doc = USER_MENTION_REGEX.sub(mask, doc)
    return doc


def remove_html(doc: str) -> str:
    doc = w3lib.html.remove_tags(doc)
    return doc


def hindi_numbers_to_arabic(doc: str) -> str:
    doc = doc.translate(HINDI_TO_ARABIC_MAP)
    return doc


def remove_non_digit_repetition(doc: str) -> str:
    doc = MULTIPLE_CHAR_PATTERN.sub(r"\1\1", doc)
    return doc


def insert_space_for_nonarabic(doc: str) -> str:
    doc = re.sub(
        "([^0-9\u0621-\u063A\u0641-\u064A\u0660-\u0669\u0653-\u0655 ]+)",
        r" \1 ",
        doc,
    )

    # re-fix brackets
    for original_mask, fixed_mask in masking_values.values():
        doc = doc.replace(fixed_mask, original_mask)

    # insert whitespace between words and numbers or numbers and words
    doc = re.sub(
        "(\\d+)([\u0621-\u063A\u0641-\u064A\u066A-\u066C\u0653-\u0655]+)",
        r" \1 \2 ",
        doc,
    )
    doc = re.sub(
        "([\u0621-\u063A\u0641-\u064A\u066A-\u066C\u0653-\u0655]+)(\\d+)",
        r" \1 \2 ",
        doc,
    )

    return doc


def remove_redundant_punct(doc: str) -> str:
    doc_ = doc
    result = re.search(REDUNDANT_PUNCT_PATTERN, doc)
    dif = 0
    while result:
        sub_group = result.group()
        sub_list = sorted(set(sub_group), key=sub_group.index)
        sub = " " + "".join(list(sub_list)) + " "
        doc = "".join(
            (doc[: result.span()[0] + dif], sub, doc[result.span()[1] + dif :])
        )
        doc_ = "".join((doc_[: result.span()[0]], doc_[result.span()[1] :])).strip()
        dif = abs(len(doc) - len(doc_))
        result = re.search(REDUNDANT_PUNCT_PATTERN, doc_)
    # doc = re.sub(r"\s+", " ", doc)
    return doc.strip()


def fix_bad_encoding(doc: str) -> str:
    doc = ftfy.fix_encoding(doc)
    return doc


def normalize_similar_chars(doc: str) -> str:
    """
    Normalizes Farsi characters to Arabic characters rendered in the same way.
    Parameters:
        doc:
            input string that needs to be normalized.
    Returns `str`
    """
    # TODO to be enhanced
    new_doc = "".join([ligatures.LIGATURES_MAP.get(c, c) for c in doc])
    new_doc_ = [SIMILAR_CHARS_MAP.get(c, c) for c in new_doc]
    return "".join(new_doc_)


def correct_hamazat(doc: str) -> str:
    new_doc = []
    i = 0
    while i < len(doc):  # for i in range(len(doc)):
        c = doc[i : i + 2]
        if c in HAMZA_MAP:
            new_doc.append(HAMZA_MAP[c])
            i += 2
        else:
            new_doc.append(doc[i])
            i += 1
    return "".join(new_doc)


def remove_non_used_unicode_chrs(doc: str) -> str:
    chars_to_remove_set = set(arabic.CHARS_TO_BE_REMOVED_at_last_step)
    return "".join(c for c in doc if c not in chars_to_remove_set)
