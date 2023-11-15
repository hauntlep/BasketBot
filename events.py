import asyncio
import random
import datetime
import dataManager as dm
from settings import settingsTable as settings

lastRandomEvent = "2021-09-28 00:00:00.000000"
randomEventTypes = ["doubleCredits", "doubleCoinflip", "phraseType"]
randomEventPhrases = [
    "apple",
    "banana",
    "cherry",
    "durian",
    "eggplant",
    "fig",
    "grape",
    "vaderhaxx",
    "bloxsense",
    "evelyn is so cute and cool",
    "everytime i try to be friends with IN TAH GER",
    "fatally bad discord bot",
]

async def disableDoubleCredits(message):
    await asyncio.sleep(settings["doubleCreditTime"])
    settings["doubleCredits"] = False
    await message.channel.send("Double credits are no longer active.")

async def disableDoubleCoinflip(message):
    await asyncio.sleep(settings["doubleCoinflipTime"])
    settings["doubleCoinFlip"] = False
    await message.channel.send("Double coinflip is no longer active.")

# afunction that, given seconds, returns a string of the format "x hours, y minutes, z seconds"
def secondsToTime(seconds):
    hours = int(seconds / 3600)
    seconds = seconds % 3600
    minutes = int(seconds / 60)
    seconds = seconds % 60

    return str(hours) + " hours, " + str(minutes) + " minutes, and " + str(seconds) + " seconds"

async def doubleCredits(message):
    global lastRandomEvent
    if datetime.datetime.now() - datetime.datetime.strptime(str(lastRandomEvent), "%Y-%m-%d %H:%M:%S.%f") > datetime.timedelta(minutes=random.randint(10, 20)):
        lastRandomEvent = str(datetime.datetime.now())
        
        settings["doubleCredits"] = True

        await message.channel.send("Double credits are now active for the next " + secondsToTime(settings["doubleCreditTime"]) + "!")

        #create a task to disable double credits after 5 minutes that will not interrupt the main thread
        asyncio.create_task(disableDoubleCredits(message))

async def doubleCoinflip(message):
    global lastRandomEvent
    if datetime.datetime.now() - datetime.datetime.strptime(str(lastRandomEvent), "%Y-%m-%d %H:%M:%S.%f") > datetime.timedelta(minutes=random.randint(10, 20)):
        lastRandomEvent = str(datetime.datetime.now())
        
        settings["doubleCoinFlip"] = True

        await message.channel.send("Double coinflip is now active for the next " + secondsToTime(settings["doubleCoinflipTime"]) + "!")

        #create a task to disable double credits after 5 minutes that will not interrupt the main thread
        asyncio.create_task(disableDoubleCoinflip(message))

async def phraseType(message):
    global lastRandomEvent
    if datetime.datetime.now() - datetime.datetime.strptime(str(lastRandomEvent), "%Y-%m-%d %H:%M:%S.%f") > datetime.timedelta(minutes=random.randint(10, 20)):
        lastRandomEvent = str(datetime.datetime.now())
        
        settings["phraseType"] = random.choice(randomEventPhrases)

        await message.channel.send("Say the phrase " + settings["phraseType"] + " to get " + str(settings["phraseTypeCredits"]) + " credits!")

async def random_event(message):
    event = random.choice(randomEventTypes)

    if event == "doubleCredits":
        await doubleCredits(message)
    elif event == "doubleCoinflip":
        await doubleCoinflip(message)
    elif event == "phraseType":
        await phraseType(message)
