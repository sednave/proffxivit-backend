import json
from os import path
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from ItemDataUtility import ItemDataUtility


def GetItemRecipe(item_id):
    service = Service(executable_path="./geckodriver")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=options)

    garland_tools_link = f"https://www.garlandtools.org/db/#item/{item_id}"
    driver.get(garland_tools_link)

    # Wait for the <div class="block-title handle"> to be present inside <div id="main">
    try:
        wait = WebDriverWait(driver, 5)
        recipe = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "recipe")))
    except:
        driver.quit()
        return None

    materials = []
    crystals = recipe.find_element(By.CLASS_NAME, "crystals")
    crystal_list = crystals.find_elements(By.CSS_SELECTOR, "*")
    for crystal in crystal_list:
        item_id = crystal.get_attribute("data-id")
        if not item_id is None:
            item_count = crystal.get_attribute("textContent")
            item_name = crystal.find_element(
                By.TAG_NAME, "img").get_attribute("title")
            materials.append({
                "id": item_id,
                "count": item_count,
                "name": item_name,
            })

    craft_item_categories = recipe.find_elements(
        By.CLASS_NAME, "craft-category")
    for craft_item_category in craft_item_categories:
        item_lines = craft_item_category.find_elements(By.CLASS_NAME, "line")
        for item_line in item_lines:
            if not item_line is None:
                item_id = item_line.get_attribute("data-id").strip()

                text_element = item_line.find_element(By.CLASS_NAME, "text")
                if not text_element is None:
                    text = text_element.get_attribute("textContent")
                    split_text = text.split(" ", 1)
                    item_count = split_text[0].strip()
                    item_name = split_text[1].strip()
                    materials.append({
                        "id": item_id,
                        "count": item_count,
                        "name": item_name,
                    })

    driver.quit()
    return materials


def WriteItemRecipes(start, end):
    ids = ItemDataUtility.GetAllItemIds()
    for id in ids[start:end]:
        print(id)
        recipe = GetItemRecipe(id)
        if recipe is None:
            continue

        cwd = os.getcwd()
        item_ids_temp_file_path = path.join(cwd, f"recipes_{start}_{end}.txt")
        item_ids_file = open(item_ids_temp_file_path, "a")
        item_ids_file.write(f"{id}: {json.dumps(recipe)}\n")
        item_ids_file.close()

def WriteTextToJson():
    cwd = os.getcwd()
    with open(path.join(cwd, "recipes.txt"), 'r') as recipes_text_file:
        text = "{\n"
        lines = recipes_text_file.readlines()
        for i, line in enumerate(lines):
            splitLine = line.strip('\n').split(": ", 1)
            jsonLine = f"\"{splitLine[0]:}\": \"{splitLine[1].replace("\"", "\\\"")}\""
            if i < len(lines) - 1:
                text += f"    {jsonLine},\n"
            else:
                text += f"    {jsonLine}\n"
        text += "}"

        asJson = json.loads(text)
        newJson = {}
        for key in list(asJson.keys()):
            recipeArray = json.loads(asJson[key])
            newRecipeArray = []

            for recipe in recipeArray:
                newRecipeArray.append({
                    "id": int(recipe["id"]),
                    "count": int(recipe["count"])
                })
            
            newJson[int(key)] = newRecipeArray

        recipes_json_file_path = path.join(cwd, "recipes.json")
        recipes_file = open(recipes_json_file_path, "w")
        recipes_file.write(json.dumps(newJson, indent=4))
        recipes_file.close()

WriteTextToJson()