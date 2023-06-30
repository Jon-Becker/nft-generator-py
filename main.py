import argparse

from src.core.config import generate_config
from src.core.main import Generator
from src.core.metadata import update_metadata

# add CLI arguments
generator = argparse.ArgumentParser(
    prog="generate", usage="main.py <command> [options]"
)

# add subcommands
generator.add_argument(
    "command",
    choices=["generate", "validate", "update_metadata", "build_config"],
    help="Command to execute",
)

# add arguments
generator.add_argument("-n", "--amount", help="Amount to generate")
generator.add_argument("-c", "--config", help="Path to configuration file")
generator.add_argument(
    "-o", "--output", help="Path to output, either a folder or file", default="./output"
)
generator.add_argument("-s", "--seed", help="Seed for random generator", default=None)
generator.add_argument(
    "-v",
    "--verbose",
    help="Verbosity level",
    action="count",
    default=0,
)
generator.add_argument(
    "--start-at",
    help="Token ID to start with",
    default=0,
)
generator.add_argument(
    "--image-path", help="Path to the image folder, or the IPFS CID."
)
generator.add_argument("--trait-dir", help="Path to the trait directory")

# add flags
generator.add_argument(
    "--no-pad",
    help="Disable zero-padding on token ID",
    action="store_true",
    default=False,
)
generator.add_argument(
    "--allow-duplicates",
    help="Allow duplicate combinations",
    action="store_true",
    default=False,
)

# parse and validate arguments
args = generator.parse_args()
args=vars(args)

if args["command"] == "validate":
    generator: Generator = Generator(**args)
    generator.logger.info("Configuration is valid!")

elif args["command"] == "generate":
    generator: Generator = Generator(**args)
    generator.generate()

elif args["command"] == "update_metadata":
    update_metadata(args["image_path"], args["output"], args["verbose"])

elif args["command"] == "build_config":
    if args["output"] == "./output":
        args["output"] = "generated.json"

    if not args["trait_dir"]:
        raise ValueError("No trait directory was provided.")

    generate_config(args["trait_dir"], args["output"], args["verbose"])
