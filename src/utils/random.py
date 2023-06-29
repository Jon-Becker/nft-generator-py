import random


def seeded_weighted_selection(
    traits: list[list], seed: int = None, nonce: int = 0
) -> str:
    """
    Selects a random trait based on a weighted selection.

    :param traits: A list of traits, each trait being a list of strings and an integer.
    :param seed: The seed to use for the random selection.
    :return: A random trait.
    """
    values = [trait[0] for trait in traits]
    weights = [trait[1] for trait in traits]

    if seed is not None:
        random.seed(seed + nonce)
    else:
        random.seed()

    return random.choices(values, weights)[0]
