class String():
    """ For operations with strings """

    @staticmethod
    def is_empty(value: str) -> bool:
        return value is None or value.strip() == ""

    @staticmethod
    def is_equal(value: str, expected: str, case_sensitive: bool = True) -> bool:
        if not case_sensitive:
            return value.lower() == expected.lower()
        return value == expected

    @staticmethod
    def remove_substring(text : str, substr : str) -> str:
        return "".join(text.split(substr))

