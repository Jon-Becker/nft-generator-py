import os
import json
from collections import Counter
from PIL import Image
import random
import json
import os

#Additional layer objects can be added following the formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)



class NFTGenerator:
    def __init__(self, config:str=None, amount:int=0):
        self.config = config
        self.amount = amount

    def __pathExists(self,dirPath):
        return os.path.exists(dirPath)

    def __loadJSON(self, path):
        with open(path) as pathFile:
            contents = json.loads("".join(pathFile.readlines()))
        return contents

    def __create_new_image(self, all_images):
        new_image = {}
        for layer in self.config["layers"]:
            new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
        
        # check for incompatibilities
        for incomp in self.config["incompatibilities"]:
            for attr in new_image:
                if new_image[incomp["layer"]] == incomp["value"] and new_image[attr] in incomp["incompatible_with"]:
                
                    # if a default incompatibility value is set, use it instead
                    if "default" in incomp:
                        new_image[attr] = incomp["default"]["value"]
                    else:
                        return self.__create_new_image(all_images, self.config)

        if new_image in all_images:
            return self.__create_new_image(all_images, self.config)
        else:
            return new_image

    def generate_unique_images(self):
        print("Generating {} unique NFTs...".format(self.amount))
        pad_amount = len(str(self.amount))
        trait_files = {}
        
        # build trait dict
        for trait in self.config["layers"]:
            trait_files[trait["name"]] = {}
            for x, key in enumerate(trait["values"]):
                trait_files[trait["name"]][key] = trait["filename"][x]
            
        for incomp in self.config["incompatibilities"]:
            if "default" in incomp:
                for layer in trait_files:
                    trait_files[layer][incomp["default"]["value"]] = incomp["default"]["filename"]
                    
        # generate n unique images
        all_images = []
        for i in range(self.amount): 
            new_trait_image = self.__create_new_image(all_images, self.config)
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
                "image": self.config["baseURI"] + "/images/" + str(token["tokenId"]) + '.png',
                "tokenId": token["tokenId"],
                "name":  self.config["name"] + str(token["tokenId"]).zfill(pad_amount),
                "description": self.config["description"],
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
                        layers[index] = Image.open(f'{self.config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

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
        for layer in self.config["layers"]:
            all_token_rarity.append({ layer["name"]: Counter(image[layer["name"]] for image in all_images) })

        with open('./metadata/all-rarity.json', 'w') as outfile:
            json.dump(all_token_rarity, outfile, indent=4)
        print("\nUnique NFT's generated.")

        if self.config["uploadToIPFS"]:
            print("\nUploading to IPFS.")
            return self.__uploadToIPFS(all_images)

    def __uploadToIPFS(self, all_images):        
        # upload to IPFS
        print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
        cid = self.config['cid']
        if len(cid) > 0:
            if not cid.startswith("ipfs://"):
                cid = "ipfs://{}".format(cid)
            if cid.endswith("/"):
                cid = cid[:-1]
            for i, item in enumerate(all_images):
                with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
                    original_json = json.loads(infile.read())
                    original_json["image"] = original_json["image"].replace(self.config["baseURI"]+"/", cid+"/")
                    with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
                        json.dump(original_json, outfile, indent=4)

    def update_cid(self):
        #updates the CID in the metadata files
        f = open('./metadata/all-objects.json')
        all_images = json.load(f)

        cid = self.config['cid']
        if len(cid) > 0:
            if not cid.startswith("ipfs://"):
                cid = "ipfs://{}".format(cid)
            if cid.endswith("/"):
                cid = cid[:-1]
            for i, item in enumerate(all_images):
                with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
                    original_json = json.loads(infile.read())
                    original_json["image"] = original_json["image"] = f'{cid}/{str(item["tokenId"])}.png'
                    with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
                        json.dump(original_json, outfile, indent=4)

    def generate_config(self):
        # generates the config.json file with balanced rarities, script should be placed in the main directory.
        layerlist = os.listdir("./trait-layers")
        url_list = []
        item_list = []
        weight = []

        for items in layerlist:
            url_list.append("./trait-layers" + "/" + items)
        for items in url_list:
            item_list.append(os.listdir(items))
        for i in range(len(item_list)):
            weight.append(100/len(item_list[i]))
            for j in range(len(item_list[i])):
                if ".png" in item_list[i][j]:
                    item_list[i][j] = item_list[i][j][:-4]
        weightlist = []*len(layerlist)

        for i in range(len(weight)):
            x = 100/weight[i]
            temp1 = []
            for y in range(int(x)):
                temp1.append(weight[i])
            weightlist.append(temp1)
        print(weightlist)

        finstr = ""
        jsonstringarray = []
        jsonstring = ""
        for x in range(len(layerlist)):
            jsonstring = '{"name": "' + layerlist[x] + '", "values": ' + str(item_list[x]) + ', "trait_path": "' + url_list[x] + '", "filename": ' + str(item_list[x]) + ', "weights": ' + str(weightlist[x]) + '}'
            jsonstringarray.append(jsonstring.replace("'",'"'))

        finstr = str(jsonstringarray).replace("'", "")

        jsondict = {"layers":finstr, "incompatibilities":[], "baseURI": "ipfs://xxxx/", "name": "Item #", "description": "description here please"}
        finstr2 = str(jsondict).replace("'",'"')
        finstr2 = finstr2.replace('"layers": "', '"layers": ')
        finstr2 = finstr2.replace('", "incompatibilities"', ', "incompatibilities"')
        jsondump = json.loads(finstr2)
        print(jsondump)
        print("adding config to directory and configuring generator")
        self.config = jsondump
        with open('config.json', 'w') as outfile:
            json.dump(jsondump, outfile)

    def start_generating(self):
        if self.amount and self.config:
            if self.__pathExists(self.config):
                self.generate_unique_images(int(self.amount), self.__loadJSON(self.config))
            else:
                print('generator: error: Configuration file specified doesn\'t exist.\n')

        else:
            print('generator: error: Missing a mandatory option (-n or -c). Use -h to show the help menu.\n')

