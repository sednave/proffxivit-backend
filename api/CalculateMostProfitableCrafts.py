MAX_API_REQUESTS_PER_INTERVAL = 8
INTERVAL_IN_MILLISECONDS = 1000
TOP_N_TO_KEEP = 10

import asyncio
from ItemDataUtility import ItemDataUtility
from GetItemProfit import GetItemProfit

mostProfitable = []

def GetMostProfitableCrafts():
    return "Hello world!"

def split_list(lst, n):
    """Splits a list into sublists of size n."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]

async def CalculateProfitableCraftsHelper(topN, subList):
    global mostProfitable

    apiRequestLists = split_list(subList, MAX_API_REQUESTS_PER_INTERVAL)

    for apiRequestList in apiRequestLists:
        try:
            tasks = []
            for recipeId in apiRequestList:
                tasks.append(GetItemProfit(recipeId))
            values = await asyncio.gather(*tasks)
            for value in values:
                finalItemId = value["finalItemId"]
                profit = value["profit"]

                foundIndex = -1
                for i, (id, _) in enumerate(mostProfitable):
                    if id == finalItemId:
                        foundIndex = i
                        break
                if foundIndex >= 0:
                    mostProfitable[foundIndex] = (finalItemId, profit)
                else:
                    mostProfitable.append((finalItemId, profit))
            mostProfitable.sort(key=lambda x: x[1], reverse=True)
            mostProfitable = mostProfitable[:10]
        except:
            continue


def StartCalculatingMostProfitableCrafts():
    asyncio.run(CalculateProfitableCraftsHelper(TOP_N_TO_KEEP, ItemDataUtility.GetAllRecipeIds()))