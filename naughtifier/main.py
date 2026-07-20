import discord
from discord.ext import commands
from discord import app_commands  # for slash command decorators
import os
from dotenv import load_dotenv
from event import Event

load_dotenv()
TOKEN = os.getenv('TOKEN')

GUILD_ID = 478287675837644800
MY_GUILD = discord.Object(id=GUILD_ID)

dintents = discord.Intents.default()
dintents.message_content = True

#client = discord.Client(intents=dintents) (cannot handle slash commands)

bot = commands.Bot(command_prefix='!', intents=dintents)  # prefix doesn't matter for slash commands


events = [
    Event(1, "Game Night", "Play board games online", "2026-07-25 18:00", "Discord Voice"),
    Event(2, "Code Review Session", "Review the new bot features", "2026-07-22 15:00", "General Chat"),
    Event(3, "Movie Watch Party", "Watch 'The Bot Movie' together", "2026-07-30 20:00", "Voice Channel 2"),
]


def load_help_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


#@client.event
#async def on_ready():
#    print(f'We have logged in as {client.user}')



#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')



@bot.command(name='hello')
async def hello_prefix(ctx):
    await ctx.send('Hello! (this is a prefix command, type !hello)')

@bot.command(name='guildid')
async def show_guild_id(ctx):
    await ctx.send(f"This server's ID is: `{ctx.guild.id}`")
#needs to be reworked!!

@bot.command(name='sync')
@commands.is_owner()  # Only you (the bot owner) can run this
async def sync_commands(ctx):
    """Force sync slash commands to this server."""
    await bot.tree.sync(guild=MY_GUILD)
    await ctx.send(f" Slash commands synced to guild ID {GUILD_ID}.")

@bot.command(name='list_commands')
@commands.is_owner()
async def list_commands(ctx):
    """List all synced slash commands for this guild."""
    guild = ctx.guild
    if guild is None:
        await ctx.send("This command only works in a server.")
        return
    # Get the bot's command tree for this guild
    commands_list = await bot.tree.fetch_commands(guild=discord.Object(id=guild.id))
    if not commands_list:
        await ctx.send("No slash commands found for this guild.")
    else:
        names = [f"`/{cmd.name}`" for cmd in commands_list]
        await ctx.send(f"Synced commands: {', '.join(names)}")

#@bot.command(name='help') -> already exists!!!
#async def help_prefix(ctx):
#    await ctx.send("Check out the slash command `/help` for full info!")

#/help

#/add_event name description date location

#/remove_event id

#/update_event id [options]

#/event_details id

# ---------- SLASH COMMANDS (Global + User Installable) ----------
# IMPORTANT: The 'guild=MY_GUILD' makes them register instantly without needing 'sync'

# These decorators make the command work in DMs and Group DMs

@discord.app_commands.allowed_installs(guilds=True, users=True)  # Allow install in guilds AND user profiles[reference:5]
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # Allow use in guilds, DMs, and Group DMs[reference:6]
@bot.tree.command(name="help", description="General information of how to use this bot")
async def help_slash(interaction: discord.Interaction):
    await interaction.response.send_message(load_help_text("naughtifier/contents/help_text.txt"))

@discord.app_commands.allowed_installs(guilds=True, users=True)  # Allow install in guilds AND user profiles[reference:5]
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)  # Allow use in guilds, DMs, and Group DMs[reference:6]
@bot.tree.command(name="hello", description="Say hello via slash command")
async def hello_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Hello from slash command!")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="events", description="List all currently available events")
async def query_all_events(interaction: discord.Interaction):
    if not events:
        await interaction.response.send_message("No events available right now.")
        return

    # Build a formatted response
    response = " **All Available Events:**\n\n"
    for event in events:
        response += f"{event}\n\n"

   # Discord limits messages to 2000 chars – handle that if needed
    if len(response) > 2000:
        await interaction.response.send_message("Too many events! I'll send a file.", ephemeral=True)
        # Optionally send as a text file here
    else:
        await interaction.response.send_message(response)

@bot.event
async def on_ready():
    print(f" Bot logged in as {bot.user}")
    print(f" Attempting to sync slash commands to Guild ID: {GUILD_ID}")

    try:
        await bot.tree.sync()
        print(f" Sync successful! Logged in as {bot.user}. Commands should appear in your server shortly.")
    except Exception as e:
        print(f" Sync failed with error: {e}")

if __name__ == '__main__':
    bot.run(TOKEN)

