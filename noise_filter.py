import json
import random
import re
from collections import Counter

import re

def replace_line_with_rules(text, max_tokens=4):
    rules = [(
        [
            "انكلكيئ", "لكيئ", "العراك", "التاجك", "الذيك",
            "كيئ", "يحات", "اكك", "يتان", "ديك", "ذيك",
            "ريك", "زيك", "هلكي", "قلكت",
        ],
        "الديوان الملكي"
    )]

    # 🔥 Pre-check: skip everything if no tokens exist at all
    all_tokens = [t for tokens, _ in rules for t in tokens]
    if not any(token in text for token in all_tokens):
        return text  # 🚀 early exit

    def token_count(line):
        return len(re.findall(r"\S+", line))

    cleaned_lines = []

    for line in text.splitlines():
        replaced = False

        # 🔥 cheap check BEFORE regex
        if any(token in line for token in all_tokens):
            if token_count(line) <= max_tokens:
                for tokens, replacement in rules:
                    if any(token in line for token in tokens):
                        cleaned_lines.append(replacement)
                        replaced = True
                        break

        if not replaced:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def read_json_file(file_path):
    """
    Reads a JSON file and returns its content as a dictionary.
    
    :param file_path: Path to the JSON file
    :return: Dictionary containing JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return None



def is_special_char_ratio_more_than(text, threshold):
    """
    Returns True if the ratio of special characters in the text
    is greater than the given threshold.

    :param text: input string
    :param threshold: float (e.g., 0.5 for 50%)
    :return: bool
    """
    if not text:
        return True  # treat empty as noise

    # Anything NOT Arabic letters, English letters, digits, or whitespace
    special_chars = re.findall(r'[^a-zA-Z0-9\u0600-\u06FF\s]', text)

    ratio = len(special_chars) / len(text)

    return ratio > threshold


def is_latin_char_ratio_more_than(text, threshold):
    """
    Returns True if the ratio of Latin (English) characters
    in the text is greater than the given threshold.

    :param text: input string
    :param threshold: float (e.g., 0.2 for 20%)
    :return: bool
    """
    if not text:
        return False  # empty text → no Latin dominance

    # Match Latin letters only (a-z, A-Z)
    latin_chars = re.findall(r'[a-zA-Z]', text)

    ratio = len(latin_chars) / len(text)

    print(ratio)
    return ratio > threshold



def is_arabic_char_ratio_less_than(text, threshold):
    """
    Returns True if the ratio of Arabic characters in the text
    is less than the given threshold.

    :param text: input string
    :param threshold: float (e.g., 0.2 for 20%)
    :return: bool
    """
    if not text:
        return True  # empty → no Arabic → below threshold

    # Match Arabic characters
    arabic_chars = re.findall(r'[\u0600-\u06FF]', text)

    ratio = len(arabic_chars) / len(text)

    return ratio < threshold



def number_of_english_tokens(text):
    """
    Returns the number of English (Latin) word tokens in the text.

    A token is defined as a sequence of a-z or A-Z letters.

    :param text: input string
    :return: int
    """
    if not text:
        return 0

    tokens = re.findall(r'\b[a-zA-Z]+\b', text)

    return len(tokens)



def number_of_arabic_tokens(text):
    """
    Returns the number of Arabic word tokens in the text.

    A token is defined as a sequence of Arabic letters.

    :param text: input string
    :return: int
    """
    if not text:
        return 0

    # Match Arabic words (letters only)
    tokens = re.findall(r'[\u0621-\u064A]+', text)

    return len(tokens)

def is_all_numbers_or_special_chars(text):
    """
    Returns True if all characters in the text are either:
    - numbers (0-9, Arabic-Indic digits)
    - special characters (anything not Arabic/English letters or whitespace)

    :param text: input string
    :return: bool
    """
    if not text:
        return False  # empty text → not "all"

    # Match numbers (0-9, Arabic-Indic) OR special characters
    return all(re.match(r'[0-9\u0660-\u0669]|[^a-zA-Z\u0600-\u06FF\s]', ch) for ch in text)


def count_english_tokens(text) -> int:
    """
    Returns the number of English (Latin) word tokens in the text.

    A token is defined as a sequence of a-z or A-Z letters.

    :param text: input string
    :return: int
    """
    if not text:
        return 0

    tokens = re.findall(r'\b[a-zA-Z]+\b', text)
    return len(tokens)



def is_char_repeated_ratio(text, max_ratio_short=0.6, max_ratio_long=0.2, short_len=20):
    """
    Detect if any single character is repeated more than a given ratio of the text length.
    
    Parameters:
    - text: input string
    - max_ratio_short: max allowed repetition ratio for short text
    - max_ratio_long: max allowed repetition ratio for long text
    - short_len: length below which the text is considered "short"
    
    Returns:
    - True if text is likely noise due to repeated chars
    """
    if not text:
        return True  # empty → consider as noise

    n = len(text)
    
    # dynamic threshold: more aggressive for longer text
    if n <= short_len:
        threshold = max_ratio_short
    else:
        # linearly interpolate between short and long thresholds
        threshold = max_ratio_long + (max_ratio_short - max_ratio_long) * (short_len / n)

    # count characters
    counts = Counter(text)
    most_common_count = counts.most_common(1)[0][1]

    return (most_common_count / n) > threshold




cnt = 0
cleaned = []
bad = []

def is_text_bad(text):
    """
    Returns True if the text should be filtered as noise,
    based on multiple heuristics:
    - too short
    - too many special characters
    - too many Latin characters with few English tokens
    - repeated characters

    Uses your thresholds from the loop example.
    """
    if not text:
        return True

    # 1. Too short
    if len(text) <= 20:
        return True

    # 2. High special character ratio
    if is_special_char_ratio_more_than(text, threshold=0.17):
        return True

    # 3. High Latin ratio but few English tokens
    if is_latin_char_ratio_more_than(text, threshold=0.4) and count_english_tokens(text) < 10:
        return True

    # 4. Repeated characters
    if is_char_repeated_ratio(text):
        return True

    # Passed all checks → clean
    return False



# # usage
# for idx, text in enumerate(index):
#     if is_text_bad(text):
#         cnt += 1
#         bad.append(text)
#     else:
#         cleaned.append(text)
