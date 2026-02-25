# all arabic letters unicode: https://www.unicode.org/charts/PDF/U0600.pdf

EMPTY_STR = ""
SIMILAR_CHARS_MAP_EXHAUSTIVE = {
    chr(0xFBDD): "ؤ",  # ARABIC LETTER U WITH HAMZA ABOVE ISOLATED FORM - ﯝ -  ۇٴ - 2
    chr(0xFE70): chr(0x64B),  # ARABIC FATHATAN ISOLATED FORM - ﹰ -   ً - 2
    chr(0xFE72): chr(0x64C),  # ARABIC DAMMATAN ISOLATED FORM - ﹲ -   ٌ - 2
    chr(0xFE74): chr(0x64D),  # ARABIC KASRATAN ISOLATED FORM - ﹴ -   ٍ - 2
    chr(0xFE76): chr(0x64E),  # ARABIC FATHA ISOLATED FORM - ﹶ -   َ - 2
    chr(0xFE77): chr(0x64E),  # ARABIC FATHA MEDIAL FORM - ﹷ -  ـَ - 2
    chr(0xFE78): chr(0x64F),  # ARABIC DAMMA ISOLATED FORM - ﹸ -   ُ - 2
    chr(0xFE79): chr(0x64F),  # ARABIC DAMMA MEDIAL FORM - ﹹ -  ـُ - 2
    chr(0xFE7A): chr(0x650),  # ARABIC KASRA ISOLATED FORM - ﹺ -   ِ - 2
    chr(0xFE7B): chr(0x650),  # ARABIC KASRA MEDIAL FORM - ﹻ -  ـِ - 2
    chr(0xFE7C): chr(0x651),  # ARABIC SHADDA ISOLATED FORM - ﹼ -   ّ - 2
    chr(0xFE7D): chr(0x651),  # ARABIC SHADDA MEDIAL FORM - ﹽ -  ـّ - 2
    chr(0xFE7E): chr(0x652),  # ARABIC SUKUN ISOLATED FORM - ﹾ -   ْ - 2
    chr(0xFE7F): chr(0x652),  # ARABIC SUKUN MEDIAL FORM - ﹿ -  ـْ - 2
    chr(0x8E4): chr(0x64E),  # ARABIC CURLY FATHA - ࣤ -  ࣤ - 1
    chr(0x8E5): chr(0x64F),  # ARABIC CURLY DAMMA - ࣥ -  ࣥ - 1
    chr(0x8E6): chr(0x650),  # ARABIC CURLY KASRA - ࣦ -  ࣦ - 1
    chr(0x8E7): chr(0x64B),  # ARABIC CURLY FATHATAN - ࣧ -  ࣧ - 1
    chr(0x8E8): chr(0x64C),  # ARABIC CURLY DAMMATAN - ࣨ -  ࣨ - 1
    chr(0x8E9): chr(0x64D),  # ARABIC CURLY KASRATAN - ࣩ -  ࣩ - 1
    chr(0x8F0): chr(0x64B),  # ARABIC OPEN FATHATAN - ࣰ -  ࣰ - 1
    chr(0x8F1): chr(0x64C),  # ARABIC OPEN DAMMATAN - ࣱ -  ࣱ - 1
    chr(0x8F2): chr(0x64D),  # ARABIC OPEN KASRATAN - ࣲ -  ࣲ - 1
    chr(0x618): chr(0x64E),  # ARABIC SMALL FATHA - ؘ -  ؘ - 1
    chr(0x619): chr(0x64F),  # ARABIC SMALL DAMMA - ؙ -  ؙ - 1
    chr(0x61A): chr(0x650),  # ARABIC SMALL KASRA - ؚ -  ؚ - 1
    chr(0x8F6): chr(0x650),  # ARABIC KASRA WITH DOT BELOW - ࣶ -  ࣶ - 1
    chr(0x8F4): chr(0x64E),  # ARABIC FATHA WITH RING - ࣴ -  ࣴ - 1
    chr(0x8F5): chr(0x64E),  # ARABIC FATHA WITH DOT ABOVE - ࣵ -  ࣵ - 1
    chr(0x65E): chr(0x64E),  # ARABIC FATHA WITH TWO DOTS - ٞ -  ٞ - 1
    chr(0x657): chr(0x64F),  # ARABIC INVERTED DAMMA - ٗ -  ٗ - 1
    chr(0x65D): chr(0x64F),  # ARABIC REVERSED DAMMA - ٝ -  ٝ - 1
    chr(0x8FE): chr(0x64F),  # ARABIC DAMMA WITH DOT - ࣾ -  ࣾ - 1
    chr(0xFE71): EMPTY_STR,  # ARABIC TATWEEL WITH FATHATAN ABOVE - ﹱ -  ـً - 2
    chr(0xFE73): EMPTY_STR  # ARABIC TAIL FRAGMENT - ﹳ -  ﹳ - 1
    # ---------
    # The following should be mapped to 0x627, ARABIC LETTER ALEF, ا
    ,
    chr(0x773): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH EXTENDED ARABIC-INDIC DIGIT TWO ABOVE, ݳ
    chr(0x774): chr(
        0x627
    )  # ARABIC LETTER ALEF WITH EXTENDED ARABIC-INDIC DIGIT THREE ABOVE, ݴ
    # Alef with some addition
    ,
    chr(0x870): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED FATHA, ࡰ
    chr(0x871): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED TOP RIGHT FATHA, ࡱ
    chr(0x874): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED KASRA, ࡴ
    chr(0x875): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED BOTTOM RIGHT KASRA, ࡵ
    chr(0x876): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED ROUND DOT ABOVE, ࡶ
    chr(0x877): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED RIGHT ROUND DOT, ࡷ
    chr(0x878): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED LEFT ROUND DOT, ࡸ
    chr(0x879): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED ROUND DOT BELOW, ࡹ
    chr(0x87B): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH ATTACHED TOP RIGHT FATHA AND DOT ABOVE, ࡻ
    chr(0x880): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH ATTACHED BOTTOM RIGHT KASRA AND LEFT RING, ࢀ
    chr(0x87D): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH ATTACHED BOTTOM RIGHT KASRA AND DOT ABOVE, ࡽ
    chr(0x87E): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH ATTACHED TOP RIGHT FATHA AND LEFT RING, ࡾ
    chr(0x881): chr(0x627),  # ARABIC LETTER ALEF WITH ATTACHED RIGHT HAMZA, ࢁ
    chr(0x882): chr(0x627)  # ARABIC LETTER ALEF WITH ATTACHED LEFT HAMZA, ࢂ
    #
    ,
    chr(0x872): chr(0x627),  # ARABIC LETTER ALEF WITH RIGHT MIDDLE STROKE, ࡲ
    chr(0x873): chr(0x627),  # ARABIC LETTER ALEF WITH LEFT MIDDLE STROKE, ࡳ
    chr(0x87A): chr(0x627),  # ARABIC LETTER ALEF WITH DOT ABOVE, ࡺ
    chr(0x87C): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH RIGHT MIDDLE STROKE AND DOT ABOVE, ࡼ
    chr(0x87F): chr(
        0x627
    ),  # ARABIC LETTER ALEF WITH RIGHT MIDDLE STROKE AND LEFT RING, ࡿ
    chr(0x8AD): chr(0x627),  # ARABIC LETTER LOW ALEF, ࢭ
    chr(0xFB50): chr(0x627),  # ARABIC LETTER ALEF WASLA ISOLATED FORM, ﭐ
    chr(0xFB51): chr(0x627),  # ARABIC LETTER ALEF WASLA FINAL FORM, ﭑ
    chr(0x10A71): chr(0x627),  # OLD SOUTH ARABIAN LETTER ALEF, 𐩱
    chr(0x10A91): chr(0x627),  # OLD NORTH ARABIAN LETTER ALEF, 𐪑
    chr(0x1EE00): chr(0x627),  # ARABIC MATHEMATICAL ALEF, 𞸀
    chr(0x1EE80): chr(0x627)  # ARABIC MATHEMATICAL LOOPED ALEF, 𞺀
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x628, ARABIC LETTER BEH, ب
    ,
    chr(0x66E): chr(0x628),  # ARABIC LETTER DOTLESS BEH, ٮ
    chr(0x750): chr(0x628),  # ARABIC LETTER BEH WITH THREE DOTS HORIZONTALLY BELOW, ݐ
    chr(0x751): chr(0x628),  # ARABIC LETTER BEH WITH DOT BELOW AND THREE DOTS ABOVE, ݑ
    chr(0x752): chr(
        0x628
    ),  # ARABIC LETTER BEH WITH THREE DOTS POINTING UPWARDS BELOW, ݒ
    chr(0x753): chr(
        0x628
    ),  # ARABIC LETTER BEH WITH THREE DOTS POINTING UPWARDS BELOW AND TWO DOTS ABOVE, ݓ
    chr(0x754): chr(0x628),  # ARABIC LETTER BEH WITH TWO DOTS BELOW AND DOT ABOVE, ݔ
    chr(0x755): chr(0x628),  # ARABIC LETTER BEH WITH INVERTED SMALL V BELOW, ݕ
    chr(0x756): chr(0x628),  # ARABIC LETTER BEH WITH SMALL V, ݖ
    chr(0x8A0): chr(0x628),  # ARABIC LETTER BEH WITH SMALL V BELOW, ࢠ
    chr(0x8A1): chr(0x628),  # ARABIC LETTER BEH WITH HAMZA ABOVE, ࢡ
    chr(0x8B6): chr(0x628),  # ARABIC LETTER BEH WITH SMALL MEEM ABOVE, ࢶ
    chr(0x10A88): chr(0x628),  # OLD NORTH ARABIAN LETTER BEH, 𐪈
    chr(0x1EE01): chr(0x628),  # ARABIC MATHEMATICAL BEH, 𞸁
    chr(0x1EE1C): chr(0x628),  # ARABIC MATHEMATICAL DOTLESS BEH, 𞸜
    chr(0x1EE21): chr(0x628),  # ARABIC MATHEMATICAL INITIAL BEH, 𞸡
    chr(0x1EE61): chr(0x628),  # ARABIC MATHEMATICAL STRETCHED BEH, 𞹡
    chr(0x1EE7C): chr(0x628),  # ARABIC MATHEMATICAL STRETCHED DOTLESS BEH, 𞹼
    chr(0x1EE81): chr(0x628),  # ARABIC MATHEMATICAL LOOPED BEH, 𞺁
    chr(0x1EEA1): chr(0x628),  # ARABIC MATHEMATICAL DOUBLE-STRUCK BEH, 𞺡
    chr(0xFB52): chr(0x628),  # ARABIC LETTER BEEH ISOLATED FORM - ﭒ -  ٻ - 1
    chr(0xFB53): chr(0x628),  # ARABIC LETTER BEEH FINAL FORM - ﭓ -  ٻ - 1
    chr(0xFB54): chr(0x628),  # ARABIC LETTER BEEH INITIAL FORM - ﭔ -  ٻ - 1
    chr(0xFB55): chr(0x628),  # ARABIC LETTER BEEH MEDIAL FORM - ﭕ -  ٻ - 1
    chr(0xFB5A): chr(0x628),  # ARABIC LETTER BEHEH ISOLATED FORM - ﭚ -  ڀ - 1
    chr(0xFB5B): chr(0x628),  # ARABIC LETTER BEHEH FINAL FORM - ﭛ -  ڀ - 1
    chr(0xFB5C): chr(0x628),  # ARABIC LETTER BEHEH INITIAL FORM - ﭜ -  ڀ - 1
    chr(0xFB5D): chr(0x628),  # ARABIC LETTER BEHEH MEDIAL FORM - ﭝ -  ڀ - 1
    chr(0x680): chr(0x628),  # ARABIC LETTER BEHEH - ڀ -  ڀ - 1
    chr(0x8B7): chr(0x628),  # ARABIC LETTER PEH WITH SMALL MEEM ABOVE - ࢷ -  ࢷ - 1
    chr(0x8BE): chr(0x628)  # ARABIC LETTER PEH WITH SMALL V - ࢾ -  ࢾ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x629, ARABIC LETTER TEH MARBUTA, ة
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62a, ARABIC LETTER TEH, ت
    ,
    chr(0x8B8): chr(0x62A),  # ARABIC LETTER TEH WITH SMALL TEH ABOVE, ࢸ
    chr(0x8BF): chr(0x62A),  # ARABIC LETTER TEH WITH SMALL V, ࢿ
    chr(0x10A89): chr(0x62A),  # OLD NORTH ARABIAN LETTER TEH, 𐪉
    chr(0x1EE15): chr(0x62A),  # ARABIC MATHEMATICAL TEH, 𞸕
    chr(0x1EE35): chr(0x62A),  # ARABIC MATHEMATICAL INITIAL TEH, 𞸵
    chr(0x1EE75): chr(0x62A),  # ARABIC MATHEMATICAL STRETCHED TEH, 𞹵
    chr(0x1EE95): chr(0x62A),  # ARABIC MATHEMATICAL LOOPED TEH, 𞺕
    chr(0x1EEB5): chr(0x62A),  # ARABIC MATHEMATICAL DOUBLE-STRUCK TEH, 𞺵
    chr(0xFB5E): chr(0x62A),  # ARABIC LETTER TTEHEH ISOLATED FORM - ﭞ -  ٺ - 1
    chr(0xFB5F): chr(0x62A),  # ARABIC LETTER TTEHEH FINAL FORM - ﭟ -  ٺ - 1
    chr(0xFB60): chr(0x62A),  # ARABIC LETTER TTEHEH INITIAL FORM - ﭠ -  ٺ - 1
    chr(0xFB61): chr(0x62A),  # ARABIC LETTER TTEHEH MEDIAL FORM - ﭡ -  ٺ - 1
    chr(0xFB62): chr(0x62A),  # ARABIC LETTER TEHEH ISOLATED FORM - ﭢ -  ٿ - 1
    chr(0xFB63): chr(0x62A),  # ARABIC LETTER TEHEH FINAL FORM - ﭣ -  ٿ - 1
    chr(0xFB64): chr(0x62A),  # ARABIC LETTER TEHEH INITIAL FORM - ﭤ -  ٿ - 1
    chr(0xFB65): chr(0x62A),  # ARABIC LETTER TEHEH MEDIAL FORM - ﭥ -  ٿ - 1
    chr(0xFB66): chr(0x62A),  # ARABIC LETTER TTEH ISOLATED FORM - ﭦ -  ٹ - 1
    chr(0xFB67): chr(0x62A),  # ARABIC LETTER TTEH FINAL FORM - ﭧ -  ٹ - 1
    chr(0xFB68): chr(0x62A),  # ARABIC LETTER TTEH INITIAL FORM - ﭨ -  ٹ - 1
    chr(0xFB69): chr(0x62A),  # ARABIC LETTER TTEH MEDIAL FORM - ﭩ -  ٹ - 1
    chr(0x8C0): chr(0x62A)  # ARABIC LETTER TTEH WITH SMALL V - ࣀ -  ࣀ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62b, ARABIC LETTER THEH, ث
    ,
    chr(0x10A9B): chr(0x62B),  # OLD NORTH ARABIAN LETTER THEH, 𐪛
    chr(0x1EE16): chr(0x62B),  # ARABIC MATHEMATICAL THEH, 𞸖
    chr(0x1EE36): chr(0x62B),  # ARABIC MATHEMATICAL INITIAL THEH, 𞸶
    chr(0x1EE76): chr(0x62B),  # ARABIC MATHEMATICAL STRETCHED THEH, 𞹶
    chr(0x1EE96): chr(0x62B),  # ARABIC MATHEMATICAL LOOPED THEH, 𞺖
    chr(0x1EEB6): chr(0x62B)  # ARABIC MATHEMATICAL DOUBLE-STRUCK THEH, 𞺶
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62c, ARABIC LETTER JEEM, ج
    ,
    chr(0x8A2): chr(0x62C),  # ARABIC LETTER JEEM WITH TWO DOTS ABOVE, ࢢ
    chr(0x8C5): chr(0x62C),  # ARABIC LETTER JEEM WITH THREE DOTS ABOVE, ࣅ
    chr(0x8C6): chr(0x62C),  # ARABIC LETTER JEEM WITH THREE DOTS BELOW, ࣆ
    chr(0x1EE02): chr(0x62C),  # ARABIC MATHEMATICAL JEEM, 𞸂
    chr(0x1EE22): chr(0x62C),  # ARABIC MATHEMATICAL INITIAL JEEM, 𞸢
    chr(0x1EE42): chr(0x62C),  # ARABIC MATHEMATICAL TAILED JEEM, 𞹂
    chr(0x1EE62): chr(0x62C),  # ARABIC MATHEMATICAL STRETCHED JEEM, 𞹢
    chr(0x1EE82): chr(0x62C),  # ARABIC MATHEMATICAL LOOPED JEEM, 𞺂
    chr(0x1EEA2): chr(0x62C),  # ARABIC MATHEMATICAL DOUBLE-STRUCK JEEM, 𞺢
    chr(0xFB72): chr(0x62C),  # ARABIC LETTER DYEH ISOLATED FORM - ﭲ -  ڄ - 1
    chr(0xFB73): chr(0x62C),  # ARABIC LETTER DYEH FINAL FORM - ﭳ -  ڄ - 1
    chr(0xFB74): chr(0x62C),  # ARABIC LETTER DYEH INITIAL FORM - ﭴ -  ڄ - 1
    chr(0xFB75): chr(0x62C),  # ARABIC LETTER DYEH MEDIAL FORM - ﭵ -  ڄ - 1
    chr(0xFB76): chr(0x62C),  # ARABIC LETTER NYEH ISOLATED FORM - ﭶ -  ڃ - 1
    chr(0xFB77): chr(0x62C),  # ARABIC LETTER NYEH FINAL FORM - ﭷ -  ڃ - 1
    chr(0xFB78): chr(0x62C),  # ARABIC LETTER NYEH INITIAL FORM - ﭸ -  ڃ - 1
    chr(0xFB79): chr(0x62C),  # ARABIC LETTER NYEH MEDIAL FORM - ﭹ -  ڃ - 1
    chr(0xFB7E): chr(0x62C),  # ARABIC LETTER TCHEHEH ISOLATED FORM - ﭾ -  ڇ - 1
    chr(0xFB7F): chr(0x62C),  # ARABIC LETTER TCHEHEH FINAL FORM - ﭿ -  ڇ - 1
    chr(0xFB80): chr(0x62C),  # ARABIC LETTER TCHEHEH INITIAL FORM - ﮀ -  ڇ - 1
    chr(0xFB81): chr(0x62C),  # ARABIC LETTER TCHEHEH MEDIAL FORM - ﮁ -  ڇ - 1
    chr(0x8C1): chr(0x62C)  # ARABIC LETTER TCHEH WITH SMALL V - ࣁ -  ࣁ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62d, ARABIC LETTER HAH, ح
    ,
    chr(0x757): chr(0x62D),  # ARABIC LETTER HAH WITH TWO DOTS ABOVE, ݗ
    chr(0x758): chr(
        0x62D
    ),  # ARABIC LETTER HAH WITH THREE DOTS POINTING UPWARDS BELOW, ݘ
    chr(0x76E): chr(0x62D),  # ARABIC LETTER HAH WITH SMALL ARABIC LETTER TAH BELOW, ݮ
    chr(0x76F): chr(
        0x62D
    ),  # ARABIC LETTER HAH WITH SMALL ARABIC LETTER TAH AND TWO DOTS, ݯ
    chr(0x772): chr(0x62D),  # ARABIC LETTER HAH WITH SMALL ARABIC LETTER TAH ABOVE, ݲ
    chr(0x77C): chr(
        0x62D
    ),  # ARABIC LETTER HAH WITH EXTENDED ARABIC-INDIC DIGIT FOUR BELOW, ݼ
    chr(0x88A): chr(0x62D),  # ARABIC LETTER HAH WITH INVERTED SMALL V BELOW, ࢊ
    chr(0x10A82): chr(0x62D),  # OLD NORTH ARABIAN LETTER HAH, 𐪂
    chr(0x1EE07): chr(0x62D),  # ARABIC MATHEMATICAL HAH, 𞸇
    chr(0x1EE27): chr(0x62D),  # ARABIC MATHEMATICAL INITIAL HAH, 𞸧
    chr(0x1EE47): chr(0x62D),  # ARABIC MATHEMATICAL TAILED HAH, 𞹇
    chr(0x1EE67): chr(0x62D),  # ARABIC MATHEMATICAL STRETCHED HAH, 𞹧
    chr(0x1EE87): chr(0x62D),  # ARABIC MATHEMATICAL LOOPED HAH, 𞺇
    chr(0x1EEA7): chr(0x62D)  # ARABIC MATHEMATICAL DOUBLE-STRUCK HAH, 𞺧
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62e, ARABIC LETTER KHAH, خ
    ,
    chr(0x10A8D): chr(0x62E),  # OLD NORTH ARABIAN LETTER KHAH, 𐪍
    chr(0x1EE17): chr(0x62E),  # ARABIC MATHEMATICAL KHAH, 𞸗
    chr(0x1EE37): chr(0x62E),  # ARABIC MATHEMATICAL INITIAL KHAH, 𞸷
    chr(0x1EE57): chr(0x62E),  # ARABIC MATHEMATICAL TAILED KHAH, 𞹗
    chr(0x1EE77): chr(0x62E),  # ARABIC MATHEMATICAL STRETCHED KHAH, 𞹷
    chr(0x1EE97): chr(0x62E),  # ARABIC MATHEMATICAL LOOPED KHAH, 𞺗
    chr(0x1EEB7): chr(0x62E)  # ARABIC MATHEMATICAL DOUBLE-STRUCK KHAH, 𞺷
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x62f, ARABIC LETTER DAL, د
    ,
    chr(0x690): chr(0x62F),  # ARABIC LETTER DAL WITH FOUR DOTS ABOVE, ڐ
    chr(0x759): chr(
        0x62F
    ),  # ARABIC LETTER DAL WITH TWO DOTS VERTICALLY BELOW AND SMALL TAH, ݙ
    chr(0x75A): chr(0x62F),  # ARABIC LETTER DAL WITH INVERTED SMALL V BELOW, ݚ
    chr(0x8AE): chr(0x62F),  # ARABIC LETTER DAL WITH THREE DOTS BELOW, ࢮ
    chr(0x10A95): chr(0x62F),  # OLD NORTH ARABIAN LETTER DAL, 𐪕
    chr(0x1EE03): chr(0x62F),  # ARABIC MATHEMATICAL DAL, 𞸃
    chr(0x1EE83): chr(0x62F),  # ARABIC MATHEMATICAL LOOPED DAL, 𞺃
    chr(0x1EEA3): chr(0x62F),  # ARABIC MATHEMATICAL DOUBLE-STRUCK DAL, 𞺣
    chr(0xFB82): chr(0x62F),  # ARABIC LETTER DDAHAL ISOLATED FORM - ﮂ -  ڍ - 1
    chr(0xFB83): chr(0x62F),  # ARABIC LETTER DDAHAL FINAL FORM - ﮃ -  ڍ - 1
    chr(0xFB84): chr(0x62F),  # ARABIC LETTER DAHAL ISOLATED FORM - ﮄ -  ڌ - 1
    chr(0xFB85): chr(0x62F),  # ARABIC LETTER DAHAL FINAL FORM - ﮅ -  ڌ - 1
    chr(0xFB86): chr(0x62F),  # ARABIC LETTER DUL ISOLATED FORM - ﮆ -  ڎ - 1
    chr(0xFB87): chr(0x62F),  # ARABIC LETTER DUL FINAL FORM - ﮇ -  ڎ - 1
    chr(0xFB88): chr(0x62F),  # ARABIC LETTER DDAL ISOLATED FORM - ﮈ -  ڈ - 1
    chr(0xFB89): chr(0x62F)  # ARABIC LETTER DDAL FINAL FORM - ﮉ -  ڈ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x630, ARABIC LETTER THAL, ذ
    ,
    chr(0x10A99): chr(0x630),  # OLD NORTH ARABIAN LETTER THAL, 𐪙
    chr(0x1EE18): chr(0x630),  # ARABIC MATHEMATICAL THAL, 𞸘
    chr(0x1EE98): chr(0x630),  # ARABIC MATHEMATICAL LOOPED THAL, 𞺘
    chr(0x1EEB8): chr(0x630)  # ARABIC MATHEMATICAL DOUBLE-STRUCK THAL, 𞺸
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x631, ARABIC LETTER REH, ر
    ,
    chr(0x693): chr(0x631),  # ARABIC LETTER REH WITH RING, ړ
    chr(0x696): chr(0x631),  # ARABIC LETTER REH WITH DOT BELOW AND DOT ABOVE, ږ
    chr(0x699): chr(0x631),  # ARABIC LETTER REH WITH FOUR DOTS ABOVE, ڙ
    chr(0x75B): chr(0x631),  # ARABIC LETTER REH WITH STROKE, ݛ
    chr(0x76B): chr(0x631),  # ARABIC LETTER REH WITH TWO DOTS VERTICALLY ABOVE, ݫ
    chr(0x76C): chr(0x631),  # ARABIC LETTER REH WITH HAMZA ABOVE, ݬ
    chr(0x771): chr(
        0x631
    ),  # ARABIC LETTER REH WITH SMALL ARABIC LETTER TAH AND TWO DOTS, ݱ
    chr(0x8AA): chr(0x631),  # ARABIC LETTER REH WITH LOOP, ࢪ
    chr(0x8B9): chr(0x631),  # ARABIC LETTER REH WITH SMALL NOON ABOVE, ࢹ
    chr(0x10A87): chr(0x631),  # OLD NORTH ARABIAN LETTER REH, 𐪇
    chr(0x1EE13): chr(0x631),  # ARABIC MATHEMATICAL REH, 𞸓
    chr(0x1EE93): chr(0x631),  # ARABIC MATHEMATICAL LOOPED REH, 𞺓
    chr(0x1EEB3): chr(0x631),  # ARABIC MATHEMATICAL DOUBLE-STRUCK REH, 𞺳
    chr(0xFB8C): chr(0x631),  # ARABIC LETTER RREH ISOLATED FORM - ﮌ -  ڑ - 1
    chr(0xFB8D): chr(0x631),  # ARABIC LETTER RREH FINAL FORM - ﮍ -  ڑ - 1
    chr(0x691): chr(0x631)  # ARABIC LETTER RREH - ڑ -  ڑ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x632, ARABIC LETTER ZAIN, ز
    ,
    chr(0x8B2): chr(0x632),  # ARABIC LETTER ZAIN WITH INVERTED V ABOVE, ࢲ
    chr(0x10A98): chr(0x632),  # OLD NORTH ARABIAN LETTER ZAIN, 𐪘
    chr(0x1EE06): chr(0x632),  # ARABIC MATHEMATICAL ZAIN, 𞸆
    chr(0x1EE86): chr(0x632),  # ARABIC MATHEMATICAL LOOPED ZAIN, 𞺆
    chr(0x1EEA6): chr(0x632)  # ARABIC MATHEMATICAL DOUBLE-STRUCK ZAIN, 𞺦
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x633, ARABIC LETTER SEEN, س
    ,
    chr(0x75C): chr(0x633),  # ARABIC LETTER SEEN WITH FOUR DOTS ABOVE, ݜ
    chr(0x76D): chr(0x633),  # ARABIC LETTER SEEN WITH TWO DOTS VERTICALLY ABOVE, ݭ
    chr(0x770): chr(
        0x633
    ),  # ARABIC LETTER SEEN WITH SMALL ARABIC LETTER TAH AND TWO DOTS, ݰ
    chr(0x77D): chr(
        0x633
    ),  # ARABIC LETTER SEEN WITH EXTENDED ARABIC-INDIC DIGIT FOUR ABOVE, ݽ
    chr(0x77E): chr(0x633),  # ARABIC LETTER SEEN WITH INVERTED V, ݾ
    chr(0x1EE0E): chr(0x633),  # ARABIC MATHEMATICAL SEEN, 𞸎
    chr(0x1EE2E): chr(0x633),  # ARABIC MATHEMATICAL INITIAL SEEN, 𞸮
    chr(0x1EE4E): chr(0x633),  # ARABIC MATHEMATICAL TAILED SEEN, 𞹎
    chr(0x1EE6E): chr(0x633),  # ARABIC MATHEMATICAL STRETCHED SEEN, 𞹮
    chr(0x1EE8E): chr(0x633),  # ARABIC MATHEMATICAL LOOPED SEEN, 𞺎
    chr(0x1EEAE): chr(0x633)  # ARABIC MATHEMATICAL DOUBLE-STRUCK SEEN, 𞺮
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x634, ARABIC LETTER SHEEN, ش
    ,
    chr(0x1EE14): chr(0x634),  # ARABIC MATHEMATICAL SHEEN, 𞸔
    chr(0x1EE34): chr(0x634),  # ARABIC MATHEMATICAL INITIAL SHEEN, 𞸴
    chr(0x1EE54): chr(0x634),  # ARABIC MATHEMATICAL TAILED SHEEN, 𞹔
    chr(0x1EE74): chr(0x634),  # ARABIC MATHEMATICAL STRETCHED SHEEN, 𞹴
    chr(0x1EE94): chr(0x634),  # ARABIC MATHEMATICAL LOOPED SHEEN, 𞺔
    chr(0x1EEB4): chr(0x634)  # ARABIC MATHEMATICAL DOUBLE-STRUCK SHEEN, 𞺴
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x635, ARABIC LETTER SAD, ص
    ,
    chr(0x8AF): chr(0x635),  # ARABIC LETTER SAD WITH THREE DOTS BELOW, ࢯ
    chr(0x10A8E): chr(0x635),  # OLD NORTH ARABIAN LETTER SAD, 𐪎
    chr(0x1EE11): chr(0x635),  # ARABIC MATHEMATICAL SAD, 𞸑
    chr(0x1EE31): chr(0x635),  # ARABIC MATHEMATICAL INITIAL SAD, 𞸱
    chr(0x1EE51): chr(0x635),  # ARABIC MATHEMATICAL TAILED SAD, 𞹑
    chr(0x1EE71): chr(0x635),  # ARABIC MATHEMATICAL STRETCHED SAD, 𞹱
    chr(0x1EE91): chr(0x635),  # ARABIC MATHEMATICAL LOOPED SAD, 𞺑
    chr(0x1EEB1): chr(0x635)  # ARABIC MATHEMATICAL DOUBLE-STRUCK SAD, 𞺱
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x636, ARABIC LETTER DAD, ض
    ,
    chr(0x10A93): chr(0x636),  # OLD NORTH ARABIAN LETTER DAD, 𐪓
    chr(0x1EE19): chr(0x636),  # ARABIC MATHEMATICAL DAD, 𞸙
    chr(0x1EE39): chr(0x636),  # ARABIC MATHEMATICAL INITIAL DAD, 𞸹
    chr(0x1EE59): chr(0x636),  # ARABIC MATHEMATICAL TAILED DAD, 𞹙
    chr(0x1EE79): chr(0x636),  # ARABIC MATHEMATICAL STRETCHED DAD, 𞹹
    chr(0x1EE99): chr(0x636),  # ARABIC MATHEMATICAL LOOPED DAD, 𞺙
    chr(0x1EEB9): chr(0x636)  # ARABIC MATHEMATICAL DOUBLE-STRUCK DAD, 𞺹
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x637, ARABIC LETTER TAH, ط
    ,
    chr(0x88B): chr(0x637),  # ARABIC LETTER TAH WITH DOT BELOW, ࢋ
    chr(0x88C): chr(0x637),  # ARABIC LETTER TAH WITH THREE DOTS BELOW, ࢌ
    chr(0x8A3): chr(0x637),  # ARABIC LETTER TAH WITH TWO DOTS ABOVE, ࢣ
    chr(0x10A97): chr(0x637),  # OLD NORTH ARABIAN LETTER TAH, 𐪗
    chr(0x1EE08): chr(0x637),  # ARABIC MATHEMATICAL TAH, 𞸈
    chr(0x1EE68): chr(0x637),  # ARABIC MATHEMATICAL STRETCHED TAH, 𞹨
    chr(0x1EE88): chr(0x637),  # ARABIC MATHEMATICAL LOOPED TAH, 𞺈
    chr(0x1EEA8): chr(0x637)  # ARABIC MATHEMATICAL DOUBLE-STRUCK TAH, 𞺨
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x638, ARABIC LETTER ZAH, ظ
    ,
    chr(0x10A9C): chr(0x638),  # OLD NORTH ARABIAN LETTER ZAH, 𐪜
    chr(0x1EE1A): chr(0x638),  # ARABIC MATHEMATICAL ZAH, 𞸚
    chr(0x1EE7A): chr(0x638),  # ARABIC MATHEMATICAL STRETCHED ZAH, 𞹺
    chr(0x1EE9A): chr(0x638),  # ARABIC MATHEMATICAL LOOPED ZAH, 𞺚
    chr(0x1EEBA): chr(0x638)  # ARABIC MATHEMATICAL DOUBLE-STRUCK ZAH, 𞺺
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x639, ARABIC LETTER AIN, ع
    ,
    chr(0x75D): chr(0x639),  # ARABIC LETTER AIN WITH TWO DOTS ABOVE, ݝ
    chr(0x75E): chr(
        0x639
    ),  # ARABIC LETTER AIN WITH THREE DOTS POINTING DOWNWARDS ABOVE, ݞ
    chr(0x75F): chr(0x639),  # ARABIC LETTER AIN WITH TWO DOTS VERTICALLY ABOVE, ݟ
    chr(0x8B3): chr(0x639),  # ARABIC LETTER AIN WITH THREE DOTS BELOW, ࢳ
    chr(0x10A92): chr(0x639),  # OLD NORTH ARABIAN LETTER AIN, 𐪒
    chr(0x1EE0F): chr(0x639),  # ARABIC MATHEMATICAL AIN, 𞸏
    chr(0x1EE2F): chr(0x639),  # ARABIC MATHEMATICAL INITIAL AIN, 𞸯
    chr(0x1EE4F): chr(0x639),  # ARABIC MATHEMATICAL TAILED AIN, 𞹏
    chr(0x1EE6F): chr(0x639),  # ARABIC MATHEMATICAL STRETCHED AIN, 𞹯
    chr(0x1EE8F): chr(0x639),  # ARABIC MATHEMATICAL LOOPED AIN, 𞺏
    chr(0x1EEAF): chr(0x639),  # ARABIC MATHEMATICAL DOUBLE-STRUCK AIN, 𞺯
    chr(0x60F): chr(0x639)  # ARABIC SIGN MISRA - ؏ -  ؏ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x63a, ARABIC LETTER GHAIN, غ
    ,
    chr(0x8C3): chr(0x63A),  # ARABIC LETTER GHAIN WITH THREE DOTS ABOVE, ࣃ
    chr(0x10A96): chr(0x63A),  # OLD NORTH ARABIAN LETTER GHAIN, 𐪖
    chr(0x1EE1B): chr(0x63A),  # ARABIC MATHEMATICAL GHAIN, 𞸛
    chr(0x1EE3B): chr(0x63A),  # ARABIC MATHEMATICAL INITIAL GHAIN, 𞸻
    chr(0x1EE5B): chr(0x63A),  # ARABIC MATHEMATICAL TAILED GHAIN, 𞹛
    chr(0x1EE7B): chr(0x63A),  # ARABIC MATHEMATICAL STRETCHED GHAIN, 𞹻
    chr(0x1EE9B): chr(0x63A),  # ARABIC MATHEMATICAL LOOPED GHAIN, 𞺛
    chr(0x1EEBB): chr(0x63A)  # ARABIC MATHEMATICAL DOUBLE-STRUCK GHAIN, 𞺻
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x641, ARABIC LETTER FEH, ف
    ,
    chr(0x760): chr(0x641),  # ARABIC LETTER FEH WITH TWO DOTS BELOW, ݠ
    chr(0x761): chr(
        0x641
    ),  # ARABIC LETTER FEH WITH THREE DOTS POINTING UPWARDS BELOW, ݡ
    chr(0x8A4): chr(0x641),  # ARABIC LETTER FEH WITH DOT BELOW AND THREE DOTS ABOVE, ࢤ
    chr(0x8BB): chr(0x641),  # ARABIC LETTER AFRICAN FEH, ࢻ
    chr(0x10A90): chr(0x641),  # OLD NORTH ARABIAN LETTER FEH, 𐪐
    chr(0x1EE10): chr(0x641),  # ARABIC MATHEMATICAL FEH, 𞸐
    chr(0x1EE1E): chr(0x641),  # ARABIC MATHEMATICAL DOTLESS FEH, 𞸞
    chr(0x1EE30): chr(0x641),  # ARABIC MATHEMATICAL INITIAL FEH, 𞸰
    chr(0x1EE70): chr(0x641),  # ARABIC MATHEMATICAL STRETCHED FEH, 𞹰
    chr(0x1EE7E): chr(0x641),  # ARABIC MATHEMATICAL STRETCHED DOTLESS FEH, 𞹾
    chr(0x1EE90): chr(0x641),  # ARABIC MATHEMATICAL LOOPED FEH, 𞺐
    chr(0x1EEB0): chr(0x641),  # ARABIC MATHEMATICAL DOUBLE-STRUCK FEH, 𞺰
    chr(0xFB6A): chr(0x641),  # ARABIC LETTER VEH ISOLATED FORM - ﭪ -  ڤ - 1
    chr(0xFB6B): chr(0x641),  # ARABIC LETTER VEH FINAL FORM - ﭫ -  ڤ - 1
    chr(0xFB6C): chr(0x641),  # ARABIC LETTER VEH INITIAL FORM - ﭬ -  ڤ - 1
    chr(0xFB6D): chr(0x641),  # ARABIC LETTER VEH MEDIAL FORM - ﭭ -  ڤ - 1
    chr(0xFB6E): chr(0x641),  # ARABIC LETTER PEHEH ISOLATED FORM - ﭮ -  ڦ - 1
    chr(0xFB6F): chr(0x641),  # ARABIC LETTER PEHEH FINAL FORM - ﭯ -  ڦ - 1
    chr(0xFB70): chr(0x641),  # ARABIC LETTER PEHEH INITIAL FORM - ﭰ -  ڦ - 1
    chr(0xFB71): chr(0x641)  # ARABIC LETTER PEHEH MEDIAL FORM - ﭱ -  ڦ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x642, ARABIC LETTER QAF, ق
    ,
    chr(0x66F): chr(0x642),  # ARABIC LETTER DOTLESS QAF, ٯ
    chr(0x8A5): chr(0x642),  # ARABIC LETTER QAF WITH DOT BELOW, ࢥ
    chr(0x8B5): chr(0x642),  # ARABIC LETTER QAF WITH DOT BELOW AND NO DOTS ABOVE, ࢵ
    chr(0x8BC): chr(0x642),  # ARABIC LETTER AFRICAN QAF, ࢼ
    chr(0x8C4): chr(0x642),  # ARABIC LETTER AFRICAN QAF WITH THREE DOTS ABOVE, ࣄ
    chr(0x10A84): chr(0x642),  # OLD NORTH ARABIAN LETTER QAF, 𐪄
    chr(0x1EE12): chr(0x642),  # ARABIC MATHEMATICAL QAF, 𞸒
    chr(0x1EE1F): chr(0x642),  # ARABIC MATHEMATICAL DOTLESS QAF, 𞸟
    chr(0x1EE32): chr(0x642),  # ARABIC MATHEMATICAL INITIAL QAF, 𞸲
    chr(0x1EE52): chr(0x642),  # ARABIC MATHEMATICAL TAILED QAF, 𞹒
    chr(0x1EE5F): chr(0x642),  # ARABIC MATHEMATICAL TAILED DOTLESS QAF, 𞹟
    chr(0x1EE72): chr(0x642),  # ARABIC MATHEMATICAL STRETCHED QAF, 𞹲
    chr(0x1EE92): chr(0x642),  # ARABIC MATHEMATICAL LOOPED QAF, 𞺒
    chr(0x1EEB2): chr(0x642)  # ARABIC MATHEMATICAL DOUBLE-STRUCK QAF, 𞺲
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x643, ARABIC LETTER KAF, ك
    ,
    chr(0x77F): chr(0x643),  # ARABIC LETTER KAF WITH TWO DOTS ABOVE, ݿ
    chr(0x8B4): chr(0x643),  # ARABIC LETTER KAF WITH DOT BELOW, ࢴ
    chr(0x10A8B): chr(0x643),  # OLD NORTH ARABIAN LETTER KAF, 𐪋
    chr(0x1EE0A): chr(0x643),  # ARABIC MATHEMATICAL KAF, 𞸊
    chr(0x1EE2A): chr(0x643),  # ARABIC MATHEMATICAL INITIAL KAF, 𞸪
    chr(0x1EE6A): chr(0x643),  # ARABIC MATHEMATICAL STRETCHED KAF, 𞹪
    chr(0xFB96): chr(0x643),  # ARABIC LETTER GUEH ISOLATED FORM - ﮖ -  ڳ - 1
    chr(0xFB97): chr(0x643),  # ARABIC LETTER GUEH FINAL FORM - ﮗ -  ڳ - 1
    chr(0xFB98): chr(0x643),  # ARABIC LETTER GUEH INITIAL FORM - ﮘ -  ڳ - 1
    chr(0xFB99): chr(0x643),  # ARABIC LETTER GUEH MEDIAL FORM - ﮙ -  ڳ - 1
    chr(0xFB9A): chr(0x643),  # ARABIC LETTER NGOEH ISOLATED FORM - ﮚ -  ڱ - 1
    chr(0xFB9B): chr(0x643),  # ARABIC LETTER NGOEH FINAL FORM - ﮛ -  ڱ - 1
    chr(0xFB9C): chr(0x643),  # ARABIC LETTER NGOEH INITIAL FORM - ﮜ -  ڱ - 1
    chr(0xFB9D): chr(0x643),  # ARABIC LETTER NGOEH MEDIAL FORM - ﮝ -  ڱ - 1
    chr(0x762): chr(0x643),  # ARABIC LETTER KEHEH WITH DOT ABOVE - ݢ -  ݢ - 1
    chr(0x763): chr(0x643),  # ARABIC LETTER KEHEH WITH THREE DOTS ABOVE - ݣ -  ݣ - 1
    chr(0x764): chr(
        0x643
    ),  # ARABIC LETTER KEHEH WITH THREE DOTS POINTING UPWARDS BELOW - ݤ -  ݤ - 1
    chr(0x88D): chr(
        0x643
    ),  # ARABIC LETTER KEHEH WITH TWO DOTS VERTICALLY BELOW - ࢍ -  ࢍ - 1
    chr(0x8C2): chr(0x643),  # ARABIC LETTER KEHEH WITH SMALL V - ࣂ -  ࣂ - 1
    chr(0x8C8): chr(0x643),  # ARABIC LETTER GRAF - ࣈ -  ࣈ - 1
    chr(0x8B0): chr(0x643),  # ARABIC LETTER GAF WITH INVERTED STROKE - ࢰ -  ࢰ - 1
    chr(0xFBD3): chr(0x643),  # ARABIC LETTER NG ISOLATED FORM - ﯓ -  ڭ - 1
    chr(0xFBD4): chr(0x643),  # ARABIC LETTER NG FINAL FORM - ﯔ -  ڭ - 1
    chr(0xFBD5): chr(0x643),  # ARABIC LETTER NG INITIAL FORM - ﯕ -  ڭ - 1
    chr(0xFBD6): chr(0x643)  # ARABIC LETTER NG MEDIAL FORM - ﯖ -  ڭ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x644, ARABIC LETTER LAM, ل
    ,
    chr(0x76A): chr(0x644),  # ARABIC LETTER LAM WITH BAR, ݪ
    chr(0x8A6): chr(0x644),  # ARABIC LETTER LAM WITH DOUBLE BAR, ࢦ
    chr(0x8C7): chr(0x644),  # ARABIC LETTER LAM WITH SMALL ARABIC LETTER TAH ABOVE, ࣇ
    chr(0x10A81): chr(0x644),  # OLD NORTH ARABIAN LETTER LAM, 𐪁
    chr(0x1EE0B): chr(0x644),  # ARABIC MATHEMATICAL LAM, 𞸋
    chr(0x1EE2B): chr(0x644),  # ARABIC MATHEMATICAL INITIAL LAM, 𞸫
    chr(0x1EE4B): chr(0x644),  # ARABIC MATHEMATICAL TAILED LAM, 𞹋
    chr(0x1EE8B): chr(0x644),  # ARABIC MATHEMATICAL LOOPED LAM, 𞺋
    chr(0x1EEAB): chr(0x644)  # ARABIC MATHEMATICAL DOUBLE-STRUCK LAM, 𞺫
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x645, ARABIC LETTER MEEM, م
    ,
    chr(0x765): chr(0x645),  # ARABIC LETTER MEEM WITH DOT ABOVE, ݥ
    chr(0x766): chr(0x645),  # ARABIC LETTER MEEM WITH DOT BELOW, ݦ
    chr(0x8A7): chr(0x645),  # ARABIC LETTER MEEM WITH THREE DOTS ABOVE, ࢧ
    chr(0x10A83): chr(0x645),  # OLD NORTH ARABIAN LETTER MEEM, 𐪃
    chr(0x1EE0C): chr(0x645),  # ARABIC MATHEMATICAL MEEM, 𞸌
    chr(0x1EE2C): chr(0x645),  # ARABIC MATHEMATICAL INITIAL MEEM, 𞸬
    chr(0x1EE6C): chr(0x645),  # ARABIC MATHEMATICAL STRETCHED MEEM, 𞹬
    chr(0x1EE8C): chr(0x645),  # ARABIC MATHEMATICAL LOOPED MEEM, 𞺌
    chr(0x1EEAC): chr(0x645)  # ARABIC MATHEMATICAL DOUBLE-STRUCK MEEM, 𞺬
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x646, ARABIC LETTER NOON, ن
    ,
    chr(0x6B9): chr(0x646),  # ARABIC LETTER NOON WITH DOT BELOW, ڹ
    chr(0x767): chr(0x646),  # ARABIC LETTER NOON WITH TWO DOTS BELOW, ݧ
    chr(0x768): chr(0x646),  # ARABIC LETTER NOON WITH SMALL TAH, ݨ
    chr(0x769): chr(0x646),  # ARABIC LETTER NOON WITH SMALL V, ݩ
    chr(0x889): chr(0x646),  # ARABIC LETTER NOON WITH INVERTED SMALL V, ࢉ
    chr(0x8BD): chr(0x646),  # ARABIC LETTER AFRICAN NOON, ࢽ
    chr(0xFB9E): chr(0x646),  # ARABIC LETTER NOON GHUNNA ISOLATED FORM, ﮞ
    chr(0xFB9F): chr(0x646),  # ARABIC LETTER NOON GHUNNA FINAL FORM, ﮟ
    chr(0x10A8C): chr(0x646),  # OLD NORTH ARABIAN LETTER NOON, 𐪌
    chr(0x1EE0D): chr(0x646),  # ARABIC MATHEMATICAL NOON, 𞸍
    chr(0x1EE1D): chr(0x646),  # ARABIC MATHEMATICAL DOTLESS NOON, 𞸝
    chr(0x1EE2D): chr(0x646),  # ARABIC MATHEMATICAL INITIAL NOON, 𞸭
    chr(0x1EE4D): chr(0x646),  # ARABIC MATHEMATICAL TAILED NOON, 𞹍
    chr(0x1EE5D): chr(0x646),  # ARABIC MATHEMATICAL TAILED DOTLESS NOON, 𞹝
    chr(0x1EE6D): chr(0x646),  # ARABIC MATHEMATICAL STRETCHED NOON, 𞹭
    chr(0x1EE8D): chr(0x646),  # ARABIC MATHEMATICAL LOOPED NOON, 𞺍
    chr(0x1EEAD): chr(0x646),  # ARABIC MATHEMATICAL DOUBLE-STRUCK NOON, 𞺭
    chr(0xFBA0): chr(0x646),  # ARABIC LETTER RNOON ISOLATED FORM - ﮠ -  ڻ - 1
    chr(0xFBA1): chr(0x646),  # ARABIC LETTER RNOON FINAL FORM - ﮡ -  ڻ - 1
    chr(0xFBA2): chr(0x646),  # ARABIC LETTER RNOON INITIAL FORM - ﮢ -  ڻ - 1
    chr(0xFBA3): chr(0x646)  # ARABIC LETTER RNOON MEDIAL FORM - ﮣ -  ڻ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x647, ARABIC LETTER HEH, ه
    ,
    chr(0xFBA4): chr(0x647),  # ARABIC LETTER HEH WITH YEH ABOVE ISOLATED FORM, ﮤ
    chr(0xFBA5): chr(0x647),  # ARABIC LETTER HEH WITH YEH ABOVE FINAL FORM, ﮥ
    chr(0xFBA6): chr(0x647),  # ARABIC LETTER HEH GOAL ISOLATED FORM, ﮦ
    chr(0xFBA7): chr(0x647),  # ARABIC LETTER HEH GOAL FINAL FORM, ﮧ
    chr(0xFBA8): chr(0x647),  # ARABIC LETTER HEH GOAL INITIAL FORM, ﮨ
    chr(0xFBA9): chr(0x647),  # ARABIC LETTER HEH GOAL MEDIAL FORM, ﮩ
    chr(0xFBAA): chr(0x647),  # ARABIC LETTER HEH DOACHASHMEE ISOLATED FORM, ﮪ
    chr(0xFBAB): chr(0x647),  # ARABIC LETTER HEH DOACHASHMEE FINAL FORM, ﮫ
    chr(0xFBAC): chr(0x647),  # ARABIC LETTER HEH DOACHASHMEE INITIAL FORM, ﮬ
    chr(0xFBAD): chr(0x647),  # ARABIC LETTER HEH DOACHASHMEE MEDIAL FORM, ﮭ
    chr(0x10A80): chr(0x647),  # OLD NORTH ARABIAN LETTER HEH, 𐪀
    chr(0x1EE24): chr(0x647),  # ARABIC MATHEMATICAL INITIAL HEH, 𞸤
    chr(0x1EE64): chr(0x647),  # ARABIC MATHEMATICAL STRETCHED HEH, 𞹤
    chr(0x1EE84): chr(0x647)  # ARABIC MATHEMATICAL LOOPED HEH, 𞺄
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x648, ARABIC LETTER WAW, و
    ,
    # chr(0x624): chr(0x648),  # ARABIC LETTER WAW WITH HAMZA ABOVE, ؤ
    chr(0x778): chr(
        0x648
    ),  # ARABIC LETTER WAW WITH EXTENDED ARABIC-INDIC DIGIT TWO ABOVE, ݸ
    chr(0x779): chr(
        0x648
    ),  # ARABIC LETTER WAW WITH EXTENDED ARABIC-INDIC DIGIT THREE ABOVE, ݹ
    chr(0x8AB): chr(0x648),  # ARABIC LETTER WAW WITH DOT WITHIN, ࢫ
    chr(0x8B1): chr(0x648),  # ARABIC LETTER STRAIGHT WAW, ࢱ
    chr(0xFEEE): chr(0x648),  # ARABIC LETTER WAW FINAL FORM, ﻮ
    chr(0x10A65): chr(0x648),  # OLD SOUTH ARABIAN LETTER WAW, 𐩥
    chr(0x10A85): chr(0x648),  # OLD NORTH ARABIAN LETTER WAW, 𐪅
    chr(0x1EE05): chr(0x648),  # ARABIC MATHEMATICAL WAW, 𞸅
    chr(0x1EE85): chr(0x648),  # ARABIC MATHEMATICAL LOOPED WAW, 𞺅
    chr(0x1EEA5): chr(0x648),  # ARABIC MATHEMATICAL DOUBLE-STRUCK WAW, 𞺥
    chr(0xFBD7): chr(0x648),  # ARABIC LETTER U ISOLATED FORM - ﯗ -  ۇ - 1
    chr(0xFBD8): chr(0x648),  # ARABIC LETTER U FINAL FORM - ﯘ -  ۇ - 1
    chr(0xFBD9): chr(0x648),  # ARABIC LETTER OE ISOLATED FORM - ﯙ -  ۆ - 1
    chr(0xFBDA): chr(0x648),  # ARABIC LETTER OE FINAL FORM - ﯚ -  ۆ - 1
    chr(0xFBDB): chr(0x648),  # ARABIC LETTER YU ISOLATED FORM - ﯛ -  ۈ - 1
    chr(0xFBDC): chr(0x648),  # ARABIC LETTER YU FINAL FORM - ﯜ -  ۈ - 1
    chr(0xFBDE): chr(0x648),  # ARABIC LETTER VE ISOLATED FORM - ﯞ -  ۋ - 1
    chr(0xFBDF): chr(0x648),  # ARABIC LETTER VE FINAL FORM - ﯟ -  ۋ - 1
    chr(0xFBE0): chr(0x648),  # ARABIC LETTER KIRGHIZ OE ISOLATED FORM - ﯠ -  ۅ - 1
    chr(0xFBE1): chr(0x648),  # ARABIC LETTER KIRGHIZ OE FINAL FORM - ﯡ -  ۅ - 1
    chr(0xFBE2): chr(0x648),  # ARABIC LETTER KIRGHIZ YU ISOLATED FORM - ﯢ -  ۉ - 1
    chr(0xFBE3): chr(0x648)  # ARABIC LETTER KIRGHIZ YU FINAL FORM - ﯣ -  ۉ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x649, ARABIC LETTER ALEF MAKSURA, ى
    ,
    chr(0xFBE8): chr(
        0x649
    ),  # ARABIC LETTER UIGHUR KAZAKH KIRGHIZ ALEF MAKSURA INITIAL FORM, ﯨ
    chr(0xFBE9): chr(
        0x649
    )  # ARABIC LETTER UIGHUR KAZAKH KIRGHIZ ALEF MAKSURA MEDIAL FORM, ﯩ
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x64a, ARABIC LETTER YEH, ي
    ,
    chr(0x620): chr(0x64A),  # ARABIC LETTER KASHMIRI YEH, ؠ
    chr(0x775): chr(
        0x64A
    ),  # ARABIC LETTER FARSI YEH WITH EXTENDED ARABIC-INDIC DIGIT TWO ABOVE, ݵ
    chr(0x776): chr(
        0x64A
    ),  # ARABIC LETTER FARSI YEH WITH EXTENDED ARABIC-INDIC DIGIT THREE ABOVE, ݶ
    chr(0x777): chr(
        0x64A
    ),  # ARABIC LETTER FARSI YEH WITH EXTENDED ARABIC-INDIC DIGIT FOUR BELOW, ݷ
    chr(0x77A): chr(
        0x64A
    ),  # ARABIC LETTER YEH BARREE WITH EXTENDED ARABIC-INDIC DIGIT TWO ABOVE, ݺ
    chr(0x77B): chr(
        0x64A
    ),  # ARABIC LETTER YEH BARREE WITH EXTENDED ARABIC-INDIC DIGIT THREE ABOVE, ݻ
    chr(0x886): chr(0x64A),  # ARABIC LETTER THIN YEH, ࢆ
    chr(0x8A8): chr(0x64A),  # ARABIC LETTER YEH WITH TWO DOTS BELOW AND HAMZA ABOVE, ࢨ
    chr(0x8A9): chr(0x64A),  # ARABIC LETTER YEH WITH TWO DOTS BELOW AND DOT ABOVE, ࢩ
    chr(0x8AC): chr(0x64A),  # ARABIC LETTER ROHINGYA YEH, ࢬ
    chr(0x8BA): chr(
        0x64A
    ),  # ARABIC LETTER YEH WITH TWO DOTS BELOW AND SMALL NOON ABOVE, ࢺ
    chr(0x8C9): chr(0x64A),  # ARABIC SMALL FARSI YEH, ࣉ
    chr(0xFBAE): chr(0x64A),  # ARABIC LETTER YEH BARREE ISOLATED FORM, ﮮ
    chr(0xFBAF): chr(0x64A),  # ARABIC LETTER YEH BARREE FINAL FORM, ﮯ
    chr(0x10A9A): chr(0x64A),  # OLD NORTH ARABIAN LETTER YEH, 𐪚
    chr(0x1EE09): chr(0x64A),  # ARABIC MATHEMATICAL YEH, 𞸉
    chr(0x1EE29): chr(0x64A),  # ARABIC MATHEMATICAL INITIAL YEH, 𞸩
    chr(0x1EE49): chr(0x64A),  # ARABIC MATHEMATICAL TAILED YEH, 𞹉
    chr(0x1EE69): chr(0x64A),  # ARABIC MATHEMATICAL STRETCHED YEH, 𞹩
    chr(0x1EE89): chr(0x64A),  # ARABIC MATHEMATICAL LOOPED YEH, 𞺉
    chr(0x1EEA9): chr(0x64A),  # ARABIC MATHEMATICAL DOUBLE-STRUCK YEH, 𞺩
    chr(0xFBE4): chr(0x64A),  # ARABIC LETTER E ISOLATED FORM - ﯤ -  ې - 1
    chr(0xFBE5): chr(0x64A),  # ARABIC LETTER E FINAL FORM - ﯥ -  ې - 1
    chr(0xFBE6): chr(0x64A),  # ARABIC LETTER E INITIAL FORM - ﯦ -  ې - 1
    chr(0xFBE7): chr(0x64A)  # ARABIC LETTER E MEDIAL FORM - ﯧ -  ې - 1
    ##
    ,
    chr(
        0xFBB0
    ): "ئ",  # ARABIC LETTER YEH BARREE WITH HAMZA ABOVE ISOLATED FORM - ﮰ -  ۓ - 1
    chr(
        0xFBB1
    ): "ئ"  # ARABIC LETTER YEH BARREE WITH HAMZA ABOVE FINAL FORM - ﮱ -  ۓ - 1
    # --------------------------------------------------------------------------------
    # The following should be mapped to 0x621, ARABIC LETTER HAMZA, ء
    # --------------------------------------------------------------------------------
    # Extended Digits
    ,
    chr(0x6F0): chr(0x660),  # EXTENDED ARABIC-INDIC DIGIT ZERO - ۰ -  ۰ - 1
    chr(0x6F1): chr(0x661),  # EXTENDED ARABIC-INDIC DIGIT ONE - ۱ -  ۱ - 1
    chr(0x6F2): chr(0x662),  # EXTENDED ARABIC-INDIC DIGIT TWO - ۲ -  ۲ - 1
    chr(0x6F3): chr(0x663),  # EXTENDED ARABIC-INDIC DIGIT THREE - ۳ -  ۳ - 1
    chr(0x6F4): chr(0x664),  # EXTENDED ARABIC-INDIC DIGIT FOUR - ۴ -  ۴ - 1
    chr(0x6F5): chr(0x665),  # EXTENDED ARABIC-INDIC DIGIT FIVE - ۵ -  ۵ - 1
    chr(0x6F6): chr(0x666),  # EXTENDED ARABIC-INDIC DIGIT SIX - ۶ -  ۶ - 1
    chr(0x6F7): chr(0x667),  # EXTENDED ARABIC-INDIC DIGIT SEVEN - ۷ -  ۷ - 1
    chr(0x6F8): chr(0x668),  # EXTENDED ARABIC-INDIC DIGIT EIGHT - ۸ -  ۸ - 1
    chr(0x6F9): chr(0x669),  # EXTENDED ARABIC-INDIC DIGIT NINE - ۹ -  ۹ - 1
    chr(0x609): "٪",  # ARABIC-INDIC PER MILLE SIGN - ؉ -  ؉ - 1
    chr(0x60A): "٪",  # ARABIC-INDIC PER TEN THOUSAND SIGN - ؊ -  ؊ - 1
    chr(0x60D): "-",  # ARABIC DATE SEPARATOR - ؍ -  ؍ - 1
}

