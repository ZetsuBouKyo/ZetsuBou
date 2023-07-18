from back.utils.keyword import KeywordParser


def test():
    data = [
        ("-language=english", "", [], [("language", "english")]),
        ('-language="english"', "", [], [("language", "english")]),
        ('-"language"=english', "", [], [("language", "english")]),
        ('-"language"="english"', "", [], [("language", "english")]),
        ("language=中文", "", [("language", "中文")], []),
        (" language=中文", "", [("language", "中文")], []),
        (" language=中文 ", "", [("language", "中文")], []),
        (" language=中文  ", "", [("language", "中文")], []),
        ("language=中文 ", "", [("language", "中文")], []),
        ("language=中文  ", "", [("language", "中文")], []),
        ('language="中文"', "", [("language", "中文")], []),
        ('"language"=中文', "", [("language", "中文")], []),
        ('"language"="中文"', "", [("language", "中文")], []),
        ('language="English (UK)"', "", [("language", "English (UK)")], []),
        ('"file page"=12', "", [("file page", "12")], []),
        (
            'language=中文 text="hello world"wrong"  format" -"language"=en "tags.subject"=math   tags.color=yellow',
            "wrong  format",
            [
                ("language", "中文"),
                ("text", "hello world"),
                ("tags.subject", "math"),
                ("tags.color", "yellow"),
            ],
            [("language", "en")],
        ),
        (
            "[社會 (歷史)] 今天天氣真好=(三國演義) [Chn]",
            "[社會 (歷史)] [Chn]",
            [("今天天氣真好", "(三國演義)")],
            [],
        ),
        ('"["社會" (歷史)] 今天天氣真好=(三國演義) [Chn]', "", [], []),
    ]

    parser = KeywordParser()
    for keywords, ans_remaining_keywords, ans_includes, ans_excludes in data:
        print("\n")
        parsed_keywords = parser.parse(keywords)
        print(f"keywords: {parsed_keywords.keywords}")
        print(f"remaining keywords: {parsed_keywords.remaining_keywords}")
        print(f"includes: {parsed_keywords.includes}")
        print(f"excludes: {parsed_keywords.excludes}")

        assert parsed_keywords.keywords == keywords
        assert parsed_keywords.remaining_keywords == ans_remaining_keywords
        assert parsed_keywords.includes == ans_includes
        assert parsed_keywords.excludes == ans_excludes
