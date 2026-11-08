import discord
from discord.ext import commands
from discord import app_commands
import time
import platform
import os
import datetime

PREFIX = os.getenv("BOT_PREFIX", "+")


class Utility(commands.Cog):
    """General utility commands."""

    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    # ── Help ──────────────────────────────────────────────────────────

    @commands.command(name="help")
    async def help_command(self, ctx, *, category: str = None):
        """Show help information."""
        p = PREFIX
        if category:
            category = category.lower()
            if category in ("tempvoice", "tv", "voice"):
                embed = discord.Embed(title="TempVoice Commands", color=0x5865F2)
                embed.add_field(name=f"Slash Commands", value=(
                    "`/setup` — Set up the TempVoice system\n"
                    "`/resetup` — Reset and redo setup\n"
                    "`/tvstatus` — View TempVoice configuration"
                ), inline=False)
                embed.add_field(name=f"Prefix Commands", value=(
                    f"`{p}tvsetup` — Prompt to use /setup\n"
                    f"`{p}tvreset` — Clear TempVoice data"
                ), inline=False)
            elif category in ("utility", "util"):
                embed = discord.Embed(title="Utility Commands", color=0x5865F2)
                embed.add_field(name="Commands", value=(
                    f"`{p}help [category]` — Show this help\n"
                    f"`{p}ping` — Bot latency\n"
                    f"`{p}uptime` — Bot uptime\n"
                    f"`{p}serverinfo` — Server information\n"
                    f"`{p}userinfo [@user]` — User information\n"
                    f"`{p}avatar [@user]` — User avatar\n"
                    f"`{p}botinfo` — Bot information\n"
                    f"`{p}invite` — Bot invite link\n"
                    f"`{p}membercount` — Server member count\n"
                    f"`{p}channelinfo [#channel]` — Channel info\n"
                    f"`{p}roleinfo [role]` — Role information\n"
                    f"`{p}roles` — List all server roles\n"
                    f"`{p}emojis` — List server emojis"
                ), inline=False)
            elif category in ("fun",):
                embed = discord.Embed(title="Fun Commands", color=0x5865F2)
                embed.add_field(name="Commands", value=(
                    f"`{p}8ball <question>` — Ask the magic 8-ball\n"
                    f"`{p}roll [sides]` — Roll a dice\n"
                    f"`{p}flip` — Flip a coin\n"
                    f"`{p}rps <rock/paper/scissors>` — Rock Paper Scissors\n"
                    f"`{p}choose <a|b|c>` — Choose between options\n"
                    f"`{p}reverse <text>` — Reverse text\n"
                    f"`{p}mock <text>` — MoCkIfY tExT\n"
                    f"`{p}ascii <text>` — ASCII art text\n"
                    f"`{p}rate <thing>` — Rate something out of 10\n"
                    f"`{p}ship @user1 @user2` — Ship two users\n"
                    f"`{p}fact` — Random fun fact\n"
                    f"`{p}roast @user` — Roast a user\n"
                    f"`{p}compliment @user` — Compliment a user\n"
                    f"`{p}slots` — Slot machine"
                ), inline=False)
            elif category in ("owner",):
                embed = discord.Embed(title="Owner Commands", color=0x5865F2)
                embed.add_field(name="Commands (Bot Owner Only)", value=(
                    f"`{p}load <cog>` — Load a cog\n"
                    f"`{p}unload <cog>` — Unload a cog\n"
                    f"`{p}reload <cog>` — Reload a cog\n"
                    f"`{p}sync` — Sync slash commands\n"
                    f"`{p}shutdown` — Shut down the bot\n"
                    f"`{p}status <text>` — Change bot status\n"
                    f"`{p}say <message>` — Make bot say something\n"
                    f"`{p}dm @user <message>` — DM a user\n"
                    f"`{p}botinfo` — Bot statistics\n"
                    f"`{p}servers` — List all servers"
                ), inline=False)
            else:
                embed = discord.Embed(description="❌ Unknown category.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="OrinCron — Help",
            description=(
                f"**Prefix:** `{p}` | Slash commands also supported.\n\n"
                f"Use `{p}help <category>` for more info."
            ),
            color=0x5865F2,
        )
        embed.add_field(name="📂 Categories", value=(
            f"`{p}help utility` — General utility\n"
            f"`{p}help fun` — Fun commands\n"
            f"`{p}help tempvoice` — TempVoice system\n"
            f"`{p}help owner` — Owner-only commands"
        ), inline=False)
        embed.set_footer(text="OrinCron • Orange")
        await ctx.send(embed=embed)

    @app_commands.command(name="help", description="Get help with OrinCron commands.")
    @app_commands.describe(category="Category to view (utility, fun, tempvoice, owner)")
    async def slash_help(self, interaction: discord.Interaction, category: str = None):
        ctx_like = type("ctx", (), {"send": interaction.response.send_message, "guild": interaction.guild})()
        p = PREFIX
        embed = discord.Embed(
            title="OrinCron — Help",
            description=f"**Prefix:** `{p}` | Slash commands also supported.\n\nCategories: `utility`, `fun`, `tempvoice`, `owner`",
            color=0x5865F2,
        )
        embed.set_footer(text="OrinCron • Orange")
        await interaction.response.send_message(embed=embed)

    # ── Ping ─────────────────────────────────────────────────────────

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def slash_ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: **{latency}ms**", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Uptime ────────────────────────────────────────────────────────

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        """Show bot uptime."""
        elapsed = int(time.time() - self.start_time)
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        embed = discord.Embed(
            title="⏱️ Uptime",
            description=f"**{hours}h {minutes}m {seconds}s**",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="uptime", description="Check how long the bot has been running.")
    async def slash_uptime(self, interaction: discord.Interaction):
        elapsed = int(time.time() - self.start_time)
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        embed = discord.Embed(title="⏱️ Uptime", description=f"**{hours}h {minutes}m {seconds}s**", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Server Info ───────────────────────────────────────────────────

    @commands.command(name="serverinfo", aliases=["si", "server"])
    async def serverinfo(self, ctx):
        """Show server information."""
        g = ctx.guild
        embed = discord.Embed(title=g.name, color=0x5865F2, timestamp=discord.utils.utcnow())
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="Owner", value=str(g.owner), inline=True)
        embed.add_field(name="ID", value=str(g.id), inline=True)
        embed.add_field(name="Region", value=str(g.preferred_locale), inline=True)
        embed.add_field(name="Members", value=str(g.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(g.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(g.roles)), inline=True)
        embed.add_field(name="Emojis", value=str(len(g.emojis)), inline=True)
        embed.add_field(name="Boost Level", value=str(g.premium_tier), inline=True)
        embed.add_field(name="Boosts", value=str(g.premium_subscription_count), inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(g.created_at, style="R"), inline=True)
        embed.set_footer(text="OrinCron")
        await ctx.send(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about this server.")
    async def slash_serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        embed = discord.Embed(title=g.name, color=0x5865F2, timestamp=discord.utils.utcnow())
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.add_field(name="Owner", value=str(g.owner), inline=True)
        embed.add_field(name="ID", value=str(g.id), inline=True)
        embed.add_field(name="Members", value=str(g.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(g.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(g.roles)), inline=True)
        embed.add_field(name="Boost Level", value=str(g.premium_tier), inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(g.created_at, style="R"), inline=True)
        await interaction.response.send_message(embed=embed)

    # ── User Info ─────────────────────────────────────────────────────

    @commands.command(name="userinfo", aliases=["ui", "whois"])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Show user information."""
        member = member or ctx.author
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        embed = discord.Embed(title=str(member), color=member.color, timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, style="R"), inline=True)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, style="R"), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:10]) or "None", inline=False)
        embed.set_footer(text="OrinCron")
        await ctx.send(embed=embed)

    @app_commands.command(name="userinfo", description="Show information about a user.")
    @app_commands.describe(member="The member to inspect")
    async def slash_userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.guild.get_member(interaction.user.id)
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        embed = discord.Embed(title=str(member), color=member.color, timestamp=discord.utils.utcnow())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, style="R"), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:10]) or "None", inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Avatar ────────────────────────────────────────────────────────

    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar(self, ctx, member: discord.Member = None):
        """Show a user's avatar."""
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=0x5865F2)
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @app_commands.command(name="avatar", description="View a user's avatar.")
    @app_commands.describe(member="The member whose avatar to show")
    async def slash_avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.guild.get_member(interaction.user.id)
        embed = discord.Embed(title=f"{member.display_name}'s Avatar", color=0x5865F2)
        embed.set_image(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ── Bot Info ──────────────────────────────────────────────────────

    @commands.command(name="info")
    async def info(self, ctx):
        """Show bot information."""
        embed = discord.Embed(title="OrinCron", description="A feature-rich Join2Create bot.", color=0x5865F2)
        embed.add_field(name="Guilds", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Prefix", value=PREFIX, inline=True)
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="OrinCron • Orange")
        await ctx.send(embed=embed)

    # ── Invite ────────────────────────────────────────────────────────

    @commands.command(name="invite")
    async def invite(self, ctx):
        """Get the bot invite link."""
        perms = discord.Permissions(
            manage_channels=True,
            manage_roles=True,
            read_messages=True,
            send_messages=True,
            embed_links=True,
            move_members=True,
            connect=True,
            speak=True,
            read_message_history=True,
        )
        url = discord.utils.oauth_url(self.bot.user.id, permissions=perms)
        embed = discord.Embed(
            title="📨 Invite OrinCron",
            description=f"[Click here to invite me!]({url})",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="invite", description="Get the invite link for OrinCron.")
    async def slash_invite(self, interaction: discord.Interaction):
        perms = discord.Permissions(manage_channels=True, manage_roles=True, read_messages=True, send_messages=True, embed_links=True, move_members=True)
        url = discord.utils.oauth_url(self.bot.user.id, permissions=perms)
        embed = discord.Embed(title="📨 Invite OrinCron", description=f"[Click here to invite me!]({url})", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Member Count ──────────────────────────────────────────────────

    @commands.command(name="membercount", aliases=["mc", "members"])
    async def membercount(self, ctx):
        """Show the server's member count."""
        g = ctx.guild
        bots = sum(1 for m in g.members if m.bot)
        humans = g.member_count - bots
        embed = discord.Embed(title=f"{g.name} — Member Count", color=0x5865F2)
        embed.add_field(name="Total", value=str(g.member_count), inline=True)
        embed.add_field(name="Humans", value=str(humans), inline=True)
        embed.add_field(name="Bots", value=str(bots), inline=True)
        await ctx.send(embed=embed)

    # ── Channel Info ──────────────────────────────────────────────────

    @commands.command(name="channelinfo", aliases=["ci"])
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Show info about a channel."""
        channel = channel or ctx.channel
        embed = discord.Embed(title=f"#{channel.name}", color=0x5865F2)
        embed.add_field(name="ID", value=str(channel.id), inline=True)
        embed.add_field(name="Type", value=str(channel.type), inline=True)
        embed.add_field(name="Category", value=str(channel.category) if channel.category else "None", inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(channel.created_at, style="R"), inline=True)
        embed.add_field(name="NSFW", value="Yes" if channel.nsfw else "No", inline=True)
        if channel.topic:
            embed.add_field(name="Topic", value=channel.topic[:200], inline=False)
        await ctx.send(embed=embed)

    # ── Role Info ─────────────────────────────────────────────────────

    @commands.command(name="roleinfo", aliases=["ri"])
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Show info about a role."""
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="ID", value=str(role.id), inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Members", value=str(len(role.members)), inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(role.created_at, style="R"), inline=True)
        await ctx.send(embed=embed)

    # ── Roles ─────────────────────────────────────────────────────────

    @commands.command(name="roles")
    async def roles(self, ctx):
        """List all server roles."""
        roles = [r.mention for r in reversed(ctx.guild.roles) if r.name != "@everyone"]
        embed = discord.Embed(
            title=f"{ctx.guild.name} Roles ({len(roles)})",
            description=" ".join(roles[:50]) or "No roles",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    # ── Emojis ────────────────────────────────────────────────────────

    @commands.command(name="emojis")
    async def emojis(self, ctx):
        """List server emojis."""
        emojis = ctx.guild.emojis
        if not emojis:
            await ctx.send("This server has no custom emojis.")
            return
        emoji_str = " ".join(str(e) for e in emojis[:50])
        embed = discord.Embed(
            title=f"{ctx.guild.name} Emojis ({len(emojis)})",
            description=emoji_str,
            color=0x5865F2,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))
