
# nft-generator-py

![preview](https://github.com/Jon-Becker/nft-generator-py/blob/main/preview.png?raw=true)

nft-generator-py is a python based NFT generator which programatically generates unique images using weighted layer files. The program is simple to use, and new layers can  be added by adding a new layer object and adding names, weights, and image files to the object.
You can [View The Demo](https://jbecker.dev/demos/nft-generator-py) here.


## How it works
- A call to `generate_unique_images(amount, config)` is made, which is the meat of the application where all the processing happens.
- The `config` object is read and for each object in the `layers` list, random values are selected and checked for uniqueness against all previously generated metadata files.
- Once we have `amount` unique tokens created, we layer them against eachother and output them and their metadata to their respective folders, `./metadata` and `./images`.

### Configuration
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
      "incompatible_with": ["Python Logo 2"]
    },
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

As of `v1.0.2`, the IPFS CID may be updated programatically after generating NFTs and uploading `/images` to IPFS. This will update all metadata files to correctly point `"image"` to the IPFS CID.
- *This is an optional step, and can be exited safely using `enter` or `control + c`.*

#### Troubleshooting
- All images should be in .png format.
- All images should be the same size in pixels, IE: 1000x1000.
- The weight values for each attribute should add up to equal 100.

### Credits
This project is completely coded by [Jonathan Becker](https://jbecker.dev), using no external libraries.

