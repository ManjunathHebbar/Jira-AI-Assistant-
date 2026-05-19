import hashlib


def generate_content_hash(content):

    return hashlib.md5(
        content.encode("utf-8")
    ).hexdigest()