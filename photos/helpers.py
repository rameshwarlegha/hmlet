import re


def extract_hashtag(caption):
    """
    Takes a string returns unique # present in it.

    Parameters
    ----------
    caption : <string>

    Returns
    -------
    set : unique hash tags of type set
    """
    hashtag_list = re.findall(r"#(\w+)", caption)
    return set(hashtag_list)
