import discord  
from discord.ext import commands


class Interaction(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(seft):
        print("Interaction.py is ready!")


    @commands.command()
    async def help(self,ctx):
        
        embed_message = discord.Embed(title="Bot guilding!",description= "Tutorial to use this bot!",color=ctx.author.color)

        embed_message.set_author(name=f"Requested by {ctx.author.name}",icon_url=ctx.author.avatar)
        
        embed_message.add_field(name="Commands", value="!ping: Display bot ping\n\
                                !clear <amount>: Clear message\n\
                                !play <name/link>: Play song, add queue\n\
                                !skip: Skip the song\n\
                                !queue: View song queue\n\
                                !gpt3 <question>: ask chatgpt question"
                                ,inline=False)
        embed_message.add_field(name="Author", value="This bot made by Vkev: \n [Click here for more information](https://vkev.github.io/Portfolio/)",inline=True)
        embed_message.set_image(url="https://i.imgur.com/MMqS2EM.jpg")

        await ctx.send(embed = embed_message)


    @commands.command()
    async def ping(self,ctx):
        bot_ping = round(self.client.latency*1000)
        await ctx.send(f"ping: {bot_ping} ms")


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx, amount: int):
        await ctx.channel.purge(limit = amount)
        await ctx.send(f'Rin has cleared {amount} message')

    

async def setup(client):
    await client.add_cog(Interaction(client))
