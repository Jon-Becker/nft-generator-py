from unittest import mock

import pytest

from src.common.exceptions import ArgumentValidationError
from src.common.validate import validate_args


class MockArgs:
    def __init__(self, amount=None, config=None, output=None, seed=None):
        self.amount = amount
        self.config = config
        self.output = output
        self.seed = seed


@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.path.isdir", return_value=False)
@mock.patch("os.makedirs")
def test_validate_args_missing_amount(mock_makedirs, mock_isdir, mock_isfile):
    args = MockArgs(config="config.txt")
    with pytest.raises(ArgumentValidationError):
        validate_args(args)


@mock.patch("os.path.isfile", return_value=False)
def test_validate_args_missing_config(mock_isfile):
    args = MockArgs(amount=1)
    with pytest.raises(ArgumentValidationError):
        validate_args(args)


@mock.patch("os.path.isfile", return_value=False)
def test_validate_args_invalid_config_path(mock_isfile):
    args = MockArgs(amount=1, config="nonexistent_config.txt")
    with pytest.raises(ArgumentValidationError):
        validate_args(args)


@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.path.isdir", return_value=False)
@mock.patch("os.makedirs", side_effect=OSError)
def test_validate_args_invalid_output_directory(mock_makedirs, mock_isdir, mock_isfile):
    args = MockArgs(amount=1, config="config.txt", output="invalid\0dir")
    with pytest.raises(ArgumentValidationError):
        validate_args(args)


@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.path.isdir", return_value=True)
def test_validate_args_invalid_seed(mock_isdir, mock_isfile):
    args = MockArgs(amount=1, config="config.txt", seed="invalid_seed")
    with pytest.raises(ArgumentValidationError):
        validate_args(args)


@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.path.isdir", return_value=True)
def test_validate_args_valid_arguments(mock_isdir, mock_isfile):
    args = MockArgs(amount=1, config="config.txt", output="output_dir", seed="123")
    # Should not raise any exceptions
    validate_args(args)


@mock.patch("os.path.isfile", return_value=True)
@mock.patch("os.path.isdir", return_value=False)
@mock.patch("os.makedirs")
def test_validate_args_create_output_directory(mock_makedirs, mock_isdir, mock_isfile):
    args = MockArgs(amount=1, config="config.txt", output="new_output_dir", seed="123")
    validate_args(args)
    assert mock_makedirs.call_count == 2
