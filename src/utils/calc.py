def calculate_possible_combinations(config: dict) -> int:
    """
    Calculate the number of possible combinations for a given configuration.

    :param config: The configuration to calculate the combinations for.
    :return: The number of possible combinations.
    """

    # Extract the layers from the config dictionary
    layers = config.get("layers", [])

    # Build a set of incompatibilities
    incompatibilities = set()
    for incompatibility in config.get("incompatibilities", []):
        layer = incompatibility.get("layer")
        value = incompatibility.get("value")
        incompatibilities.add((layer, value))

    # Calculate combinations
    total_combinations = 1
    for layer in layers:
        layer_name = layer.get("name")
        values = layer.get("values", [])
        num_values = len(values)

        # If layer has incompatible values, reduce num_values by 1
        # since the incompatible value will be replaced by the default one.
        for value in values:
            if (layer_name, value) in incompatibilities:
                num_values -= 1
                break

        total_combinations *= max(num_values, 1)

    return total_combinations
