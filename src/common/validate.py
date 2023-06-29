import os

from src.common.exceptions import ArgumentValidationError, ConfigValidationError


def validate_args(args) -> bool:
    """
    Validates the arguments passed to the program.

    :param args: The arguments passed to the program.
    :return: True if the arguments are valid, panics otherwise.
    """

    if not args.amount:
        raise ArgumentValidationError("Missing mandatory option: -n / --amount")

    if not args.config:
        raise ArgumentValidationError("Missing mandatory option: -c / --config")
    elif not os.path.isfile(args.config):
        raise ArgumentValidationError(
            "Configuration file not found: '{}'".format(args.config)
        )

    if args.output:
        if not os.path.isdir(args.output):
            try:
                os.makedirs(args.output + "/images")
                os.makedirs(args.output + "/metadata")
            except OSError:
                raise ArgumentValidationError(
                    "Invalid output directory: '{}'".format(args.output)
                )

    if args.seed:
        try:
            int(args.seed)
        except ValueError:
            raise ArgumentValidationError("Invalid seed: '{}'".format(args.seed))


def validate_config(config: dict) -> bool:
    """
    Validates the generation configuration

    :param config: The provided configuration dict
    :return: True if the configuration is valid, panics otherwise.
    """
    all_trait_values = []
    required_config_values = list(
        zip(
            ["layers", "incompatibilities", "baseURI", "name", "description"],
            [list, list, str, str, str],
        )
    )
    required_layer_values = list(
        zip(
            ["name", "values", "trait_path", "filename", "weights"],
            [str, list, str, list, list],
        )
    )
    required_incompatibility_values = list(
        zip(["layer", "value", "incompatible_with"], [str, str, list, dict])
    )

    # check if all required config values are present
    for required_key in required_config_values:
        # check if all required keys are present
        if required_key[0] not in config:
            raise ConfigValidationError(
                "Missing configuration value: '{}'".format(required_key[0])
            )

        # check if the values are of the correct type
        if not isinstance(config[required_key[0]], required_key[1]):
            raise ConfigValidationError(
                "Invalid configuration value: '{}'. Expected type: {}".format(
                    required_key[0], required_key[1]
                )
            )

    # check the layers and their config values
    for i, layer in enumerate(config["layers"]):
        layer_trait_count = 0
        all_trait_values += layer["values"]
        for required_key in required_layer_values:
            # check if all required layer keys are present
            if required_key[0] not in layer:
                raise ConfigValidationError(
                    "config[\"layers\"][{}]: Missing required layer key: '{}'".format(
                        i, required_key[0]
                    )
                )

            # check if the layer configuration values are of the correct type
            if not isinstance(layer[required_key[0]], required_key[1]):
                raise ConfigValidationError(
                    "config[\"layers\"][{}]: Invalid layer configuration value: '{}'. Expected type: {}".format(
                        i, required_key[0], required_key[1]
                    )
                )

            # check if the layer values are valid
            if required_key[0] == "values":
                layer_trait_count = len(layer["values"])
                for j, value in enumerate(layer["values"]):
                    if not isinstance(value, str):
                        raise ConfigValidationError(
                            'config["layers"][{}]["{}"][{}]: Invalid layer value: \'{}\'. Expected type: {}'.format(
                                i, required_key[0], j, value, str
                            )
                        )

            # check if the layer trait path is valid
            if required_key[0] == "weights":
                if len(layer["weights"]) != layer_trait_count:
                    raise ConfigValidationError(
                        'config["layers"][{}]["{}"]: Invalid layer weights length: {}. Expected length: {}'.format(
                            i, required_key[0], len(layer["weights"]), layer_trait_count
                        )
                    )

                for j, weight in enumerate(layer["weights"]):
                    if not isinstance(weight, int):
                        raise ConfigValidationError(
                            'config["layers"][{}]["{}"][{}]: Invalid layer weight: \'{}\'. Expected type: {}'.format(
                                i, required_key[0], j, weight, int
                            )
                        )

                if sum(layer["weights"]) != 100:
                    raise ConfigValidationError(
                        'config["layers"][{}]["{}"]: The sum of the weights must be 100. Current sum: {}'.format(
                            i, required_key[0], sum(layer["weights"])
                        )
                    )

            # check if the layer filenames are valid
            if required_key[0] == "filename":
                for j, filename in enumerate(layer["filename"]):
                    if not isinstance(filename, str):
                        raise ConfigValidationError(
                            'config["layers"][{}]["{}"][{}]: Invalid layer filename: \'{}\'. Expected type: {}'.format(
                                i, required_key[0], j, filename, str
                            )
                        )

                    # check that the file exists
                    if not os.path.isfile(
                        "{}/{}.png".format(layer["trait_path"], filename)
                    ):
                        raise ConfigValidationError(
                            'config["layers"][{}]["{}"][{}]: File not found: \'{}/{}.png\''.format(
                                i, required_key[0], j, layer["trait_path"], filename
                            )
                        )

    # check the incompatibilities and their config values
    for i, incompatibility in enumerate(config["incompatibilities"]):
        # check if all required incompatibility keys are present
        for required_key in required_incompatibility_values:
            if required_key[0] not in incompatibility:
                raise ConfigValidationError(
                    "config[\"incompatibilities\"][{}]: Missing required incompatibility key: '{}'".format(
                        i, required_key[0]
                    )
                )

            # check if the incompatibility configuration values are of the correct type
            if not isinstance(incompatibility[required_key[0]], required_key[1]):
                raise ConfigValidationError(
                    "config[\"incompatibilities\"][{}]: Invalid incompatibility configuration value: '{}'. Expected type: {}".format(
                        i, required_key[0], required_key[1]
                    )
                )

            # check if the incompatibility values are valid
            if required_key[0] == "value":
                if incompatibility["value"] not in all_trait_values:
                    raise ConfigValidationError(
                        'config["incompatibilities"][{}]["{}"]: Invalid incompatibility value: \'{}\'. Expected one of: {}'.format(
                            i,
                            required_key[0],
                            incompatibility["value"],
                            all_trait_values,
                        )
                    )

            # check if the incompatibility incompatible_with values are valid
            if required_key[0] == "incompatible_with":
                for j, incompatible_with in enumerate(
                    incompatibility["incompatible_with"]
                ):
                    if not isinstance(incompatible_with, str):
                        raise ConfigValidationError(
                            'config["incompatibilities"][{}]["{}"][{}]: Invalid incompatibility incompatible_with: \'{}\'. Expected type: {}'.format(
                                i, required_key[0], j, incompatible_with, str
                            )
                        )

                    if incompatible_with not in all_trait_values:
                        raise ConfigValidationError(
                            'config["incompatibilities"][{}]["{}"][{}]: Invalid incompatibility incompatible_with: \'{}\'. Expected one of: {}'.format(
                                i,
                                required_key[0],
                                j,
                                incompatible_with,
                                all_trait_values,
                            )
                        )

            # check if the incompatibility default values are valid
            if required_key[0] == "layer":
                if incompatibility["layer"] not in [
                    layer["name"] for layer in config["layers"]
                ]:
                    raise ConfigValidationError(
                        'config["incompatibilities"][{}]["{}"]: Invalid incompatibility layer: \'{}\'. Expected one of: {}'.format(
                            i,
                            required_key[0],
                            incompatibility["layer"],
                            [layer["name"] for layer in config["layers"]],
                        )
                    )
