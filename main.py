import discord
from discord import app_commands
import dataManager as dm
from commandsF import loadCommands
from reactions import get_reaction as rarity
from reactions import calculate_rarity as percentage
from reactions import reactions as reactionList
import emoji as em
import datetime
from settings import settingsTable as settings
import random
import events
from environmentfile import dotenv

dm.create_user("1024467790557610085")
dm.make_superuser("1024467790557610085")

BaseIntents = discord.Intents.default()
BaseIntents.members = True
BaseIntents.message_content = True
BaseIntents.messages = True

BOT = {
    "TOKEN": dotenv["TOKEN"],
    "CLIENT": discord.Client(intents=BaseIntents),
}

Client = BOT["CLIENT"]

Tree = app_commands.CommandTree(Client)

@Client.event
async def on_ready():
    await loadCommands(Client, Tree)

    await dm.sync_usernames(Client)

    await Tree.sync()

    print("Bot is ready.")


@Client.event
async def on_message(message):
    global lastRandomEvent

    

    # if this server doesnt have a "basket-botter" role, create it
    if message.guild != None and discord.utils.get(message.guild.roles, name="basket-botter") == None:
        await message.guild.create_role(name="basket-botter")

    lastRandomEvent = events.lastRandomEvent

    if message.author == Client.user:
        return

    # does this person have a save file?
    userId = str(message.author.id)
    if not dm.user_exists(userId):
        return
    
    dm.save_user_data(userId, "name", message.author.name)

    # if this person does not have the basket-botter role, give it to them
    if message.guild != None and discord.utils.get(message.author.roles, name="basket-botter") == None:
        await message.author.add_roles(discord.utils.get(message.guild.roles, name="basket-botter"))

    if settings['phraseType'] != None:
        if message.content.lower() == settings['phraseType'].lower():
            await message.channel.send("Congratulations, <@" + userId + ">! You have typed the phrase correctly! You have been awarded " + str(settings['phraseTypeCredits']) + " credits.")

            settings['phraseType'] = None

            dm.add_user_data(userId, "credits", settings['phraseTypeCredits'])
            return
    
    # is this a random event?
    if settings["randomEvents"]:
        if datetime.datetime.now() - datetime.datetime.strptime(lastRandomEvent, "%Y-%m-%d %H:%M:%S.%f") > datetime.timedelta(minutes=random.randint(10, 20)):
            await events.random_event(message)

    
    # do we get a reaction?
    reaction, emoji, chance = rarity()
    if reaction:
        if dm.has_reaction(userId, emoji):
            creditsToAdd = reactionList.index(emoji)
            # if the index is 0, we add 1 to the index
            if creditsToAdd == 0:
                creditsToAdd += 1

            creditsToAdd = creditsToAdd * 2.5
            print("Reaction obtained: " + emoji + " by " + message.author.name + " (duplicate), accrediting " + str(creditsToAdd) + " credits.")
            dm.save_user_data(userId, "credits", dm.get_user_data(userId)["credits"] + creditsToAdd)
            await message.add_reaction(em.emojize(emoji, language="alias"))
            await message.channel.send("<@" + userId + "> has obtained a duplicate reaction! They have been accredited " + str(creditsToAdd) + " credits.")
            return
        
        __, percentageValue = percentage(emoji)
        
        dm.add_reaction(userId, emoji)
        
        if percentageValue <= 10:
            await message.channel.send("<@" + userId + "> has obtained a rare reaction! They have been accredited " + str(percentageValue) + " credits.")
            dm.add_user_data(userId, "credits", percentageValue)
        elif percentageValue <= 5:
            await message.channel.send("WOW! <@" + userId + "> has obtained a super rare reaction! They have been accredited " + str(percentageValue^2 * 2) + " credits.")
            dm.add_user_data(userId, "credits", percentageValue^2 * 2)
        elif percentageValue <= 2:
            await message.channel.send("OH MY GOD! <@" + userId + "> has obtained a legendary reaction! They have been accredited " + str(percentageValue^3 * 3) + " credits.")
            dm.add_user_data(userId, "credits", percentageValue^3 * 3)

        await message.add_reaction(em.emojize(emoji, language="alias"))

        dm.save_user_data(userId, "lastReactionTime", str(message.created_at))


Client.run(BOT["TOKEN"])
