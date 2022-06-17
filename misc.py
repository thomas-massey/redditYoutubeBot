def tidy_up_text(text):
    """
    Tidies up the text to make it easier to process.
    """
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = text.replace("  ", " ")
    return text