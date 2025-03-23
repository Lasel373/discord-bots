import os
import discord
import datetime
from dotenv import load_dotenv
from responses import get_response

load_dotenv()
TOKEN = os.getenv('TOKEN')

dintents = discord.Intents.default()
dintents.message_content = True
client = discord.Client(intents=dintents)

async def send_message(message: discord.Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")

    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " application: Login as '{0.user}'".format(client))

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return
    
    #logging
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)
    
if __name__ == '__main__':
    client.run(TOKEN)