import discord 
from discord.ext  import commands, tasks
from discord import app_commands
from itertools import cycle
import os
import asyncio
import pathlib


path = pathlib.Path(__file__).parent.resolve()

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all(),help_command=None)

bot_status = cycle(["Singing ♪♪♪", "Chilling 😇", "Sad... 🥺"])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    print(f'{client.user} has wake up !')
    change_status.start()
    try:
        synced = await client.tree.sync()
        print(f"Successfully synced {len(synced)} commands.")
    except Exception as e:
        print(e)




@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}", ephemeral=True)

@client.tree.command(name="say")
@app_commands.describe(thing_to_say= "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}", ephemeral=True)

@client.event
async def on_command_error(ctx,error):
    if(isinstance(error,commands.MissingRequiredArgument)):
        await ctx.send("Missing required argument")
    if(isinstance(error,commands.MissingPermissions)):
        await ctx.send("You don't have permission! baka!")
    

async def load():
    for file in os.listdir(os.path.join(path,'cogs')):
        if file.endswith(".py"):
            
            await client.load_extension(f"cogs.{file[:-3]}")

#@client.command(aliases=["lmao","huhu"]) ## command will be run if type in !lmao or !huhu or !clear


async def main():
    async with client:
        await load()
        await client.start('enter your token here')

asyncio.run(main())

