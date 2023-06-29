import json
import os


def load_config(path: str) -> dict:
    """
    Reads the json configuration file and returns a dictionary with the configuration

    :param path: Path to the configuration file
    :return: Dictionary with the configuration
    """
    with open(path) as f:
        config = json.load(f)
    return config


def write_json(path: str, obj: dict):
    """
    Writes a dictionary to a json file

    :param path: Path to the output file
    :param obj: The json to write
    """

    # create folder structure if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)
