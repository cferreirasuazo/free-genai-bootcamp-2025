import json


def make_payload(group_name, words):
    return json.dumps({
        "group_name": group_name,
        "words": words
    })