# with the lep of this link: https://github.com/AmyrAhmady/FarsiType/blob/master/FarsiType.cpp
SIMILAR_CHARS_MAP = {
    "\u0674": "\u0654",  # faa_HAMZA_ABOVE, # ء
    "\u065F": "\u0655",  # faa_HAMZA_BELOW, # ء
    "\ufe80": "\u0621",  # faa_HAMZA, # ء
    "\u06FD": "\u0621",  # faa_HAMZA, # ء
    "\ufe81": "\u0622",  # faa_ALEF_MAD_ABOVE, # آ
    "\ufe82": "\u0622",  # faa_ALEF_MAD_ABOVE, # آ
    "\u0675": "\u0623",  # faa_ALEF_HAMZEH_ABOVE, # أ
    "\ufe83": "\u0623",  # faa_ALEF_HAMZEH_ABOVE, # أ
    "\ufe84": "\u0623",  # faa_ALEF_HAMZEH_ABOVE, # أ
    "\u0671": "\u0623",  # faa_ALEF_HAMZEH_ABOVE, # أ
    "\u0672": "\u0623",  # faa_ALEF_HAMZEH_ABOVE, # أ
    "\ufe85": "\u0624",  # faa_VAAV_HAMZEH_ABOVE, # ؤ
    "\ufe86": "\u0624",  # faa_VAAV_HAMZEH_ABOVE, # ؤ
    "\u0676": "\u0624",  # faa_VAAV_HAMZEH_ABOVE, # ؤ
    "\u0677": "\u0624",  # faa_VAAV_HAMZEH_ABOVE, # ؤ
    "\ufe87": "\u0625",  # faa_ALEF_HAMZEH_BELOW, # إ
    "\ufe88": "\u0625",  # faa_ALEF_HAMZEH_BELOW, # إ
    "\u0673": "\u0625",  # faa_ALEF_HAMZEH_BELOW, # إ
    "\ufe89": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\ufe8b": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\ufe8c": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\ufe8a": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\u0678": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\u06D3": "\u0626",  # faa_YEH_HAMZEH_ABOVE, # ئ
    "\ufe8d": "\u0627",  # faa_ALEF, # ا
    "\ufe8e": "\u0627",  # faa_ALEF, # ا
    "\ufe8f": "\u0628",  # faa_BEH, # ب
    "\ufe91": "\u0628",  # faa_BEH, # ب
    "\ufe92": "\u0628",  # faa_BEH, # ب
    "\ufe90": "\u0628",  # faa_BEH, # ب
    "\ufb56": "\u0628",  # faa_BEH, # ب
    "\ufb58": "\u0628",  # faa_BEH, # ب
    "\ufb59": "\u0628",  # faa_BEH, # ب
    "\ufb57": "\u0628",  # faa_BEH, # ب
    "\u067B": "\u0628",  # faa_BEH, # ب
    "\u067E": "\u0628",  # faa_BEH, # ب
    "\ufe93": "\u0629",  # faa_TEH_TANIS, # ة
    "\ufe94": "\u0629",  # faa_TEH_TANIS, # ة
    "\u06C3": "\u0629",  # faa_TEH_TANIS, # ة
    "\ufe95": "\u062A",  # faa_TEH, # ت
    "\ufe97": "\u062A",  # faa_TEH, # ت
    "\ufe98": "\u062A",  # faa_TEH, # ت
    "\ufe96": "\u062A",  # faa_TEH, # ت
    "\u0679": "\u062A",  # faa_TEH, # ت
    "\u067A": "\u062A",  # faa_TEH, # ت
    "\u067C": "\u062A",  # faa_TEH, # ت
    "\ufe99": "\u062b",  # faa_SEH, # ث
    "\ufe9b": "\u062b",  # faa_SEH, # ث
    "\ufe9c": "\u062b",  # faa_SEH, # ث
    "\ufe9a": "\u062b",  # faa_SEH, # ث
    "\u067D": "\u062b",  # faa_SEH, # ث
    "\u067F": "\u062b",  # faa_SEH, # ث
    "\ufe9d": "\u062c",  # faa_JEEM, # ج
    "\ufe9f": "\u062c",  # faa_JEEM, # ج
    "\ufea0": "\u062c",  # faa_JEEM, # ج
    "\ufe9e": "\u062c",  # faa_JEEM, # ج
    "\ufb7a": "\u062c",  # faa_JEEM, # ج
    "\u0686": "\u062c",  # faa_JEEM, # ج
    "\ufb7c": "\u062c",  # faa_JEEM, # ج
    "\ufb7d": "\u062c",  # faa_JEEM, # ج
    "\ufb7b": "\u062c",  # faa_JEEM, # ج
    "\u0681": "\u062c",  # faa_JEEM, # ج
    "\u0683": "\u062c",  # faa_JEEM, # ج
    "\u0684": "\u062c",  # faa_JEEM, # ج
    "\u0687": "\u062c",  # faa_JEEM, # ج
    "\u06BF": "\u062c",  # faa_JEEM, # ج
    "\ufea1": "\u062d",  # faa_HEH_JEEMY, # ح
    "\ufea3": "\u062d",  # faa_HEH_JEEMY, # ح
    "\ufea4": "\u062d",  # faa_HEH_JEEMY, # ح
    "\ufea2": "\u062d",  # faa_HEH_JEEMY, # ح
    "\ufea5": "\u062e",  # faa_KHEH, # خ
    "\ufea7": "\u062e",  # faa_KHEH, # خ
    "\ufea8": "\u062e",  # faa_KHEH, # خ
    "\ufea6": "\u062e",  # faa_KHEH, # خ
    "\u0682": "\u062e",  # faa_KHEH, # خ
    "\u0685": "\u062e",  # faa_KHEH, # خ
    "\ufea9": "\u062f",  # faa_DAAL, # د
    "\ufeaa": "\u062f",  # faa_DAAL, # د
    "\u0688": "\u062f",  # faa_DAAL, # د
    "\u0689": "\u062f",  # faa_DAAL, # د
    "\u068A": "\u062f",  # faa_DAAL, # د
    "\u068B": "\u062f",  # faa_DAAL, # د
    "\u068C": "\u062f",  # faa_DAAL, # د
    "\u068D": "\u062f",  # faa_DAAL, # د
    "\u068F": "\u062f",  # faa_DAAL, # د
    "\u06EE": "\u062f",  # faa_DAAL, # د
    "\ufeab": "\u0630",  # faa_ZAAL, # ذ
    "\ufeac": "\u0630",  # faa_ZAAL, # ذ
    "\u068E": "\u0630",  # faa_ZAAL, # ذ
    "\ufead": "\u0631",  # faa_REH, # ر
    "\ufeae": "\u0631",  # faa_REH, # ر
    "\u0692": "\u0631",  # faa_REH, # ر
    "\u0694": "\u0631",  # faa_REH, # ر
    "\u0695": "\u0631",  # faa_REH, # ر
    "\u06EF": "\u0631",  # faa_REH, # ر
    "\ufeaf": "\u0632",  # faa_ZEH, # ز
    "\ufeb0": "\u0632",  # faa_ZEH, # ز
    "\ufb8a": "\u0632",  # faa_ZEH, # ز
    "\u0698": "\u0632",  # faa_ZEH, # ز
    "\ufb8b": "\u0632",  # faa_ZEH, # ز
    "\u0697": "\u0632",  # faa_ZEH, # ز
    "\ufeb1": "\u0633",  # faa_SEEN, # س
    "\ufeb3": "\u0633",  # faa_SEEN, # س
    "\ufeb4": "\u0633",  # faa_SEEN, # س
    "\ufeb2": "\u0633",  # faa_SEEN, # س
    "\u069A": "\u0633",  # faa_SEEN, # س
    "\u069B": "\u0633",  # faa_SEEN, # س
    "\ufeb5": "\u0634",  # faa_SHEEN, # ش
    "\ufeb7": "\u0634",  # faa_SHEEN, # ش
    "\ufeb8": "\u0634",  # faa_SHEEN, # ش
    "\ufeb6": "\u0634",  # faa_SHEEN, # ش
    "\u069C": "\u0634",  # faa_SHEEN, # ش
    "\u06FA": "\u0634",  # faa_SHEEN, # ش
    "\ufeb9": "\u0635",  # faa_SAAD, # ص
    "\ufebb": "\u0635",  # faa_SAAD, # ص
    "\ufebc": "\u0635",  # faa_SAAD, # ص
    "\ufeba": "\u0635",  # faa_SAAD, # ص
    "\u069D": "\u0635",  # faa_SAAD, # ص
    "\ufebd": "\u0636",  # faa_ZAAD, # ض
    "\ufebf": "\u0636",  # faa_ZAAD, # ض
    "\ufec0": "\u0636",  # faa_ZAAD, # ض
    "\ufebe": "\u0636",  # faa_ZAAD, # ض
    "\u069E": "\u0636",  # faa_ZAAD, # ض
    "\u06FB": "\u0636",  # faa_ZAAD, # ض
    "\ufec1": "\u0637",  # faa_TAAH, # ط
    "\ufec3": "\u0637",  # faa_TAAH, # ط
    "\ufec4": "\u0637",  # faa_TAAH, # ط
    "\ufec2": "\u0637",  # faa_TAAH, # ط
    "\ufec5": "\u0638",  # faa_ZAAH, # ظ
    "\ufec7": "\u0638",  # faa_ZAAH, # ظ
    "\ufec8": "\u0638",  # faa_ZAAH, # ظ
    "\ufec6": "\u0638",  # faa_ZAAH, # ظ
    "\u069F": "\u0638",  # faa_ZAAH, # ظ
    "\ufec9": "\u0639",  # faa_AIN, # ع
    "\ufecb": "\u0639",  # faa_AIN, # ع
    "\ufecc": "\u0639",  # faa_AIN, # ع
    "\ufeca": "\u0639",  # faa_AIN, # ع
    "\ufecd": "\u063a",  # faa_GHAIN, # غ
    "\ufecf": "\u063a",  # faa_GHAIN, # غ
    "\ufed0": "\u063a",  # faa_GHAIN, # غ
    "\ufece": "\u063a",  # faa_GHAIN, # غ
    "\u06A0": "\u063a",  # faa_GHAIN, # غ
    "\u06FC": "\u063a",  # faa_GHAIN, # غ
    "\ufed1": "\u0641",  # faa_FEH, # ف
    "\ufed3": "\u0641",  # faa_FEH, # ف
    "\ufed4": "\u0641",  # faa_FEH, # ف
    "\ufed2": "\u0641",  # faa_FEH, # ف
    "\u06A1": "\u0641",  # faa_FEH, # ف
    "\u06A2": "\u0641",  # faa_FEH, # ف
    "\u06A3": "\u0641",  # faa_FEH, # ف
    "\u06A4": "\u0641",  # faa_FEH, # ف
    "\u06A5": "\u0641",  # faa_FEH, # ف
    "\u06A6": "\u0641",  # faa_FEH, # ف
    "\ufed5": "\u0642",  # faa_QAAF, # ق
    "\ufed7": "\u0642",  # faa_QAAF, # ق
    "\ufed8": "\u0642",  # faa_QAAF, # ق
    "\ufed6": "\u0642",  # faa_QAAF, # ق
    "\u06A7": "\u0642",  # faa_QAAF, # ق
    "\u06A8": "\u0642",  # faa_QAAF, # ق
    "\ufed9": "\u0643",  # faa_KAAF, # ك
    "\ufb8e": "\u0643",  # faa_KAAF, # ك
    "\ufb90": "\u0643",  # faa_KAAF, # ك
    "\ufb91": "\u0643",  # faa_KAAF, # ك
    "\ufb8f": "\u0643",  # faa_KAAF, # ك
    "\ufedb": "\u0643",  # faa_KAAF, # ك
    "\ufedc": "\u0643",  # faa_KAAF, # ك
    "\ufeda": "\u0643",  # faa_KAAF, # ك
    "\ufb92": "\u0643",  # faa_KAAF, # ك
    "\ufb94": "\u0643",  # faa_KAAF, # ك
    "\ufb95": "\u0643",  # faa_KAAF, # ك
    "\ufb93": "\u0643",  # faa_KAAF, # ك
    "\u063B": "\u0643",  # faa_KAAF, # ك
    "\u063C": "\u0643",  # faa_KAAF, # ك
    "\u06A9": "\u0643",  # faa_KAAF, # ك
    "\u06AA": "\u0643",  # faa_KAAF, # ك
    "\u06AB": "\u0643",  # faa_KAAF, # ك
    "\u06AC": "\u0643",  # faa_KAAF, # ك
    "\u06AD": "\u0643",  # faa_KAAF, # ك
    "\u06AE": "\u0643",  # faa_KAAF, # ك
    "\u06AF": "\u0643",  # faa_KAAF, # ك
    "\u06B0": "\u0643",  # faa_KAAF, # ك
    "\u06B1": "\u0643",  # faa_KAAF, # ك
    "\u06B2": "\u0643",  # faa_KAAF, # ك
    "\u06B3": "\u0643",  # faa_KAAF, # ك
    "\u06B4": "\u0643",  # faa_KAAF, # ك
    "\ufedd": "\u0644",  # faa_LAAM, # ل
    "\ufedf": "\u0644",  # faa_LAAM, # ل
    "\ufee0": "\u0644",  # faa_LAAM, # ل
    "\ufede": "\u0644",  # faa_LAAM, # ل
    "\u06B5": "\u0644",  # faa_LAAM, # ل
    "\u06B6": "\u0644",  # faa_LAAM, # ل
    "\u06B7": "\u0644",  # faa_LAAM, # ل
    "\u06B8": "\u0644",  # faa_LAAM, # ل
    "\ufee1": "\u0645",  # faa_MEEM, # م
    "\ufee3": "\u0645",  # faa_MEEM, # م
    "\ufee4": "\u0645",  # faa_MEEM, # م
    "\ufee2": "\u0645",  # faa_MEEM, # م
    "\u06FE": "\u0645",  # faa_MEEM, # م
    "\ufee5": "\u0646",  # faa_NOON, # ن
    "\ufee7": "\u0646",  # faa_NOON, # ن
    "\ufee8": "\u0646",  # faa_NOON, # ن
    "\ufee6": "\u0646",  # faa_NOON, # ن
    "\u06BA": "\u0646",  # faa_NOON, # ن
    "\u06BB": "\u0646",  # faa_NOON, # ن
    "\u06BC": "\u0646",  # faa_NOON, # ن
    "\u06BD": "\u0646",  # faa_NOON, # ن
    "\ufee9": "\u0647",  # faa_HEH, # ه
    "\ufeeb": "\u0647",  # faa_HEH, # ه
    "\ufeec": "\u0647",  # faa_HEH, # ه
    "\ufeea": "\u0647",  # faa_HEH, # ه
    "\u06BE": "\u0647",  # faa_HEH, # ه
    "\u06C0": "\u0647",  # faa_HEH, # ه
    "\u06C1": "\u0647",  # faa_HEH, # ه
    "\u06C2": "\u0647",  # faa_HEH, # ه
    "\u06D5": "\u0647",  # faa_HEH, # ه
    "\u06FF": "\u0647",  # faa_HEH, # ه
    "\ufeed": "\u0648",  # faa_VAAV, # و
    "\u06C4": "\u0648",  # faa_VAAV, # و
    "\u06C5": "\u0648",  # faa_VAAV, # و
    "\u06C6": "\u0648",  # faa_VAAV, # و
    "\u06C7": "\u0648",  # faa_VAAV, # و
    "\u06C8": "\u0648",  # faa_VAAV, # و
    "\u06C9": "\u0648",  # faa_VAAV, # و
    "\u06CA": "\u0648",  # faa_VAAV, # و
    "\u06CB": "\u0648",  # faa_VAAV, # و
    "\u06CF": "\u0648",  # faa_VAAV, # و
    "\ufbfc": "\u0649",  # faa_YEH, # ی
    "\ufbfe": "\u0649",  # faa_YEH, # ی
    "\ufbff": "\u0649",  # faa_YEH, # ی
    "\ufbfd": "\u0649",  # faa_YEH, # ی
    "\ufeef": "\u0649",  # faa_YEH, # ی
    "\ufef0": "\u0649",  # faa_YEH, # ی
    "\u06CC": "\u064a",  # faa_YEH, # ی
    "\u06CD": "\u0649",  # faa_YEH, # ی
    "\u06CE": "\u0649",  # faa_YEH, # ی
    "\ufef1": "\u064a",  # faa_ARABIC_YEH, # ي
    "\ufef3": "\u064a",  # faa_ARABIC_YEH, # ي
    "\ufef4": "\u064a",  # faa_ARABIC_YEH, # ي
    "\ufef2": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u063D": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u063E": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u063F": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u06D0": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u06D1": "\u064a",  # faa_ARABIC_YEH, # ي
    "\u06D2": "\u064a",  # faa_ARABIC_YEH, # ي
    "\ufefb": "\u0644\u0627",  # faa_LAAM_ALEF, # لا
    "\ufefc": "\u0644\u0627",  # faa_LAAM_ALEF, # لا
    "\ufef5": "\u0644\u0622",  # faa_LAAM_ALEF_MAD_ABOVE, # لآ
    "\ufef6": "\u0644\u0622",  # faa_LAAM_ALEF_MAD_ABOVE, # لآ
    "\ufef7": "\u0644\u0623",  # faa_LAAM_ALEF_HAMZA_ABOVE, # لأ
    "\ufef8": "\u0644\u0623",  # faa_LAAM_ALEF_HAMZA_ABOVE, # لأ
    "\ufef9": "\u0644\u0625",  # faa_LAAM_ALEF_HAMZEH_BELOW, # لإ
    "\ufefa": "\u0644\u0625",  # faa_LAAM_ALEF_HAMZEH_BELOW, # لإ
}

