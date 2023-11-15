import dataManager as dm
import discord
from discord.ui import Button
from discord import ButtonStyle
import emoji as emo
import reactions as rea

from discord.ui import View

reactionList = rea.reactions

flatRate = len(reactionList) / 150 * 1.05 # sell price
flatBuyRate = len(reactionList) * 200  # buy price

async def loadCommands(client, tree):
    @tree.command(name = "register", description = "Create a save file")
    
    async def register(ctx):
        userId = str(ctx.user.id)
        if dm.user_exists(userId):
            await ctx.response.send_message("You already have a save file!", ephemeral=True)
        else:
            dm.create_user(userId)
            await ctx.response.send_message("Save file created!", ephemeral=True)

    @tree.command(name = "wipe", description = "Wipe your save file (WARNING: THIS CANNOT BE UNDONE)")
    async def wipe(ctx):
        userId = str(ctx.user.id)
        if dm.user_exists(userId):
            dm.data_wipe(userId)
            await ctx.response.send_message("Save file wiped!", ephemeral=True)
        else:
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)

    @tree.command(name = "reactions", description = "View the reactions you have obtained")
    async def reactions(ctx):
        userId = str(ctx.user.id)
        if dm.user_exists(userId):
            reactions = dm.obtained_reactions(userId)

            if len(reactions) == 0:
                await ctx.response.send_message("You have not obtained any reactions.", ephemeral=True)
                return
            
            reactions.sort(key=lambda x: rea.get_reaction_index(x) * flatRate, reverse=True)

            embed = discord.Embed(title="Your reactions", description="You have obtained " + str(len(reactions)) + " reactions.", color=0x00ff00)
            view = View()

            pages = []

            for i in range(0, len(reactions), 10):
                page = reactions[i:i+10]
                pages.append(page)

            if len(pages) == 1:
                embed.clear_fields()
                for reaction in pages[0]:
                    embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * flatRate, 2)) + " credits", inline=False)
                await ctx.response.send_message(embed=embed, ephemeral=True)
                return
            
            next = Button(style=ButtonStyle.green, label="Next")
            previous = Button(style=ButtonStyle.green, label="Previous")

            buttons = [previous, next]

            current_page = 0

            for reaction in pages[current_page]:
                embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * flatRate, 2)) + " credits", inline=False)

            # button callbacks

            async def next_callback(interaction):
                nonlocal current_page
                current_page += 1
                if current_page >= len(pages):
                    current_page = 0
                embed.clear_fields()
                for reaction in pages[current_page]:
                    embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * flatRate, 2)) + " credits", inline=False)
                
                await interaction.response.edit_message(embed=embed)


            async def previous_callback(interaction):
                nonlocal current_page
                current_page -= 1
                if current_page < 0:
                    current_page = len(pages) - 1
                embed.clear_fields()
                for reaction in pages[current_page]:
                    embed.add_field(name=emo.demojize(reaction, language="alias"), value="Selling price: " + str(round(rea.get_reaction_index(reaction) * flatRate, 2)) + " credits", inline=False)
                await interaction.response.edit_message(embed=embed)
                

            next.callback = next_callback
            previous.callback = previous_callback

            for button in buttons:
                view.add_item(button)

            await ctx.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)

            


    @tree.command(name = "credits", description = "View your credits")
    async def credits(ctx):
        userId = str(ctx.user.id)
        if dm.user_exists(userId):
            credits = dm.get_user_data(userId)["credits"]
            await ctx.response.send_message("You have " + str(credits) + " credits.", ephemeral=True)
        else:
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)
