import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import sys

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


class Owner(commands.Cog):
    """Bot owner-only commands."""

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return ctx.author.id == OWNER_ID

    # ── Prefix commands ──────────────────────────────────────────────

    @commands.command(name="load")
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        """Load a cog."""
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            embed = discord.Embed(
                description=f"✅ Loaded `cogs.{cog}` successfully.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Failed to load `cogs.{cog}`:\n```{e}```",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        """Unload a cog."""
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            embed = discord.Embed(
                description=f"✅ Unloaded `cogs.{cog}` successfully.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Failed to unload `cogs.{cog}`:\n```{e}```",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        """Reload a cog."""
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            embed = discord.Embed(
                description=f"✅ Reloaded `cogs.{cog}` successfully.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Failed to reload `cogs.{cog}`:\n```{e}```",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx):
        """Sync slash commands globally."""
        synced = await self.bot.tree.sync()
        embed = discord.Embed(
            description=f"✅ Synced `{len(synced)}` slash commands globally.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot."""
        embed = discord.Embed(
            description="🔴 Shutting down...",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        await self.bot.close()

    @commands.command(name="status")
    @commands.is_owner()
    async def set_status(self, ctx, *, text: str):
        """Change the bot's playing status."""
        await self.bot.change_presence(activity=discord.Game(name=text))
        embed = discord.Embed(
            description=f"✅ Status changed to: **{text}**",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="say")
    @commands.is_owner()
    async def say(self, ctx, *, message: str):
        """Make the bot say something."""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name="dm")
    @commands.is_owner()
    async def dm_user(self, ctx, user: discord.User, *, message: str):
        """DM a user."""
        try:
            await user.send(message)
            embed = discord.Embed(
                description=f"✅ DM sent to **{user}**.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Could not DM **{user}**: {e}",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="botinfo")
    @commands.is_owner()
    async def bot_info(self, ctx):
        """Display bot statistics."""
        guilds = len(self.bot.guilds)
        users = sum(g.member_count for g in self.bot.guilds)
        embed = discord.Embed(title="OrinCron — Bot Info", color=0x5865F2)
        embed.add_field(name="Guilds", value=str(guilds), inline=True)
        embed.add_field(name="Users", value=str(users), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Owner ID", value=str(OWNER_ID), inline=True)
        embed.set_footer(text="OrinCron Bot")
        await ctx.send(embed=embed)

    @commands.command(name="servers")
    @commands.is_owner()
    async def list_servers(self, ctx):
        """List all servers the bot is in."""
        lines = [f"`{g.id}` — **{g.name}** ({g.member_count} members)" for g in self.bot.guilds]
        embed = discord.Embed(
            title=f"OrinCron is in {len(self.bot.guilds)} servers",
            description="\n".join(lines) or "None",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    # ── Slash commands ────────────────────────────────────────────────

    @app_commands.command(name="ownerinfo", description="[Owner] Display bot owner info and stats.")
    async def slash_ownerinfo(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Owner only.", ephemeral=True)
            return
        guilds = len(self.bot.guilds)
        users = sum(g.member_count for g in self.bot.guilds)
        embed = discord.Embed(title="OrinCron — Owner Dashboard", color=0x5865F2)
        embed.add_field(name="Guilds", value=str(guilds), inline=True)
        embed.add_field(name="Users", value=str(users), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Owner(bot))
