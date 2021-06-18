import json

# Settings
# Loads settings from json file


def init(path: str):
    global settings
    with open(path, 'r', encoding='utf8') as f:
        settings = json.load(f)


# def __init__(path: str, glob: bool = True) -> None:
#     # path  # Path to settings file
#     # glob  # Determines if settings are returned or stored in global var (Not implemented)
#     load()
