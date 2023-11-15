import emoji as emo
import dataManager as dm
from settings import settingsTable as settings
from reactions import reactions as reactionList
import random
import datetime


flatRate = len(reactionList) / 150 * 1.05 # sell price
flatBuyRate = len(reactionList) / 100 * 25 # buy price

from dataManager import calculate_inventory_value as calculateInventoryValue

async def loadCommands(client, tree):
    @tree.command(name = "sell", description="Sell a reaction")
    async def sell(ctx, emoji: str):
        reaction = emo.demojize(emoji, language="alias")
        if reaction == "all":
            total = calculateInventoryValue(str(ctx.user.id))

            total = round(total, 2)
        
            await ctx.response.send_message("Are you sure you want to sell all reactions for " + str(total) + " credits? (y/n)")
            def check(m):
                return m.author == ctx.user and m.channel == ctx.channel
            try:
                msg = await client.wait_for('message', check=check, timeout=10.0)
            except:
                # we have to send the message a different way because we are not in the same scope
                await ctx.followup.send("Reaction sale cancelled.", ephemeral=True)
                return
            
            if msg.content.lower() != "y":
                await ctx.followup.send("Reaction sale cancelled.", ephemeral=True)
                return
            
            final = dm.add_user_data(str(ctx.user.id), "credits", total)

            print("final: " + str(final))

            final = round(final, 2)

            print("final: " + str(final))

            dm.save_user_data(str(ctx.user.id), "reactions", [])
            successString = settings["doubleCredits"] and "Double credits is active, doubling inventory value and selling for " or "Selling all reactions for "
            await ctx.followup.send(successString + str(final) + " credits.", ephemeral=True)
            return
        
        if reaction not in reactionList:
            # try without the alias
            reaction = emo.demojize(emoji, language="en")
            if reaction not in reactionList:
                await ctx.response.send_message("That is not a valid reaction.", ephemeral=True)
                return
            else:
                print("Using non-alias reaction")
                reaction = reactionList[reactionList.index(reaction)]

        
        if not dm.has_reaction(str(ctx.user.id), reaction):
            await ctx.response.send_message("You do not have that reaction.", ephemeral=True)
            return
        
        price = reactionList.index(reaction) > 0 and reactionList.index(reaction) * flatRate or 1 * flatRate
        price = round(price, 2)
        
        await ctx.response.send_message("Are you sure you want to sell " + reaction + " for " + str(price) + " credits? (y/n)")
        def check(m):
            return m.author == ctx.user and m.channel == ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=10.0)
        except:
            # we have to send the message a different way because we are not in the same scope
            ctx.followup.send("Reaction sale cancelled.", ephemeral=True)
            return
        
        if msg.content.lower() != "y":
            await ctx.followup.send("Reaction sale cancelled.", ephemeral=True)
            return
        
        
        dm.remove_reaction(str(ctx.user.id), reaction)
        
        final = dm.add_user_data(str(ctx.user.id), "credits", price)
        final = round(final, 2)

        successString = settings["doubleCredits"] and "Double credits is active, doubling reaction value. Sold for " or "Sold for "
        
        await ctx.followup.send(successString + str(final) + " credits.", ephemeral=True)


    @tree.command(name = "buy", description="Buy a reaction")
    async def buy(ctx, reaction: str):
        reaction = emo.demojize(reaction, language="alias")
        if reaction not in reactionList:
            await ctx.response.send_message("That is not a valid reaction.", ephemeral=True)
            return
        
        if dm.has_reaction(str(ctx.user.id), reaction):
            await ctx.response.send_message("You already have that reaction.", ephemeral=True)
            return
        
        price = reactionList.index(reaction) > 0 and reactionList.index(reaction) * flatBuyRate or 1 * flatBuyRate
        price = round(price, 2)
        
        if dm.get_user_data(str(ctx.user.id))["credits"] <= price:
            await ctx.response.send_message("You do not have enough credits to buy that reaction.", ephemeral=True)
            return
        
        
        await ctx.response.send_message("Are you sure you want to buy " + reaction + " for " + str(price) + " credits? (y/n)")
        def check(m):
            return m.author == ctx.user and m.channel == ctx.channel
        try:
            msg = await client.wait_for('message', check=check, timeout=10.0)
        except:
            # we have to send the message a different way because we are not in the same scope
            ctx.followup.send("Reaction purchase cancelled.", ephemeral=True)
            return
        
        if msg.content.lower() != "y":
            await ctx.followup.send("Reaction purchase cancelled.", ephemeral=True)
            return
        
        
        dm.add_reaction(str(ctx.user.id), reaction)
        
        dm.save_user_data(str(ctx.user.id), "credits", dm.get_user_data(str(ctx.user.id))["credits"] - price)
        
        await ctx.followup.send("Reaction purchased. - " + str(price) + " credits.", ephemeral=True)


    @tree.command(name = "claim", description="Claim your daily credits")
    async def claim(ctx):
        userId = str(ctx.user.id)
        if not dm.user_exists(userId):
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)
            return
            
        if dm.get_user_data(userId)["lastDaily"] != None:
            if dm.get_user_data(userId)["lastDaily"] == datetime.datetime.now().strftime("%Y-%m-%d"):
                await ctx.response.send_message("You have already claimed your daily credits today; you can claim them again at midnight.", ephemeral=True)
                return
            
        dm.save_user_data(userId, "lastDaily", datetime.datetime.now().strftime("%Y-%m-%d"))
        dm.save_user_data(userId, "credits", dm.get_user_data(userId)["credits"] + 250)
        await ctx.response.send_message("You have claimed your daily credits. +250 credits.", ephemeral=True)


    @tree.command(name = "cf", description="Play a game of coinflip")
    async def coinflip(ctx, bet: int, side: str):
        userId = str(ctx.user.id)
        if not dm.user_exists(userId):
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)
            return
        
        if dm.get_user_data(userId)["credits"] < bet:
            await ctx.response.send_message("You do not have enough credits to bet that much.", ephemeral=True)
            return
        
        if side.lower() != "heads" and side.lower() != "tails":
            await ctx.response.send_message("That is not a valid side.", ephemeral=True)
            return
        
        if bet < 1:
            await ctx.response.send_message("You must bet at least 1 credit.", ephemeral=True)
            return
        
        # get a random side
        sides = ["heads", "tails"]
        randomSide = sides[round(random.random())]
        bet = round(bet, 2)
        doubleVal = bet * 2
        doubleVal = round(doubleVal, 2)

        double = settings["doubleCoinFlip"]
        
        # did they win?
        if side.lower() == randomSide:
            if double:
                doubleVal = doubleVal
                await ctx.response.send_message("You won double! " + str(doubleVal) + " credits have been added to your balance. (Double coinflip is active)")

                dm.add_user_data(userId, "credits", doubleVal)

                return
            else:
                await ctx.response.send_message("You won! " + str(bet) + " credits have been added to your balance.")

                dm.add_user_data(userId, "credits", bet)

                return
        else:
            await ctx.response.send_message("You lost! " + str(bet) + " credits have been removed from your balance.")

            dm.save_user_data(userId, "credits", dm.get_user_data(userId)["credits"] - bet)

            return


    @tree.command(name = "total", description="View the total value of your inventory")
    async def total(ctx):
        userId = str(ctx.user.id)
        if not dm.user_exists(userId):
            await ctx.response.send_message("You don't have a save file! Use /register to create one.", ephemeral=True)
            return
        
        total = dm.calculate_inventory_value(userId)
        total = round(total, 2)
        await ctx.response.send_message("The total value of your inventory is " + str(total) + " credits.")
