import os
import json
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
with open('config_CHECKandRENAME.json', 'w') as outfile:
    json.dump(jsondump, outfile)
