import json
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

class ItemDataUtility:
    namesToIds = {} # <string, int>
    idsToNames = {} # <int, string>
    recipes = {}
    initialized = False

    def __init__(self):
        item_ids_file_path = path.join(BASE_DIR, "item_ids.json")
        with open(item_ids_file_path, "r") as f:
            ItemDataUtility.idsToNames = json.load(f)
        ItemDataUtility.namesToIds = {}
        for id in ItemDataUtility.idsToNames:
            name = ItemDataUtility.idsToNames[id]
            ItemDataUtility.namesToIds[name] = id
        
        recipes_file_path = path.join(BASE_DIR, "recipes.json")
        with open(recipes_file_path, "r") as f:
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