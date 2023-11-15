# Handles the data management for the application.
# This includes the loading and saving of data.
# Each user has their own data file.

import os
import json
import emoji as emo
from reactions import calculate_rarity
from reactions import reactions as reactionList
import reactions
from settings import settingsTable as settings
from concurrent.futures import ThreadPoolExecutor

def get_user_data(user_id):
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/" + user_id + ".json"):
        return None
    with open("data/" + user_id + ".json", "r") as file:
        return json.load(file)

def save_user_data(user_id, key, value):
    data = get_user_data(user_id)
    if data == None:
        create_user(user_id)
        data = get_user_data(user_id)

    data[key] = value

    with open("data/" + user_id + ".json", "w") as file:
        json.dump(data, file) 

    return value

def add_user_data(user_id, key, value):
    data = get_user_data(user_id)
    if data == None:
        create_user(user_id)
        data = get_user_data(user_id)

    if key not in data:
        print("Attempted to add data to user that does not exist.")
        return
    
    if settings["doubleCredits"]:
        value = value * 2
    
    data[key] += value

    with open("data/" + user_id + ".json", "w") as file:
        json.dump(data, file) 

    return value

def obtained_reactions(user_id, num=None):
    data = get_user_data(user_id)
    if data == None:
        return []
    if "reactions" not in data:
        return []
    if num == None:
        return data["reactions"]
    
    return data["reactions"][:num]


def add_reaction(user_id, reaction):
    reactions = obtained_reactions(user_id)
    if reaction not in reactions:
        reactions.append(reaction)
    else:
        print("Attempted to add reaction that was already obtained.")

    save_user_data(user_id, "reactions", reactions)

def remove_reaction(user_id, reaction):
    reactions = obtained_reactions(user_id)
    if reaction in reactions:
        reactions.remove(reaction)
    save_user_data(user_id, "reactions", reactions)

def make_superuser(user_id):
    save_user_data(user_id, "superuser", True)

def create_user(user_id):
    if not os.path.exists("data"):
        os.makedirs("data")
    if os.path.exists("data/" + user_id + ".json"):
        print("Attempted to create user that already exists.")
        return
    with open("data/" + user_id + ".json", "w") as file:
        json.dump({"reactions": [], "credits": 0, "superuser": False, "lastDaily": "meow", "lastReactionTime": None, "name": "unknown"}, file)

def user_exists(user_id):
    if not os.path.exists("data"):
        os.makedirs("data")
    return os.path.exists("data/" + str(user_id) + ".json")

def data_wipe(user_id):
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/" + user_id + ".json"):
        print("Attempted to wipe data for user that does not exist.")
        return
    os.remove("data/" + user_id + ".json")

def name_from_id(user_id):
    data = get_user_data(user_id)
    if data == None:
        return "unknown"
    return data["name"]

def data_wipe_all():
    if not os.path.exists("data"):
        os.makedirs("data")
    for file in os.listdir("data"):
        with open("data/" + file, "w") as f:
            json.dump({"reactions": [], "credits": 0, "superuser": False, "lastDaily": "meow", "lastReactionTime": None, "name": "unknown"}, f)


def process_file(file):
    with open(f"data/{file}", "r") as f:
        data = json.load(f)
    return file[:-5], data

validSorts = {"credits", "reactions"}

def construct_leaderboard(sorting):
    if sorting not in validSorts:
        print("Invalid sorting method.")
        return

    leaderboard = []

    with ThreadPoolExecutor() as executor:
        files = os.listdir("data")
        results = list(executor.map(process_file, files))

    for file, data in results:
        if sorting == "credits":
            value = data.get(sorting, 0)
        elif sorting == "reactions":
            value = len(data.get(sorting, []))
        leaderboard.append((file, value))

    leaderboard.sort(key=lambda x: x[1], reverse=True)
    
    return leaderboard, sorting

inf = float("inf")

def highest_rarityemoji(user_id):
    reactions = obtained_reactions(user_id)
    # by highest we mean MOST RARE, so lower percentage
    highest = inf
    highest_reaction = None

    for reaction in reactions:
        _, percentage = calculate_rarity(reaction)
        # is this percentage lower than the current highest?
        if percentage < highest:
            highest = percentage
            highest_reaction = reaction
        
    if highest == inf:
        return None
    
    return highest_reaction

def has_reaction(user_id, reaction):
    reactions = obtained_reactions(user_id)
    return reaction in reactions

async def sync_usernames(Client):
    for file in os.listdir("data"):
        user_id = file[:-5]
        user = await Client.fetch_user(user_id)
        if user == None:
            continue
        save_user_data(user_id, "name", user.name)


def total_saved_users():
    return len(os.listdir("data"))

def calculate_inventory_value(user_id):
    reactions2 = obtained_reactions(user_id)
    doubleCredits = settings["doubleCredits"]
    value = 0

    # indexMultiplier = reaction.reactions.len() / 100 * 1.5 # sell price
    indexMultiplier = len(reactionList) / 100 * 1.5 # sell price

    for reaction in reactions2:
        index = reactions.get_reaction_index(reaction)

        if index == 0:
            index += 1

        value += index * indexMultiplier

    if doubleCredits:
        print("Double credits is active, doubling inventory value.")
        value = value * 2

    return value