# temp_new = SIMILAR_CHARS_MAP_EXHAUSTIVE.copy()
# temp_old = SIMILAR_CHARS_MAP.copy()

# # [Test] new mapping does not map an element that exists in the old mapping
# assert set(SIMILAR_CHARS_MAP_EXHAUSTIVE.keys()).intersection(set(SIMILAR_CHARS_MAP.keys())) == set(), 'There are duplicate mappings'

# SIMILAR_CHARS_MAP overrides SIMILAR_CHARS_MAP_EXHAUSTIVE
SIMILAR_CHARS_MAP_EXHAUSTIVE.update(SIMILAR_CHARS_MAP)
SIMILAR_CHARS_MAP = SIMILAR_CHARS_MAP_EXHAUSTIVE

# # [Test] old mappings are perserved
# for key in temp_old:
#     assert temp_old[key] == SIMILAR_CHARS_MAP[key]

# temp_new = None
# temp_old = None
# SIMILAR_CHARS_MAP_EXHAUSTIVE = None


FATHA = "\u064e"
DAMMA = "\u064f"
KASRA = "\u0650"
SHADDA = "\u0651"
SUKUN = "\u0652"
TANWEEN_FATH = "\u064b"
TANWEEN_DAMM = "\u064c"
TANWEEN_KASR = "\u064d"

