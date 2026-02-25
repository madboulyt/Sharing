# from arabic_cleaning.constents import (
#     BAD_CHARS,
#     CHARS_REPLACEMENTS,
#     HAMZA_MAP,
#     PUNCTUATION_SET,
#     SIMILAR_CHARS_MAP,
# )
from arabic_cleaning.constents import arabic
from arabic_cleaning.text_cleansing import (
    normalize_similar_chars,
    remove_bad_chars,
    remove_non_used_unicode_chrs,
)


def test_remove_bad_chars():
    all_bad_chars = "\u200f \u200e \u202a \u202b \u2067 \u202e \u202c \u202d \u2069"
    assert remove_bad_chars(all_bad_chars) == ""


def test_normalize_similar_chars____basic_latters_do_not_chage():
    basic_arabic_characters = [
        (chr(0x621), "ARABIC LETTER HAMZA"),  # ء
        (chr(0x622), "ARABIC LETTER ALEF WITH MADDA ABOVE"),  # آ
        (chr(0x623), "ARABIC LETTER ALEF WITH HAMZA ABOVE"),  # أ
        (chr(0x624), "ARABIC LETTER WAW WITH HAMZA ABOVE"),  # ؤ
        (chr(0x625), "ARABIC LETTER ALEF WITH HAMZA BELOW"),  # إ
        (chr(0x626), "ARABIC LETTER YEH WITH HAMZA ABOVE"),  # ئ
        (chr(0x627), "ARABIC LETTER ALEF"),  # ا
        (chr(0x628), "ARABIC LETTER BEH"),  # ب
        (chr(0x629), "ARABIC LETTER TEH MARBUTA"),  # ة
        (chr(0x62A), "ARABIC LETTER TEH"),  # ت
        (chr(0x62B), "ARABIC LETTER THEH"),  # ث
        (chr(0x62C), "ARABIC LETTER JEEM"),  # ج
        (chr(0x62D), "ARABIC LETTER HAH"),  # ح
        (chr(0x62E), "ARABIC LETTER KHAH"),  # خ
        (chr(0x62F), "ARABIC LETTER DAL"),  # د
        (chr(0x630), "ARABIC LETTER THAL"),  # ذ
        (chr(0x631), "ARABIC LETTER REH"),  # ر
        (chr(0x632), "ARABIC LETTER ZAIN"),  # ز
        (chr(0x633), "ARABIC LETTER SEEN"),  # س
        (chr(0x634), "ARABIC LETTER SHEEN"),  # ش
        (chr(0x635), "ARABIC LETTER SAD"),  # ص
        (chr(0x636), "ARABIC LETTER DAD"),  # ض
        (chr(0x637), "ARABIC LETTER TAH"),  # ط
        (chr(0x638), "ARABIC LETTER ZAH"),  # ظ
        (chr(0x639), "ARABIC LETTER AIN"),  # ع
        (chr(0x63A), "ARABIC LETTER GHAIN"),  # غ
        # (chr(0x63b), "ARABIC LETTER KEHEH WITH TWO DOTS ABOVE" ), # ػ
        # (chr(0x63c), "ARABIC LETTER KEHEH WITH THREE DOTS BELOW" ), # ؼ
        # (chr(0x63d), "ARABIC LETTER FARSI YEH WITH INVERTED V" ), # ؽ
        # (chr(0x63e), "ARABIC LETTER FARSI YEH WITH TWO DOTS ABOVE" ), # ؾ
        # (chr(0x63f), "ARABIC LETTER FARSI YEH WITH THREE DOTS ABOVE" ), # ؿ
        # (chr(0x640), "ARABIC TATWEEL" ), # ـ
        (chr(0x641), "ARABIC LETTER FEH"),  # ف
        (chr(0x642), "ARABIC LETTER QAF"),  # ق
        (chr(0x643), "ARABIC LETTER KAF"),  # ك
        (chr(0x644), "ARABIC LETTER LAM"),  # ل
        (chr(0x645), "ARABIC LETTER MEEM"),  # م
        (chr(0x646), "ARABIC LETTER NOON"),  # ن
        (chr(0x647), "ARABIC LETTER HEH"),  # ه
        (chr(0x648), "ARABIC LETTER WAW"),  # و
        (chr(0x649), "ARABIC LETTER ALEF MAKSURA"),  # ى
        (chr(0x64A), "ARABIC LETTER YEH"),  # ي
        ("١٢٣٤٥٧٨٩٠", "ARABIC Digits"),
        ("1234567890", "English Digits"),
    ]
    for char, _ in basic_arabic_characters:
        assert normalize_similar_chars(char) == char


def test_remove_non_used_unicode_chrs():
    text = "".join(arabic.CHARS_TO_BE_REMOVED_at_last_step) + "123"
    assert remove_non_used_unicode_chrs(text) == "123"
