# handles the loading of commands
import os
import datetime

commandPath = "commands"

async def loadCommands(client, tree):
    print("Loading commands...")

    for file in os.listdir(commandPath):
        if file.endswith(".py"):
            start = datetime.datetime.now()
            f = __import__(commandPath + "." + file[:-3], fromlist = ["loadCommands"])

            await f.loadCommands(client, tree)

            print("Loaded " + file + " in " + str(datetime.datetime.now() - start) + " seconds.")
            

    

    

    