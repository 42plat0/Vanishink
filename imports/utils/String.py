class String():
    """ For operations with strings """
    def remove_substring(text : str, substr : str) -> None:
        return "".join(text.split(substr))