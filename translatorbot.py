







import asyncio
import discord
from googletrans import Translator


TOKEN = 
intents = discord.Intents.default()
intents.reactions = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print('Logged in as', client.user)

@client.event
async def on_message(message):
    print(f"Message received: {message.content}")

    if message.author == client.user:
        return

    if message.content.startswith('!translate'):
        content = message.content[len('!translate'):].strip()
        print("Received message:", content)
        await message.channel.send("Please send the country code of the desired language (e.g., en for English, es for Spanish, fr for French, de for German). "
                                   "Send 'stop' to stop translating.")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        while True:
            try:
                msg = await client.wait_for('message', check=check, timeout=30)  # Wait for user's response

                if msg.content.lower() == 'stop':
                    await message.channel.send("Translation stopped.")
                    break

                dest_lang = msg.content.lower()

                translated = translator.translate(content, dest=dest_lang).text
                print(f"Translated message ({dest_lang}): {translated}")
                await message.channel.send(f"Translated message ({dest_lang}): {translated}")

                await message.channel.send("Send another country code or 'stop' to stop translating.")

            except asyncio.TimeoutError:
                await message.channel.send("Translation request timed out. Please try again.")
                break

            except Exception as e:
                print("Translation Error:", e)
                await message.channel.send("An error occurred during translation. Please try again later.")
                break

client.run(TOKEN)