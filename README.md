
# nft-generator-py

![preview](https://github.com/Jon-Becker/nft-generator-py/blob/main/preview.png?raw=true)

[![Unit Tests (on PR)](https://github.com/Jon-Becker/nft-generator-py/actions/workflows/tests-merged.yaml/badge.svg)](https://github.com/Jon-Becker/nft-generator-py/actions/workflows/tests-merged.yaml)

nft-generator-py is a simple script which programatically generates images using weighted layer files.

## Getting Started
Clone the repository and install the requirements.
```
git clone https://github.com/Jon-Becker/nft-generator-py
cd nft-generator-py
python3 -m pip install -r requirements.txt
```

Create a configuration file, or use the `build_configuration` command to create a configuration file from a directory of traits. For more information on configuration files, see [Configuration](#configuration).

## CLI Options
The following commands are available:
| Command               | Usage                                                                   | Description                                                                          |
| --------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `generate`            | `python3 main.py generate --config <config> [options]`                  | Generates a set of images using the provided configuration file.                     |
| `build_config` | `python3 main.py build_config --trait-dir <trait_dir> [options]` | Builds a configuration file from a directory of traits.                              |
| `validate`            | `python3 main.py validate --config <config> [options]`                  | Validates a configuration file.                                                      |
| `update_metadata`     | `python3 main.py update_metadata --image-path <config> [options]`       | Updates the metadata files for all generated images at the provided `--output` path. |

### Optional Arguments
| Argument                           | Description                                                              |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `-o <output>`, `--output <output>` | The path to the directory where the generated images will be saved.      |
| `-c <config>`, `--config <config>` | The path to the configuration file.                                      |
| `--trait-dir <trait_dir>`          | The path to the directory containing the trait images.                   |
| `-n <amount>`, `--amount <amount>` | The number of images to generate.                                        |
| `-v`, `--verbose`                  | Enables verbose logging.                                                 |
| `--start-at <start_at>`            | The number to start counting from when generating images.                |
| `--allow-duplicates`               | Allows duplicate images to be generated.                                 |
| `--no-pad`                         | Disables zero-padding of tokenIds.                                       |
| `-s <seed>`, `--seed <seed>`       | The seed to use when generating images. Allows for reproducible results. |

## Configuration
```
{
  "layers": [
    {
      "name": "Background",
      "values": ["Blue", "Orange", "Purple", "Red", "Yellow"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["blue", "orange", "purple", "red", "yellow"],
      "weights": [30, 45, 15, 5, 10]
    },
    ...
  ],
  "incompatibilities": [
    {
      "layer": "Background",
      "value": "Blue",
      "incompatible_with": ["Python Logo 2"],
      "default": {
        "value": "Default Incompatibility",
        "filename": "./trait-layers/foreground/logo"
      }
    }
  ],
  "baseURI": ".",
  "name": "NFT #",
  "description": "This is a description for this NFT series."
}
```

The `config` object is a dict that contains configuration instructions that can be changed to produce different outputs when running the program. Within metadata files, tokens are named using the configuration's `name` parameter, and described using the `description` parameter.
- In ascending order, tokenIds are appended to the `name` resulting in NFT metadata names such as NFT #0001.
- tokenIds are padded to the largest amount generated. IE, generating 999 objects will result in names NFT #001, using the above configuration, and generating 1000 objects will result in NFT #0001.
- As of `v1.0.2`, padding filenames has been removed.

The `layers` list contains `layer` objects that define the layers for the program to use when generating unique tokens. Each `layer` has a name,  which will be displayed as an attribute, values, trait_path, filename, and weights.
- `trait_path` refers to the path where the image files in `filename` can be found. Please note that filenames omit .png, and it will automatically be prepended.
- `weight` corresponds with the percent chance that the specific value that weight corresponds to will be selected when the program is run. The weights must add up to 100, or the program will fail.

The `incompatibilities` list contains an object that tells the program what layers are incompatible with what. In the above configuration, A Blue Background `layer` will *never* be generated with Python Logo 2.
- `layer` refers to the targeted layer.
- `value` is the value of the layer that is incompatible with attributes within the `incompatible_with` list.
- `incompatible_with` is the list of incompatible layers that will never be selected when `layer` has attribute `value`.
- An optional `default` object can be provided to each incompatibility. This object will be selected 100% of the time if present and an incompatible layer is selected. The `default` object has a `value` and `filename` attribute.
  - `value` is the name of the default selection which will be displayed in the metadata.
  - `filename` is the path to the image file that will be used as the default selection.

## Troubleshooting
- All images should be in .png format.
- All images should be the same size in pixels, IE: 1000x1000.
- The weight values for each attribute should add up to equal 100.

## Contributing
Before contributing, make a new branch with the following format:

```
user/{username}/{description}
```

Your names should be descriptive of the changes you are making. For example, if you are adding a new command, your branch name might be `user/jon-becker/some-new-command`.

Your code will be reviewed and require at least one approval before being merged into the `main` branch.

Please follow [this guide](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/) when writing commit messages. Messages should be descriptive and clean.
