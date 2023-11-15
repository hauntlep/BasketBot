
import discord
import dataManager as dm
from reactions import calculate_rarity as rarity
from reactions import reactions as reactionList
import reactions as rea
import emoji as emo
import datetime
from settings import settingsTable as settings

from discord.ui import View
from discord.ui import Button
from discord import ButtonStyle

sellPrice = len(reactionList) / 150 * 1.05 # sell price
buyPrice = len(reactionList) / 100 * 25 # buy price

async def loadCommands(client, tree):
    @tree.command(name = "rarity", description = "Check the rarity of a reaction")
    async def checkRarity(ctx, reaction: str):
        reaction = emo.demojize(reaction, language="alias")
        if reaction not in reactionList:
            await ctx.response.send_message("That is not a valid reaction.", ephemeral=True)
            return
        chance, percentageOutOf100 = rarity(reaction)
        await ctx.response.send_message("The chance of obtaining " + reaction + " is " + str(percentageOutOf100) + "%.", ephemeral=True)


    @tree.command(name = "dataget", description = "View anyones save file")
    async def datafunc(ctx, user: discord.User, key: str):
        if not dm.user_exists(str(user.id)):
            await ctx.response.send_message("That user does not have a save file.", ephemeral=True)
            return
        
        data = dm.get_user_data(str(user.id))

        if key not in data:
            await ctx.response.send_message("That key does not exist.", ephemeral=True)
            return
        
        await ctx.response.send_message("The value of " + key + " is " + str(data[key]) + ".")

   

    @tree.command(name = "leaderboard", description="View the leaderboard")
    async def leaderboard(ctx, sorting: str):
        if sorting not in ["credits", "reactions"]:
            await ctx.response.send_message("That is not a valid sorting method. Please use either 'credits' or 'reactions'.", ephemeral=True)
            return
        
        maxEntries = 10
        s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        leaderboard, method = dm.construct_leaderboard(sorting)
        print("Leaderboard construction took " + str(datetime.datetime.now() - datetime.datetime.strptime(s, "%Y-%m-%d-%H-%M-%S")) + " seconds.")

        if len(leaderboard) > maxEntries:
            leaderboard = leaderboard[:maxEntries]

        embed = discord.Embed(title="Leaderboard", description=f"Sorted by {sorting}", color=0x00ff00)

        afterValueString = " credits" if method == "credits" else "reaction(s)"
   
        nameTimeStart = datetime.datetime.now()

        names = []

        # construct names list
        for entry in leaderboard:
            names.append(dm.name_from_id(entry[0]))
        
        print("Name iteration took " + str(datetime.datetime.now() - nameTimeStart) + " seconds.")
        
        mainIterTimeStart = datetime.datetime.now()
        for i, entry in enumerate(leaderboard):
            name = dm.name_from_id(entry[0])

            # Determine the highest rarity emoji
            highestRarityEmoji = dm.highest_rarityemoji(entry[0])
            highestRarityEmoji = "No Emojis!" if highestRarityEmoji is None else emo.demojize(highestRarityEmoji, language="alias")

            # Get the value
            value = entry[1]

            # Create the value string
            valueString = f"{value} {afterValueString}; Highest rarity reaction: {highestRarityEmoji}"

            # Add the field to the embed
            embed.add_field(name=name, value=valueString, inline=False)

        print("Main iteration took " + str(datetime.datetime.now() - mainIterTimeStart) + " seconds.")

        await ctx.response.send_message(embed=embed, ephemeral=True)


    @tree.command(name = "list", description="Lists all reactions")
    async def list(ctx):
        embed = discord.Embed(title="Reactions", description="List of all reactions", color=0x00ff00)

        view = View()

        # split into pages of 10
        pages = []

        for i in range(0, len(reactionList), 10):
            page = reactionList[i:i+10]
            pages.append(page)

        if len(pages) == 1:
            embed.clear_fields()
            for reaction in pages[0]:
                embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * sellPrice, 2)) + " credits", inline=False)
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return
        
        next = Button(style=ButtonStyle.green, label="Next")
        previous = Button(style=ButtonStyle.green, label="Previous")

        buttons = [previous, next]

        current_page = 0

        for reaction in pages[current_page]:
            embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * sellPrice, 2)) + " credits", inline=False)

        # button callbacks

        async def next_callback(interaction):
            nonlocal current_page
            current_page += 1
            if current_page >= len(pages):
                current_page = 0
            embed.clear_fields()
            for reaction in pages[current_page]:
                embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * sellPrice, 2)) + " credits", inline=False)
            
            await interaction.response.edit_message(embed=embed)

        async def previous_callback(interaction):
            nonlocal current_page
            current_page -= 1
            if current_page < 0:
                current_page = len(pages) - 1
            embed.clear_fields()
            for reaction in pages[current_page]:
                embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * sellPrice, 2)) + " credits", inline=False)
            await interaction.response.edit_message(embed=embed)

        next.callback = next_callback
        previous.callback = previous_callback

        for button in buttons:
            view.add_item(button)

        await ctx.response.send_message(embed=embed, view=view, ephemeral=True)

    @tree.command(name = "totalusers", description="View the amount of users with save files")
    async def totalusers(ctx):
        await ctx.response.send_message("There are " + str(dm.total_saved_users()) + " users with save files.")


    @tree.command(name = "ping", description = "Pong!")
    async def test(ctx):
        latency = round(client.latency * 1000)
        embed = discord.Embed(title="Pong!", description="Latency: " + str(latency) + "ms", color=0x00ff00)
        await ctx.response.send_message(embed=embed)
    # AppCommandOptionType
    def CommandOptionTypeToTypeString(type):
        
        type = str(type)[21:]

        
        type = type.lower()
       

        return type

    @tree.command(name = "help", description = "View the help menu")
    async def help(ctx):
        commands = tree.get_commands()

        embed = discord.Embed(title="Help", description="List of commands", color=0x00ff00)

        

        for command in commands:
            parametersList = []

            for parameter in command.parameters:

                parametersList.append(f"<{parameter.display_name}>, {CommandOptionTypeToTypeString(parameter.type)}")

            # if the size of the parameters list is 0, then we don't want to add a comma and instead say "No parameters"
            embed.add_field(name=command.name, value="Description: " + command.description + "\nParameters: " + (", ".join(parametersList) if len(parametersList) > 0 else "No parameters"), inline=False)


        await ctx.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name = "invite", description = "Invite the bot to your server")
    async def invite(ctx):
        # client_id=1092886690600845463&permissions=8&scope=bot
        await ctx.response.send_message("https://discord.com/api/oauth2/authorize?client_id=1092886690600845463&permissions=8&scope=bot", ephemeral=True)

    @tree.command(name = "rarest", description = "View the rarest reaction you have")
    async def rarest(ctx):
        if not dm.user_exists(ctx.user.id):
            await ctx.response.send_message("You do not have a save file.", ephemeral=True)
            return
        reaction = dm.highest_rarityemoji(str(ctx.user.id))
        if reaction is None:
            await ctx.response.send_message("You do not have any reactions.", ephemeral=True)
            return
        await ctx.response.send_message("Your rarest reaction is " + emo.demojize(reaction, language="alias") + " with a rarity of " + str(rarity(reaction)[1]) + "%.", ephemeral=True)
    
    @tree.command(name = "top10", description = "View the top 10 rarest OVERALL reactions")
    async def top10(ctx):
        __, top10 = rea.rarest_reaction()

        embed = discord.Embed(title="Top 10", description="Top 10 rarest reactions", color=0x00ff00)

        for i, reaction in enumerate(top10):
            # if i is 0, 1, 2 then we want corresponding medals
            indexInList = rea.get_reaction_index(reaction[0])
            if i < 3:
                if i == 0:
                    medal = ":first_place:"
                elif i == 1:
                    medal = ":second_place:"
                else:
                    medal = ":third_place:"
            else:
                medal = ""

            embed.add_field(name=medal + " " + emo.demojize(reaction[0], language="alias"), value="Percentage: " + str(reaction[1]) + "%\nIndex: " + str(indexInList), inline=False)

        
        await ctx.response.send_message(embed=embed, ephemeral=True)
