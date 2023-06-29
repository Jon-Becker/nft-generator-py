import glob
import json
import os


def read_json(path: str) -> dict:
    """
    Reads the json file and returns its contents as a dictionary

    :param path: Path to the json file
    :return: Dictionary contents of the json file
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


def write_file(path: str, contents: str):
    """
    Writes a string to a file

    :param path: Path to the output file
    :param contents: The string to write
    """

    # create folder structure if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(contents)


def list_full_dir(path: str) -> list:
    return glob.glob(os.path.join(path, "*"))


def list_name(path: str) -> list:
    return [os.path.basename(x) for x in glob.glob(path)]
