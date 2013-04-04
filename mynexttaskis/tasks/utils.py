import re


def get_categories(task_string):
    """
    Return an array of hashtag-esque categories from a task string
    """
    return re.findall(r'(?:\s?#(\w+)\s?)', task_string)
