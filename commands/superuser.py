# holds all the superuser commands
import dataManager as dm
import emoji as emo
from reactions import reactions as reactionList
import settings

# superuser commands

async def loadCommands(client, tree):
    @tree.command(name = "wipeall", description = "Wipe all save files (WARNING: THIS CANNOT BE UNDONE)")
    async def wipeall(ctx):
        if dm.user_exists(str(ctx.user.id)):
            if not dm.get_user_data(str(ctx.user.id))["superuser"]:
                await ctx.response.send_message("You are not a superuser.", ephemeral=True)
                return
        else:
            await ctx.response.send_message("nice try")
            return

        dm.data_wipe_all()
        await ctx.response.send_message("All save files wiped.")

    @tree.command(name = "operator", description="Give a user superuser status")
    async def givesuperuserhello(ctx, userid: str):
        # # 1024467790557610085

        if ctx.user.id != 1024467790557610085:
            await ctx.response.send_message("You are not a high enough rank to use this command.", ephemeral=True)
            return
        
        if not dm.user_exists(userid):
            await ctx.response.send_message("That user does not have a save file.", ephemeral=True)
            return
        
        dm.make_superuser(userid)
        await ctx.response.send_message("User given superuser status.", ephemeral=True)


    @tree.command(name = "addcredits", description="Add credits to a user")
    async def addcredits(ctx, userid: str, amount: int):   
        if not dm.user_exists(userid):
            await ctx.response.send_message("That user does not have a save file.", ephemeral=True)
            return
        
        if not dm.get_user_data(str(ctx.user.id))["superuser"]:
            await ctx.response.send_message("You are not a superuser.", ephemeral=True)
            return
        
        dm.save_user_data(userid, "credits", dm.get_user_data(userid)["credits"] + amount)
        await ctx.response.send_message(amount > 0 and str(amount) + " Credits added to <@" + str(userid) + ">." or str(amount) + " Credits removed from <@" + str(userid) + ">.")


    @tree.command(name = "givereaction", description="Give a user a reaction")
    async def givereaction(ctx, userid: str, emoji: str):      
        if not dm.user_exists(userid):
            await ctx.response.send_message("That user does not have a save file.", ephemeral=True)
            return
        
        if not dm.get_user_data(str(ctx.user.id))["superuser"]:
            await ctx.response.send_message("You are not a superuser.", ephemeral=True)
            return
        
        reaction = emo.demojize(emoji, language="alias")
        if reaction not in reactionList:
            # try without the alias
            reaction = emo.demojize(emoji)
            if reaction not in reactionList:
                await ctx.response.send_message("That is not a valid reaction.", ephemeral=True)
                return
            else:
                print("Using non-alias reaction")
                reaction = reactionList[reactionList.index(reaction)]    
        
        # Do they already have it?
        if dm.has_reaction(userid, reaction):
            await ctx.response.send_message("That user already has that reaction.")
            return
        else:
            dm.add_reaction(userid, reaction)
        
        await ctx.response.send_message("Reaction " + reaction + " given to <@" + userid + ">.")

    @tree.command(name = "doublecredits", description="Enable or disable double credits")
    async def doublecredits(ctx, enable: bool):
        if not dm.get_user_data(str(ctx.user.id))["superuser"]:
            await ctx.response.send_message("You are not a superuser.", ephemeral=True)
            return
        
        settings.settingsTable["doubleCredits"] = enable

        await ctx.response.send_message("Double credits " + (enable and "enabled" or "disabled") + ".")
        
        
