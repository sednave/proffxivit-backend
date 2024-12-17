import json

class ItemDataUtility:
    namesToIds = {} # <string, int>
    idsToNames = {} # <int, string>
    recipes = {}
    initialized = False

    def __init__(self):
        with open("item_ids.json", "r") as f:
            ItemDataUtility.idsToNames = json.load(f)
        ItemDataUtility.namesToIds = {}
        for id in ItemDataUtility.idsToNames:
            name = ItemDataUtility.idsToNames[id]
            ItemDataUtility.namesToIds[name] = id
        
        with open("recipes.json", "r") as f:
            ItemDataUtility.recipes = json.load(f)
        
        ItemDataUtility.initialized = True

    @staticmethod
    def ValidId(id):
        return str(id) in ItemDataUtility.idsToNames

    @staticmethod
    def ValidName(name):
        return name in ItemDataUtility.namesToIds

    @staticmethod
    def GetNameFromId(id):
        if (not ItemDataUtility.initialized):
            ItemDataUtility()
        return ItemDataUtility.idsToNames[str(id)]

    @staticmethod
    def GetIdFromName(name):
        if not ItemDataUtility.initialized:
            ItemDataUtility()
        return ItemDataUtility.namesToIds[name]

    @staticmethod
    def GetAllItemIds():
        if not ItemDataUtility.initialized:
            ItemDataUtility()
        return list(ItemDataUtility.idsToNames.keys())

    @staticmethod
    def GetRecipe(id):
        if not ItemDataUtility.initialized:
            ItemDataUtility()
        return ItemDataUtility.recipes[str(id)] if str(id) in ItemDataUtility.recipes else None 

    @staticmethod
    def GetAllRecipeIds():
        if not ItemDataUtility.initialized:
            ItemDataUtility()
        return list(ItemDataUtility.recipes.keys())