import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "+")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True


class OrinCron(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            owner_id=OWNER_ID,
            help_command=None,
            case_insensitive=True,
        )

    async def setup_hook(self):
        cogs = ["cogs.owner", "cogs.tempvoice", "cogs.utility", "cogs.fun"]
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"[+] Loaded {cog}")
            except Exception as e:
                print(f"[-] Failed to load {cog}: {e}")
        await self.tree.sync()
        print("[+] Slash commands synced")

    async def on_ready(self):
        print(f"[+] Logged in as {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Game(name=f"{PREFIX}help || Orange"),
            status=discord.Status.online,
        )

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="❌ You don't have permission to use this command.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="❌ This command is restricted to the bot owner.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"❌ Missing argument: `{error.param.name}`",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        else:
            print(f"[Error] {error}")


bot = OrinCron()

if __name__ == "__main__":
    if not TOKEN:
        print("[-] ERROR: DISCORD_TOKEN not set in .env file.")
    else:
        bot.run(TOKEN)
