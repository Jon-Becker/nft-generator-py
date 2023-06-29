import argparse

from src.common.validate import validate_args
from src.core.main import Generator

# add CLI arguments
generator = argparse.ArgumentParser(prog="generate", usage="generate.py [options]")
generator.add_argument("-n", "--amount", help="Amount to generate")
generator.add_argument("-c", "--config", help="Path to configuration file")
generator.add_argument(
    "-o", "--output", help="Path to output folder", default="./output"
)
generator.add_argument("-s", "--seed", help="Seed for random generator", default=None)
generator.add_argument(
    "-v", "--verbose", help="Verbosity level", action="count", default=0
)
generator.add_argument("--start-at", help="Token ID to start with", default=0)

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
validate_args(args)

print(args)

generator: Generator = Generator(args)
generator.generate()
