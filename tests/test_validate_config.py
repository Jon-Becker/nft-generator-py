from unittest.mock import patch

import pytest

from src.common.exceptions import ConfigValidationError
from src.common.validate import validate_config


@patch("os.path.isfile", return_value=True)
def test_validate_config_valid_input(mock_isfile):
    valid_config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    assert validate_config(valid_config) is None  # It should not raise an exception


def test_validate_config_missing_key():
    config = {
        "layers": [],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_mismatch_weights():
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo", "some other value"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo", "some file"],
                "weights": [100],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_mismatch_filename():
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo", "some other value"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100, 100],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_mismatch_values():
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo", "logo 2"],
                "weights": [100, 100],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_incorrect_type():
    config = {
        "layers": "should be a list",
        "incompatibilities": [],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_missing_layer_key():
    config = {
        "layers": [
            {
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_invalid_layer_key_type():
    config = {
        "layers": [
            {
                "name": 123,
                "values": "Python Logo",
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_value_type():
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo", 1],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_weight_length():
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100, 0],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_weight_sum():
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo", "1"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100, 1],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


def test_validate_config_layer_weight_type():
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo", "1"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": ["100", "1"],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_layer_filename_wrong_type(mock_isfile):
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo", "1"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo", 2],
                "weights": [100, 1],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=False)
def test_validate_config_layer_filename_nonexistent(mock_isfile):
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_missing_incompatibility_key(mock_isfile):
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {"value": "Python Logo", "incompatible_with": ["Python Logo"]}
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_key_type(mock_isfile):
    config = {
        "layers": [
            {
                "name": "123",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {"layer": 1, "value": "Python Logo", "incompatible_with": ["Python Logo"]}
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_incompatibility_type(mock_isfile):
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {"layer": "Background", "value": "Python Logo", "incompatible_with": [2]}
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_value_type(mock_isfile):
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {"layer": "Background", "value": 2, "incompatible_with": ["Python Logo"]}
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_value_value(mock_isfile):
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {"layer": "Background", "value": "2", "incompatible_with": ["Python Logo"]}
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_invalid_layer_value(mock_isfile):
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background 2",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo 2"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)


@patch("os.path.isfile", return_value=True)
def test_validate_config_invalid_incompatibility_invalid_incompatibility_value(
    mock_isfile,
):
    config = {
        "layers": [
            {
                "name": "Background",
                "values": ["Python Logo"],
                "trait_path": "./trait-layers/foreground",
                "filename": ["logo"],
                "weights": [100],
            }
        ],
        "incompatibilities": [
            {
                "layer": "Background",
                "value": "Python Logo",
                "incompatible_with": ["Python Logo 2"],
            }
        ],
        "baseURI": ".",
        "name": "NFT #",
        "description": "This is a description for this NFT series.",
    }

    with pytest.raises(ConfigValidationError):
        validate_config(config)
