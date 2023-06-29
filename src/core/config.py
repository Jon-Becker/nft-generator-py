import json
import os

from src.utils.io import list_full_dir, list_name
from src.utils.logger import get_logger


def generate_config(trait_dir: str, output: str, verbose: int) -> None:
    logger = get_logger(verbose)
    layerlist = list_name(f"{trait_dir}/*")
    path_list = list_full_dir(f"{trait_dir}/")
    item_list = [list_name(items + "/*") for items in path_list]

    # calculate weight
    weight = []
    for i in range(len(item_list)):
        weight.append(100 / len(item_list[i]))
        for j in range(len(item_list[i])):
            item_list[i][j] = item_list[i][j].split(".")[0]

    weightlist = [] * len(layerlist)

    for i in range(len(weight)):
        x = 100 / weight[i]
        temp1 = []
        for _ in range(int(x)):
            temp1.append(weight[i])
        weightlist.append(temp1)

    # generate json blob
    finalized_layers = []
    for x in range(len(layerlist)):
        layer = {
            "name": layerlist[x],
            "values": item_list[x],
            "trait_path": path_list[x],
            "filename": item_list[x],
            "weights": weightlist[x],
        }
        finalized_layers.append(layer)

    config = {
        "layers": finalized_layers,
        "incompatibilities": [],
        "baseURI": "TODO",
        "name": "TODO",
        "description": "TODO",
    }

    # ensure the directory exists for the output file
    print(config)
    try:
        os.makedirs(os.path.dirname(output), exist_ok=True)
    except OSError:
        pass

    with open(output, "w") as outfile:
        json.dump(config, outfile, indent=4)

    logger.info(f"Generated config file at {output}")
    logger.warning(
        "You'll need to manually update the baseURI, name, and description fields."
    )
