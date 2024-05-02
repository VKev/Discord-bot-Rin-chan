from g4f.client import AsyncClient
from g4f.cookies import set_cookies
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
import discord  
from discord.ext import commands
import requests

set_cookies(".bing.com", {
"_U": "1IvqFCeKeWR94_1tMC4adFm1loHy7arAUztuJv6CmEyM8R9I-71O8-IJz2Ek01-HfvwLmTSfm8apWiqX9JS4lsyABHfbv3xPhOruuJW2AYZSskIe1PcsuOHOndFgHwaDcGt3FX8NhNLO6ov4bc2VHh_bOnUtQkFgBdEHmM08i9STikmx5YhniJic3dscag1dlQLhqLv4wietF2RG9AsXVRCRfnpBH3vxyJz4pV5snysQ"
})

set_cookies(".google.com", {
"__Secure-1PSID": "g.a000iAgkpxIn5ta4aIuPvpcbgr7xi4NVOYhrTzva559hv62tcByY9WebT2mdDNRxvvOXB3fFngACgYKAewSAQASFQHGX2Mild5VphrxWgIZRXa6SeJqthoVAUF8yKp1NTNnS6kx0T9F22v6w5Eb0076",
"__Secure-1PSIDCC":"AKEyXzWlsjbLal-cX05lBAZaDFYFKyh2Jfa5LsEpCJ2alxgESfRBWP8WwMC5LueqjRo4AXJLvd8",
"__Secure-1PSIDTS":"sidts-CjEBLwcBXE8fPP5fqkre35-B3gNLaNPwP701DE8ufx14oZ6Ezi4Jwb9a96SreEfHRY0zEAA"
})


asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


class OpenAi(commands.Cog):
    def __init__(self, client):
        self.client = client
        try:
            self.clientAI = AsyncClient()
        except Exception as e:
            print("Error initializing g4f client:", e)

    async def update_processing_message(self,processing_msg, spin_chars):
            spin_index = 0
            while True:
                await processing_msg.edit(content=f"{processing_msg.content} {spin_chars[spin_index]}")
                spin_index = (spin_index + 1) % len(spin_chars)
                await asyncio.sleep(0.5)

    @commands.command(name="gpt4")
    async def gpt4(self, ctx, *, content):
        processing_msg = await ctx.send("Generating response, please wait...")
        spin_chars = ['-', '\\', '|', '/']
        
        spin_task = self.client.loop.create_task(self.update_processing_message(processing_msg, spin_chars))
        response = await self.clientAI.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": content}],
        )
        spin_task.cancel()
        await processing_msg.delete()

        await ctx.message.reply(response.choices[0].message.content)

    @commands.command(name="gpt3")
    async def gpt3(self, ctx, *, content):
        processing_msg = await ctx.send("Generating response, please wait...")
        spin_chars = ['-', '\\', '|', '/']
        
        spin_task = self.client.loop.create_task(self.update_processing_message(processing_msg, spin_chars))
        response = await self.clientAI.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}],
        )
        spin_task.cancel()
        await processing_msg.delete()

        await ctx.message.reply(response.choices[0].message.content)

    @commands.command(name="dall3")
    async def dall3(self, ctx, *, content):
        processing_msg = await ctx.send("Generating image, please wait...")
        spin_chars = ['-', '\\', '|', '/']
        
        spin_task = self.client.loop.create_task(self.update_processing_message(processing_msg, spin_chars))
        
        response = await self.clientAI.images.generate(
            model="dall-e-3",
            prompt= content,
        )
        spin_task.cancel()
        await processing_msg.delete()

        image_url = response.data[0].url
        await ctx.message.reply(image_url)


    @commands.Cog.listener()
    async def on_ready(self):
        print("OpenAi.py is ready!")

async def setup(client):
    await client.add_cog(OpenAi(client))
