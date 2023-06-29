from src.utils.random import seeded_weighted_selection


def test_seeded_weighted_selection_without_seed():
    traits = [["Trait 1", 1], ["Trait 2", 2], ["Trait 3", 3]]
    assert seeded_weighted_selection(traits) in ["Trait 1", "Trait 2", "Trait 3"]


def test_seeded_weighted_selection_with_valid_data():
    traits = [["Trait 1", 1], ["Trait 2", 2], ["Trait 3", 3]]
    seed = 123456
    nonce = 2
    assert seeded_weighted_selection(traits, seed, nonce) == "Trait 2"


def test_seeded_weighted_selection_with_equal_weights():
    traits = [["Trait 1", 1], ["Trait 2", 1], ["Trait 3", 1]]
    seed = 123456
    nonce = 3
    assert seeded_weighted_selection(traits, seed, nonce) == "Trait 2"


def test_seeded_weighted_selection_with_no_seed():
    traits = [["Trait 1", 1], ["Trait 2", 2], ["Trait 3", 3]]
    assert seeded_weighted_selection(traits) in ["Trait 1", "Trait 2", "Trait 3"]


def test_seeded_weighted_selection_with_one_trait():
    traits = [["Trait 1", 1]]
    seed = 123456
    nonce = 0
    assert seeded_weighted_selection(traits, seed, nonce) == "Trait 1"


def test_seeded_weighted_selection_with_zero_weights():
    traits = [["Trait 1", 0], ["Trait 2", 0], ["Trait 3", 3]]
    seed = 123456
    nonce = 4
    assert seeded_weighted_selection(traits, seed, nonce) == "Trait 3"


def test_seeded_weighted_selection_with_negative_weights():
    traits = [["Trait 1", -1], ["Trait 2", -2], ["Trait 3", 3]]
    seed = 123456
    nonce = 5
    try:
        seeded_weighted_selection(traits, seed, nonce)
        assert False  # Expected an exception
    except ValueError:
        assert True
