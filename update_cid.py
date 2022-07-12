import json

f = open('./metadata/all-objects.json')
all_images = json.load(f)

cid = input("IPFS Image CID (): ")
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