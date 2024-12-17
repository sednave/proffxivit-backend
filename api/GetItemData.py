from ItemDataUtility import ItemDataUtility
import requests
import json
import datetime

itemData = {}
itemRequestTimestamps = {}


def ItemDataValid(id):
    if id in itemData:
        if id in itemRequestTimestamps:
            difference = abs(itemRequestTimestamps[id] - datetime.datetime.now)
            if difference < datetime.timedelta(minutes=5):
                return True
    return False


def GetItemData(id):
    if ItemDataValid(id):
        return itemData[id]

    worldId = 53 # Exodus
    domain = "https://universalis.app/"

    recipe = ItemDataUtility.GetRecipe(id)
    queryItems = [id];
    if not recipe is None:
        queryItems = queryItems + list(map(lambda r: r["id"], recipe))
    endpoint = f"{domain}/api/v2/aggregated/{worldId}/{",".join(str(id) for id in queryItems)}"

    res = requests.get(endpoint)
    data = json.loads(res.text)
    itemData[id] = data["results"][0]
    itemRequestTimestamps[id] = datetime.datetime.now

    for i in range(1, len(data["results"])):
        itemId = queryItems[i]
        itemData[itemId] = data["results"][i]
        itemRequestTimestamps[itemId] = datetime.datetime.now
    
    return itemData[id]