from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

import os
from os import path
import json


def GetFFXIVMBDataURL(item_id):
    return f"https://universalis.app/market/{item_id}"


def GetItemName(item_id):
    print(item_id)

    url_to_scrape = GetFFXIVMBDataURL(item_id)

    service = Service(executable_path="./geckodriver")
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=options)

    driver.get(url_to_scrape)

    item_name = driver.title.replace(" - Universalis", "")

    print(item_name)

    driver.quit()
    return item_name


def GetAllItemIds(start, end):
    item_ids = {}
    for i in range(start, end):
        item_name = GetItemName(i)
        if not item_name == "Failed to retrieve":
            item_ids[i] = item_name

            cwd = os.getcwd()
            item_ids_temp_file_path = path.join(cwd, f"item_ids_temp_{start}_{end}.txt")
            item_ids_file = open(item_ids_temp_file_path, "a")
            item_ids_file.write(f"{i}: {item_name}\n")
            item_ids_file.close()
    return item_ids


def WriteAllItemNames():
    cwd = os.getcwd()
    with open(path.join(cwd, "item_ids_temp.txt"), 'r') as text_file:
        text = "{\n"
        lines = text_file.readlines()
        for i, line in enumerate(lines):
            splitLine = line.strip('\n').split(": ")
            jsonLine = f"\"{splitLine[0]:}\": \"{splitLine[1]}\""
            if i < len(lines) - 1:
                text += f"    {jsonLine},\n"
            else:
                text += f"    {jsonLine}\n"
        text += "}"

        item_ids_file_path = path.join(cwd, "item_ids.json")
        item_ids_file = open(item_ids_file_path, "w")
        item_ids_file.write(text)
        item_ids_file.close()

WriteAllItemNames()