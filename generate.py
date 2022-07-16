from collections import Counter
from PIL import Image
import argparse
import random
import json
import os

from lib.util.io import loadJSON, pathExists

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    # check for incompatibilities
    for incomp in config["incompatibilities"]:
      for attr in new_image:
        if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
          
          # if a default incompatibility value is set, use it instead
          if "default" in incomp:
            new_image[attr] = incomp["default"]["value"]
          else:
            return create_new_image(all_images, config)

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount))
  trait_files = {}
  
  # build trait dict
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x]
    
  for incomp in config["incompatibilities"]:
    if "default" in incomp:
      for layer in trait_files:
        trait_files[layer][incomp["default"]["value"]] = incomp["default"]["filename"]
        
  # generate n unique images
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 1
  for item in all_images:
      item["tokenId"] = i
      i += 1

  # dump unique images
  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": config["baseURI"] + "/images/" + str(token["tokenId"]) + '.png',
        "tokenId": token["tokenId"],
        "name":  config["name"] + str(token["tokenId"]).zfill(pad_amount),
        "description": config["description"],
        "attributes": attributes
    }
    with open('./metadata/' + str(token["tokenId"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = []
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        
        if "/" in trait_files[attr][item[attr]]:
          layers[index] = Image.open(f'{trait_files[attr][item[attr]]}.png').convert('RGBA')
        else:
          layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGBA')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGBA')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGBA')
      file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/" + file_name)
  
  all_token_rarity = []
  for layer in config["layers"]:
    all_token_rarity.append({ layer["name"]: Counter(image[layer["name"]] for image in all_images) })

  with open('./metadata/all-rarity.json', 'w') as outfile:
    json.dump(all_token_rarity, outfile, indent=4)

  
  # v1.0.2 addition
  print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "ipfs://{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)



#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)


generator = argparse.ArgumentParser(prog='generate', usage='generate.py [options]')

generator.add_argument('-n', '--amount', help="Amount to generate")
generator.add_argument('-c', '--config', help="Path to configuration file")

args = generator.parse_args()

if args.amount and args.config:
  if pathExists(args.config):
    generate_unique_images(int(args.amount), loadJSON(args.config))
  else:
    print('generator: error: Configuration file specified doesn\'t exist.\n')

else:
  print('generator: error: Missing a mandatory option (-n or -c). Use -h to show the help menu.\n')
#generate_unique_images(args.amo, )
