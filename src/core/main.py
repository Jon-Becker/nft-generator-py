import concurrent.futures

from PIL import Image
from tqdm import tqdm

from src.common.validate import validate_config
from src.utils.calc import calculate_possible_combinations
from src.utils.io import load_config, write_json
from src.utils.logger import get_logger
from src.utils.random import seeded_weighted_selection


class Generator:
    def __init__(self, args):
        # set verbosity level (0 = silent, 1 = normal, 2 = verbose) and initialize logger
        self.verbosity = args.verbose + 1
        self.logger = get_logger(max(50 - (10 * self.verbosity), 10))

        # read configuration and validate it
        self.logger.debug("Loading configuration from '%s'", args.config)
        self.config = load_config(args.config)
        self.logger.debug("Validating configuration")
        validate_config(self.config)

        # set arguments
        self.amount = int(args.amount)
        self.seed = int(args.seed) if args.seed is not None else None
        self.start_at = int(args.start_at)
        self.output = args.output
        self.allow_duplicates = args.allow_duplicates
        self.no_pad = args.no_pad

        # initialize state
        self.nonce = 0
        self.pad_amount = 0 if self.no_pad else len(str(self.amount))
        self.all_genomes = []

    def __build_genome_metadata(self, token_id: int = 0):
        """
        Builds the generation / NFT metadata for a single NFT.
        """

        genome_traits = {}

        # select traits for each layer
        for layer in self.config["layers"]:
            trait_values_and_weights = list(zip(layer["values"], layer["weights"]))
            genome_traits[layer["name"]] = seeded_weighted_selection(
                trait_values_and_weights, seed=self.seed, nonce=self.nonce
            )
            self.nonce += 1

        # check for incompatibilities
        for incompatibility in self.config["incompatibilities"]:
            for trait in genome_traits:
                if (
                    genome_traits[incompatibility["layer"]] == incompatibility["value"]
                    and genome_traits[trait] in incompatibility["incompatible_with"]
                ):
                    # if a default incompatibility value is set, use it instead
                    if "default" in incompatibility:
                        genome_traits[trait] = incompatibility["default"]["value"]
                    else:
                        return self.__build_genome_metadata(token_id)

        if genome_traits in self.all_genomes and not self.allow_duplicates:
            return self.__build_genome_metadata(token_id)
        else:
            self.all_genomes.append(
                {
                    "token_id": token_id,
                    "image": "{}/images/{}.png".format(self.output, token_id),
                    "name": self.config["name"] + str(token_id).zfill(self.pad_amount),
                    "description": self.config["description"],
                    "attributes": [
                        {
                            "trait_type": layer["name"],
                            "value": genome_traits[layer["name"]],
                        }
                        for layer in self.config["layers"]
                    ],
                }
            )

    def __build_genome_image(self, metadata: dict):
        """
        Builds the NFT image for a single NFT.
        """
        layers = []
        for index, attr in enumerate(metadata["attributes"]):
            # get the image for the trait
            for i, trait in enumerate(self.config["layers"][index]["values"]):
                if trait == attr["value"]:
                    layers.append(
                        Image.open(
                            f'{self.config["layers"][index]["trait_path"]}/{self.config["layers"][index]["filename"][i]}.png'
                        ).convert("RGBA")
                    )
                    break

        if len(layers) == 1:
            rgb_im = layers[0].convert("RGBA")
        elif len(layers) == 2:
            main_composite = Image.alpha_composite(layers[0], layers[1])
            rgb_im = main_composite.convert("RGBA")
        elif len(layers) >= 3:
            main_composite = Image.alpha_composite(layers[0], layers[1])
            for index, remaining in enumerate(layers):
                main_composite = Image.alpha_composite(main_composite, remaining)
            rgb_im = main_composite.convert("RGBA")

        rgb_im.save("{}/images/{}.png".format(self.output, metadata["token_id"]))

    def generate(self):
        """
        Generates the NFTs with the given configuration.
        """
        self.logger.info("Starting generation")

        max_combinations = calculate_possible_combinations(self.config)
        self.logger.debug(
            "There are {:,} possible unique combinations of this configuration".format(
                max_combinations
            )
        )
        if self.amount > max_combinations and not self.allow_duplicates:
            raise ValueError(
                "Amount of NFTs to generate ({:,}) is greater than the number of possible unique combinations ({:,})".format(
                    self.amount, max_combinations
                )
            )

        self.logger.info("Generating %d NFTs", self.amount)
        for i in tqdm(range(self.amount)):
            token_id = self.start_at + i
            self.__build_genome_metadata(token_id)
            write_json(
                "{}/metadata/{}.json".format(self.output, token_id),
                self.all_genomes[-1],
            )
        write_json(
            "{}/metadata/all-objects.json".format(
                self.output,
            ),
            self.all_genomes,
        )

        self.logger.info("Generating layered images for %d NFTs", self.amount)

        # create thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            # Create a list to hold the future objects
            futures = []

            # Submit the tasks to the executor
            for i in tqdm(range(self.amount)):
                token_id = self.start_at + i
                future = executor.submit(self.__build_genome_image, self.all_genomes[i])
                futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
