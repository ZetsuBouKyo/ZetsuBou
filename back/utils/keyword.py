from back.model.search import ParsedKeywords


class KeywordParser:
    def __init__(self):
        self._init()

    def _init(self):
        self._parsed_keywords = ParsedKeywords()
        self._field_name = ""
        self._field_value = ""

        self._included = True
        self._is_field_name = True
        self._in_quotes = False

    def _update(self, c=""):
        if not self._is_field_name:
            if self._field_name and self._field_value:
                if self._included:
                    self._parsed_keywords.includes.append(
                        (self._field_name.strip(), self._field_value.strip())
                    )
                else:
                    self._parsed_keywords.excludes.append(
                        (self._field_name.strip(), self._field_value.strip())
                    )
        else:
            if not self._included:
                self._parsed_keywords.excludes.append((self._field_name.strip(), ""))
            else:
                self._parsed_keywords.remaining_keywords += (
                    self._field_name + self._field_value + c
                )

    def parse(self, keywords: str, value_sep: str = "=") -> ParsedKeywords:
        self._init()
        self._parsed_keywords.keywords = keywords
        if keywords.count('"') % 2 == 1:
            self._parsed_keywords.remaining_keywords = keywords
            return self._parsed_keywords

        for i, c in enumerate(keywords):
            if i == 0:
                if c == "-":
                    self._included = False
                elif c == '"':
                    self._in_quotes = True
                else:
                    self._field_name += c
                continue

            if c == " ":
                if self._in_quotes:
                    if self._is_field_name:
                        self._field_name += c
                    else:
                        self._field_value += c
                else:
                    self._update(c)
                    self.reset()
            elif c == '"':
                if self._in_quotes:
                    if not self._is_field_name:
                        self._update()
                        self.reset()
                    else:
                        self._in_quotes = False
                else:
                    self._in_quotes = True
            elif c == "-" and self._field_name == "":
                self._included = False

            elif c == value_sep:
                if not self._is_field_name:
                    self._field_value += c
                else:
                    self._is_field_name = False
            else:
                if self._is_field_name:
                    self._field_name += c
                else:
                    self._field_value += c

        self._update()
        self._parsed_keywords.remaining_keywords = (
            self._parsed_keywords.remaining_keywords.strip()
        )
        return self._parsed_keywords

    def reset(self):
        self._field_name = ""
        self._field_value = ""
        self._included = True
        self._is_field_name = True
        self._in_quotes = False
