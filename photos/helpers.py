import re

from rest_framework.exceptions import ValidationError


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


def validate_ids(data, field="id", unique=True):
    if isinstance(data, list):
        id_list = [int(x[field]) for x in data]

        if unique and len(id_list) != len(set(id_list)):
            raise ValidationError(
                "Multiple updates to a single {} found".format(field))

        return id_list

    return [data]
