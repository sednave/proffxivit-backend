from .ItemDataUtility import ItemDataUtility
import requests
import json

def GetItemPrice(itemData, quality):
    if not type(itemData) is dict:
        return -1

    if not quality in itemData \
            or itemData[quality] is None \
            or itemData[quality]["averageSalePrice"] is None:
        return -1

    averageSalePriceData = itemData[quality]["averageSalePrice"]
    if "world" in averageSalePriceData:
        return averageSalePriceData["world"]["price"]
    elif "dc" in averageSalePriceData:
        return averageSalePriceData["dc"]["price"]
    elif "region" in averageSalePriceData:
        return averageSalePriceData["region"]["price"]
    return -1

def GetHqPrice(itemData):
    return GetItemPrice(itemData, "hq")

def GetNqPrice(itemData):
    return GetItemPrice(itemData, "nq")


async def GetItemProfit(finalItemId):
    worldId = 53 # Exodus
    domain = "https://universalis.app/"

    recipe = ItemDataUtility.GetRecipe(finalItemId)
    queryItems = [finalItemId];
    if not recipe is None:
        queryItems = queryItems + list(map(lambda r: r["id"], recipe))
    endpoint = f"{domain}/api/v2/aggregated/{worldId}/{','.join(str(id) for id in queryItems)}"

    res = requests.get(endpoint)
    data = json.loads(res.text)
    itemData = data["results"]
    finalItemData = itemData[0]
    finalItemPrice = GetHqPrice(finalItemData)
    if finalItemPrice == -1:
        finalItemPrice = GetNqPrice(finalItemPrice)

    recipePrices = {}
    for i in range(1, len(itemData)):
        itemId = queryItems[i]
        itemRecord = itemData[i]
        itemPrice = GetHqPrice(itemRecord)
        if itemPrice == -1:
            itemPrice = GetNqPrice(itemRecord)
        recipePrices[itemId] = itemPrice

    totalMaterialsPrice = 0

    recipeItems = {} 
    if not recipe is None:
        for recipeItem in recipe:
            totalMaterialsPrice += float(recipePrices[recipeItem["id"]]) * int(recipeItem["count"])

    for recipeItem in recipe:
        itemId = int(recipeItem["id"])
        recipeItems[itemId] = {
            "itemId": itemId,
            "count": int(recipeItem["count"]),
            "averagePrice": float(recipePrices[itemId])
        }
    

    retValue = {
        "finalItemId": finalItemId,
        "finalItemPrice": finalItemPrice,
        "profit": finalItemPrice - totalMaterialsPrice,
        "recipeItems": recipeItems
    }

    return retValue