DIACRITICS = {
    FATHA,
    DAMMA,
    KASRA,
    SHADDA,
    SUKUN,
    TANWEEN_FATH,
    TANWEEN_DAMM,
    TANWEEN_KASR,
    "`",
}
HAMZA_MAP = {"آ": "آ", "إ": "إ", "أ": "أ", "ئ": "ئ", "ؤ": "ؤ"}


CHARS_TO_BE_REMOVED_at_last_step = [
    chr(0x6D8),  # ARABIC SMALL HIGH MEEM INITIAL FORM - ۘ -  ۘ - 1
    chr(0x6D9),  # ARABIC SMALL HIGH LAM ALEF - ۙ -  ۙ - 1
    chr(0x6DA),  # ARABIC SMALL HIGH JEEM - ۚ -  ۚ - 1
    chr(0x6DB),  # ARABIC SMALL HIGH THREE DOTS - ۛ -  ۛ - 1
    chr(0x6DC),  # ARABIC SMALL HIGH SEEN - ۜ -  ۜ - 1
    chr(0x8D3),  # ARABIC SMALL LOW WAW - ࣓ -  ࣓ - 1
    chr(0x8D4),  # ARABIC SMALL HIGH WORD AR-RUB - ࣔ -  ࣔ - 1
    chr(0x8D5),  # ARABIC SMALL HIGH SAD - ࣕ -  ࣕ - 1
    chr(0x8D6),  # ARABIC SMALL HIGH AIN - ࣖ -  ࣖ - 1
    chr(0x8D7),  # ARABIC SMALL HIGH QAF - ࣗ -  ࣗ - 1
    chr(0x8DA),  # ARABIC SMALL HIGH WORD ATH-THALATHA - ࣚ -  ࣚ - 1
    chr(0x8DB),  # ARABIC SMALL HIGH WORD AS-SAJDA - ࣛ -  ࣛ - 1
    chr(0x8DC),  # ARABIC SMALL HIGH WORD AN-NISF - ࣜ -  ࣜ - 1
    chr(0x8DD),  # ARABIC SMALL HIGH WORD SAKTA - ࣝ -  ࣝ - 1
    chr(0x8DE),  # ARABIC SMALL HIGH WORD QIF - ࣞ -  ࣞ - 1
    chr(0x8DF),  # ARABIC SMALL HIGH WORD WAQFA - ࣟ -  ࣟ - 1
    chr(0x8E0),  # ARABIC SMALL HIGH FOOTNOTE MARKER - ࣠ -  ࣠ - 1
    chr(0x8E1),  # ARABIC SMALL HIGH SIGN SAFHA - ࣡ -  ࣡ - 1
    chr(0x6DF),  # ARABIC SMALL HIGH ROUNDED ZERO - ۟ -  ۟ - 1
    chr(0x8F3),  # ARABIC SMALL HIGH WAW - ࣳ -  ࣳ - 1
    chr(0x6E0),  # ARABIC SMALL HIGH UPRIGHT RECTANGULAR ZERO - ۠ -  ۠ - 1
    chr(0x6E1),  # ARABIC SMALL HIGH DOTLESS HEAD OF KHAH - ۡ -  ۡ - 1
    chr(0x6E2),  # ARABIC SMALL HIGH MEEM ISOLATED FORM - ۢ -  ۢ - 1
    chr(0x6E3),  # ARABIC SMALL LOW SEEN - ۣ -  ۣ - 1
    chr(0x6E4),  # ARABIC SMALL HIGH MADDA - ۤ -  ۤ - 1
    chr(0x6E5),  # ARABIC SMALL WAW - ۥ -  ۥ - 1
    chr(0x6E6),  # ARABIC SMALL YEH - ۦ -  ۦ - 1
    chr(0x6E7),  # ARABIC SMALL HIGH YEH - ۧ -  ۧ - 1
    chr(0x6E8),  # ARABIC SMALL HIGH NOON - ۨ -  ۨ - 1
    chr(0x615),  # ARABIC SMALL HIGH TAH - ؕ -  ؕ - 1
    chr(0x617),  # ARABIC SMALL HIGH ZAIN - ؗ -  ؗ - 1
    chr(0x8D8),  # ARABIC SMALL HIGH NOON WITH KASRA - ࣘ -  ࣘ - 1
    chr(0x8D9),  # ARABIC SMALL LOW NOON WITH KASRA - ࣙ -  ࣙ - 1
    chr(0x898),  # ARABIC SMALL HIGH WORD AL-JUZ - ࢘ -  ࢘ - 1
    chr(0x6ED),  # ARABIC SMALL LOW MEEM - ۭ -  ۭ - 1
    chr(0x899),  # ARABIC SMALL LOW WORD ISHMAAM - ࢙ -  ࢙ - 1
    chr(0x89A),  # ARABIC SMALL LOW WORD IMAALA - ࢚ -  ࢚ - 1
    chr(0x89B),  # ARABIC SMALL LOW WORD TASHEEL - ࢛ -  ࢛ - 1
    chr(0x8CA),  # ARABIC SMALL HIGH FARSI YEH - ࣊ -  ࣊ - 1
    chr(0x8CB),  # ARABIC SMALL HIGH YEH BARREE WITH TWO DOTS BELOW - ࣋ -  ࣋ - 1
    chr(0x8CC),  # ARABIC SMALL HIGH WORD SAH - ࣌ -  ࣌ - 1
    chr(0x8CD),  # ARABIC SMALL HIGH ZAH - ࣍ -  ࣍ - 1
    chr(0x8E3),  # ARABIC TURNED DAMMA BELOW - ࣣ -  ࣣ - 1
    chr(0xFBB2),  # ARABIC SYMBOL DOT ABOVE - ﮲ -  ﮲ - 1
    chr(0xFBB3),  # ARABIC SYMBOL DOT BELOW - ﮳ -  ﮳ - 1
    chr(0xFBB4),  # ARABIC SYMBOL TWO DOTS ABOVE - ﮴ -  ﮴ - 1
    chr(0xFBB5),  # ARABIC SYMBOL TWO DOTS BELOW - ﮵ -  ﮵ - 1
    chr(0xFBB6),  # ARABIC SYMBOL THREE DOTS ABOVE - ﮶ -  ﮶ - 1
    chr(0xFBB7),  # ARABIC SYMBOL THREE DOTS BELOW - ﮷ -  ﮷ - 1
    chr(0xFBB8),  # ARABIC SYMBOL THREE DOTS POINTING DOWNWARDS ABOVE - ﮸ -  ﮸ - 1
    chr(0xFBB9),  # ARABIC SYMBOL THREE DOTS POINTING DOWNWARDS BELOW - ﮹ -  ﮹ - 1
    chr(0xFBBA),  # ARABIC SYMBOL FOUR DOTS ABOVE - ﮺ -  ﮺ - 1
    chr(0xFBBB),  # ARABIC SYMBOL FOUR DOTS BELOW - ﮻ -  ﮻ - 1
    chr(0xFBBC),  # ARABIC SYMBOL DOUBLE VERTICAL BAR BELOW - ﮼ -  ﮼ - 1
    chr(0xFBBD),  # ARABIC SYMBOL TWO DOTS VERTICALLY ABOVE - ﮽ -  ﮽ - 1
    chr(0xFBBE),  # ARABIC SYMBOL TWO DOTS VERTICALLY BELOW - ﮾ -  ﮾ - 1
    chr(0xFBBF),  # ARABIC SYMBOL RING - ﮿ -  ﮿ - 1
    chr(0xFBC0),  # ARABIC SYMBOL SMALL TAH ABOVE - ﯀ -  ﯀ - 1
    chr(0xFBC1),  # ARABIC SYMBOL SMALL TAH BELOW - ﯁ -  ﯁ - 1
    chr(0xFBC2),  # ARABIC SYMBOL WASLA ABOVE - ﯂ -  ﯂ - 1
    chr(0x8F7),  # ARABIC LEFT ARROWHEAD ABOVE - ࣷ -  ࣷ - 1
    chr(0x8F8),  # ARABIC RIGHT ARROWHEAD ABOVE - ࣸ -  ࣸ - 1
    chr(0x8F9),  # ARABIC LEFT ARROWHEAD BELOW - ࣹ -  ࣹ - 1
    chr(0x8FA),  # ARABIC RIGHT ARROWHEAD BELOW - ࣺ -  ࣺ - 1
    chr(0x8FB),  # ARABIC DOUBLE RIGHT ARROWHEAD ABOVE - ࣻ -  ࣻ - 1
    chr(0x8FC),  # ARABIC DOUBLE RIGHT ARROWHEAD ABOVE WITH DOT - ࣼ -  ࣼ - 1
    chr(0x8FD),  # ARABIC RIGHT ARROWHEAD ABOVE WITH DOT - ࣽ -  ࣽ - 1
    chr(0x8FF),  # ARABIC MARK SIDEWAYS NOON GHUNNA - ࣿ -  ࣿ - 1
    chr(0x65A),  # ARABIC VOWEL SIGN SMALL V ABOVE - ٚ -  ٚ - 1
    chr(0x65B),  # ARABIC VOWEL SIGN INVERTED SMALL V ABOVE - ٛ -  ٛ - 1
    chr(0x65C),  # ARABIC VOWEL SIGN DOT BELOW - ٜ -  ٜ - 1
    chr(0x6DD),  # ARABIC END OF AYAH - ۝ -  ۝ - 1
    chr(0x6DE),  # ARABIC START OF RUB EL HIZB - ۞ -  ۞ - 1
    chr(0x6E9),  # ARABIC PLACE OF SAJDAH - ۩ -  ۩ - 1
    chr(0x6EA),  # ARABIC EMPTY CENTRE LOW STOP - ۪ -  ۪ - 1
    chr(0x6EB),  # ARABIC EMPTY CENTRE HIGH STOP - ۫ -  ۫ - 1
    chr(0x6EC),  # ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE - ۬ -  ۬ - 1
    chr(0x883),  # ARABIC TATWEEL WITH OVERSTRUCK HAMZA - ࢃ -  ࢃ - 1
    chr(0x884),  # ARABIC TATWEEL WITH OVERSTRUCK WAW - ࢄ -  ࢄ - 1
    chr(0x885),  # ARABIC TATWEEL WITH TWO DOTS BELOW - ࢅ -  ࢅ - 1
    chr(0x887),  # ARABIC BASELINE ROUND DOT - ࢇ -  ࢇ - 1
    chr(0x888),  # ARABIC RAISED ROUND DOT - ࢈ -  ࢈ - 1
    chr(0x88E),  # ARABIC VERTICAL TAIL - ࢎ -  ࢎ - 1
    chr(0x8EA),  # ARABIC TONE ONE DOT ABOVE - ࣪ -  ࣪ - 1
    chr(0x8EB),  # ARABIC TONE TWO DOTS ABOVE - ࣫ -  ࣫ - 1
    chr(0x8EC),  # ARABIC TONE LOOP ABOVE - ࣬ -  ࣬ - 1
    chr(0x8ED),  # ARABIC TONE ONE DOT BELOW - ࣭ -  ࣭ - 1
    chr(0x8EE),  # ARABIC TONE TWO DOTS BELOW - ࣮ -  ࣮ - 1
    chr(0x8EF),  # ARABIC TONE LOOP BELOW - ࣯ -  ࣯ - 1
    chr(0x89C),  # ARABIC MADDA WAAJIB - ࢜ -  ࢜ - 1
    chr(0x89D),  # ARABIC SUPERSCRIPT ALEF MOKHASSAS - ࢝ -  ࢝ - 1
    chr(0x89E),  # ARABIC DOUBLED MADDA - ࢞ -  ࢞ - 1
    chr(0x600),  # ARABIC NUMBER SIGN - ؀ -  ؀ - 1
    chr(0x601),  # ARABIC SIGN SANAH - ؁ -  ؁ - 1
    chr(0x602),  # ARABIC FOOTNOTE MARKER - ؂ -  ؂ - 1
    chr(0x603),  # ARABIC SIGN SAFHA - ؃ -  ؃ - 1
    chr(0x604),  # ARABIC SIGN SAMVAT - ؄ -  ؄ - 1
    chr(0x605),  # ARABIC NUMBER MARK ABOVE - ؅ -  ؅ - 1
    chr(0x608),  # ARABIC RAY - ؈ -  ؈ - 1
    chr(0x610),  # ARABIC SIGN SALLALLAHOU ALAYHE WASSALLAM - ؐ -  ؐ - 1
    chr(0x611),  # ARABIC SIGN ALAYHE ASSALLAM - ؑ -  ؑ - 1
    chr(0x612),  # ARABIC SIGN RAHMATULLAH ALAYHE - ؒ -  ؒ - 1
    chr(0x613),  # ARABIC SIGN RADI ALLAHOU ANHU - ؓ -  ؓ - 1
    chr(0x614),  # ARABIC SIGN TAKHALLUS - ؔ -  ؔ - 1
    chr(0x61C),  # ARABIC LETTER MARK - ؜ -  ؜ - 1
    chr(0x61D),  # ARABIC END OF TEXT MARK - ؝ -  ؝ - 1
    chr(0x61E),  # ARABIC TRIPLE DOT PUNCTUATION MARK - ؞ -  ؞ - 1
    chr(0x653),  # ARABIC MADDAH ABOVE - ٓ -  ٓ - 1
    chr(0x656),  # ARABIC SUBSCRIPT ALEF - ٖ -  ٖ - 1
    chr(0x658),  # ARABIC MARK NOON GHUNNA - ٘ -  ٘ - 1
    chr(0x659),  # ARABIC ZWARAKAY - ٙ -  ٙ - 1
    chr(0x66D),  # ARABIC FIVE POINTED STAR - ٭ -  ٭ - 1
    chr(0x670),  # ARABIC LETTER SUPERSCRIPT ALEF - ٰ -  ٰ - 1
    chr(0x6D4),  # ARABIC FULL STOP - ۔ -  ۔ - 1
    chr(0x890),  # ARABIC POUND MARK ABOVE - ࢐ -  ࢐ - 1
    chr(0x891),  # ARABIC PIASTRE MARK ABOVE - ࢑ -  ࢑ - 1
    chr(0x89F),  # ARABIC HALF MADDA OVER MADDA - ࢟ -  ࢟ - 1
    chr(0x8CE),  # ARABIC LARGE ROUND DOT ABOVE - ࣎ -  ࣎ - 1
    chr(0x8CF),  # ARABIC LARGE ROUND DOT BELOW - ࣏ -  ࣏ - 1
    chr(0x8D0),  # ARABIC SUKUN BELOW - ࣐ -  ࣐ - 1
    chr(0x8D1),  # ARABIC LARGE CIRCLE BELOW - ࣑ -  ࣑ - 1
    chr(0x8D2),  # ARABIC LARGE ROUND DOT INSIDE CIRCLE BELOW - ࣒ -  ࣒ - 1
    chr(0x8E2),  # ARABIC DISPUTED END OF AYAH - ࣢ -  ࣢ - 1
    chr(0x206C),  # INHIBIT ARABIC FORM SHAPING - ⁬ -  ⁬ - 1
    chr(0x206D),  # ACTIVATE ARABIC FORM SHAPING - ⁭ -  ⁭ - 1
]

if __name__ == "__main__":
    # a = set(temp_new.keys())
    # b = set(temp_old.keys())
    # print(b.intersection(a))

    pass
