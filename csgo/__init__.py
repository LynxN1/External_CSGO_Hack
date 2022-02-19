import requests
import json


res = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json").json()
with open("csgo.json", "w") as offsets_file:
    json.dump(res, offsets_file, indent=2)
    print("Offsets are loaded")
