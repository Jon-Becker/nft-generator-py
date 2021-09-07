from IPython.display import display 
from PIL import Image
import random
import json

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    if new_image in all_images:
        return create_new_image(all_images, config)
    else:
        return new_image

def generate_unique_images(amount, config):
  pad_amount = len(str(amount));
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x];
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 0
  for item in all_images:
      item["tokenId"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": "./images/" + str(i).zfill(pad_amount) + '.png',
        "tokenId": i,
        "name":  config["name"] + str(i).zfill(pad_amount),
        "attributes": attributes
    }
    with open('./metadata/' + str(i).zfill(pad_amount) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = [];
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGB')
      file_name = str(item["tokenId"]).zfill(pad_amount) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGB')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)

generate_unique_images(5, {
  "layers": [
    {
      "name": "Background",
      "values": ["Blue", "Orange", "Purple", "Red", "Yellow"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["blue", "orange", "purple", "red", "yellow"],
      "weights": [30, 45, 15, 5, 10]
    },
    {
      "name": "Foreground",
      "values": ["Python Logo"],
      "trait_path": "./trait-layers/foreground",
      "filename": ["logo"],
      "weights": [100]
    },
    {
      "name": "Branding",
      "values": ["A Name"],
      "trait_path": "./trait-layers/text",
      "filename": ["text"],
      "weights": [100]
    }
  ],
  "name": "NFT #"
})

#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)
