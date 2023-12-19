import os

from huggingface_hub import HfApi, login


def huggingface_login():
    api = HfApi()
    token = os.environ.get("HUGGINGFACE_TOKEN")
    if token:
        login(token)
    else:
        raise ValueError("HUGGINGFACE_TOKEN environment variable not set.")
