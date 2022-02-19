import json


with open("csgo.json", "r") as offsets_file:
    offset_list = json.loads(offsets_file.read())
