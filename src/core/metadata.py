import glob

from src.utils.io import read_json, write_json
from src.utils.logger import get_logger, get_progress_bar


def update_metadata(image_path: str, output: str, verbose: int):
    """
    Updates the image paths in the metadata files.
    """
    logger = get_logger(verbose)

    if not image_path:
        raise ValueError("No image path was provided.")
    elif not image_path.endswith("/"):
        raise ValueError(
            "Invalid image path '{}'. It should end with a '/'.".format(image_path)
        )

    all_metadata_files = glob.glob(f"{output}/metadata/*.json")

    with get_progress_bar(len(all_metadata_files)) as bar:
        for file in all_metadata_files:
            if file.endswith("all-objects.json"):
                continue

            # read the file
            json_contents = read_json(file)
            token_id = json_contents["token_id"]
            json_contents["image"] = f"{image_path}{token_id}.png"

            # write the file
            write_json(file, json_contents)
            bar()

    logger.info("Updated image paths in metadata files.")
