from g4f.client import AsyncClient
from g4f.cookies import set_cookies
import asyncio
from discord.ext import commands
import logging

set_cookies(".bing.com", {
"_U": "1efYXLNNrlbV3AZgLkh9e1FFkzfi--0iWQdlAwmSoj_l_LauAq3tghzCvZtqFQTMa34yTku21eexytXX-VOIDMWHOKd5BCrFNmh0u3hZ7EAtLnPqg9aX3oQ31DrrrSL1d0PPnjLEc8I6-yKbU4KwBQPKfImzh11xaGtYaeXJzW0bv83DD8ms1YQJhYgkgejnZ4bhD2ZpLK9H2oif9TWz92IdDlS-fKKDPsXzNPB8_-j0"
})

set_cookies(".google.com", {
"__Secure-1PSID": "g.a000jAgRQ64CdgTFe2D8WgfiNGBZJbRtQqEcSWT74sUwOQrSzYIJvvHBFeZFYK245Hgus9cSBQACgYKAXcSAQASFQHGX2Mi7pVeI-kmTVsNBmPmb-ripxoVAUF8yKqjWCL1wfRPMOqlqBaHQBjX0076",
"__Secure-1PSIDCC":"AKEyXzWx52C8FE40UnzpvGYu_xap2lRiAKiQ26o3m4uFf1eR5U_ThDUgV183Yw5s-20tmvt5q3c",
"__Secure-1PSIDTS":"sidts-CjIBLwcBXODuVGYLdeoO3HnMrBlprALTFhORt4xkPGcCYCxoO-UF3USyn-0VtfOMuakfixAA"
})


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
        try:
            response = await self.clientAI.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": content}],
            )
            spin_task.cancel()
            await processing_msg.delete()

            await ctx.message.reply(response.choices[0].message.content)
        except Exception as e:
            spin_task.cancel()
            await processing_msg.edit(content=(str(e)+". Không thể vượt capcha =))"))

    @commands.command(name="gpt3")
    async def gpt3(self, ctx, *, content):
        processing_msg = await ctx.send("Generating response, please wait...")
        spin_chars = ['-', '\\', '|', '/']
        
        spin_task = self.client.loop.create_task(self.update_processing_message(processing_msg, spin_chars))
        try:
            response = await self.clientAI.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}],
            )
            spin_task.cancel()
            await processing_msg.delete()

            await ctx.message.reply(response.choices[0].message.content)
        except Exception as e:
            spin_task.cancel()
            await processing_msg.edit(content=e)

    @commands.command(name="dall3")
    async def dall3(self, ctx, *, content):
        processing_msg = await ctx.send("Generating image, please wait...")
        spin_chars = ['-', '\\', '|', '/']
        
        spin_task = self.client.loop.create_task(self.update_processing_message(processing_msg, spin_chars))
        try:
            response = await self.clientAI.images.generate(
                model="dall-e-3",
                prompt= content,
            )
            spin_task.cancel()
            await processing_msg.delete()

            image_url = response.data[0].url
            await ctx.message.reply(image_url)
        except Exception as e:
            spin_task.cancel()
            await processing_msg.edit(content=e)
            


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("OpenAi.py is ready!")

async def setup(client):
    await client.add_cog(OpenAi(client))
