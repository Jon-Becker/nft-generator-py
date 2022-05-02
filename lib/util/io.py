import os
import json

def pathExists(dirPath):
  return os.path.exists(dirPath)

def loadJSON(path):
  with open(path) as pathFile:
    contents = json.loads("".join(pathFile.readlines()))
  return contents