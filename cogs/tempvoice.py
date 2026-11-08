import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "data/tempvoice.json"


def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_guild_config(guild_id: int) -> dict:
    data = load_data()
    return data.get(str(guild_id), {})


def set_guild_config(guild_id: int, config: dict):
    data = load_data()
    data[str(guild_id)] = config
    save_data(data)


def get_temp_channels(guild_id: int) -> dict:
    config = get_guild_config(guild_id)
    return config.get("temp_channels", {})


def save_temp_channels(guild_id: int, temp_channels: dict):
    data = load_data()
    if str(guild_id) not in data:
        data[str(guild_id)] = {}
    data[str(guild_id)]["temp_channels"] = temp_channels
    save_data(data)


# ── Interface View ────────────────────────────────────────────────────────────

class TempVoiceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def _get_owner(self, guild: discord.Guild, channel_id: int) -> int | None:
        temp = get_temp_channels(guild.id)
        info = temp.get(str(channel_id))
        if info:
            return info.get("owner")
        return None

    async def _get_user_channel(self, interaction: discord.Interaction) -> discord.VoiceChannel | None:
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice or not member.voice.channel:
            await interaction.response.send_message(
                "❌ You must be in your temp voice channel to use this.", ephemeral=True
            )
            return None
        vc = member.voice.channel
        temp = get_temp_channels(interaction.guild.id)
        if str(vc.id) not in temp:
            await interaction.response.send_message(
                "❌ You are not in a temp voice channel.", ephemeral=True
            )
            return None
        owner_id = temp[str(vc.id)].get("owner")
        if owner_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ You are not the owner of this voice channel.", ephemeral=True
            )
            return None
        return vc

    # Row 1
    @discord.ui.button(label="Lock", emoji="🔒", style=discord.ButtonStyle.secondary, custom_id="tv:lock", row=0)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        overwrite = vc.overwrites_for(interaction.guild.default_role)
        overwrite.connect = False
        await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="🔒 Channel **locked**. No new members can join.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Unlock", emoji="🔓", style=discord.ButtonStyle.secondary, custom_id="tv:unlock", row=0)
    async def unlock(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        overwrite = vc.overwrites_for(interaction.guild.default_role)
        overwrite.connect = None
        await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="🔓 Channel **unlocked**. Anyone can join.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Hide", emoji="🙈", style=discord.ButtonStyle.secondary, custom_id="tv:hide", row=0)
    async def hide(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        overwrite = vc.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = False
        await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="🙈 Channel **hidden** from others.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Unhide", emoji="👁️", style=discord.ButtonStyle.secondary, custom_id="tv:unhide", row=0)
    async def unhide(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        overwrite = vc.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = None
        await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description="👁️ Channel **visible** to everyone.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Row 2
    @discord.ui.button(label="Limit", emoji="👥", style=discord.ButtonStyle.secondary, custom_id="tv:limit", row=1)
    async def limit(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(LimitModal(vc))

    @discord.ui.button(label="Invite", emoji="📨", style=discord.ButtonStyle.secondary, custom_id="tv:invite", row=1)
    async def invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(InviteModal(vc))

    @discord.ui.button(label="Ban", emoji="🔨", style=discord.ButtonStyle.secondary, custom_id="tv:ban", row=1)
    async def ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(BanModal(vc))

    @discord.ui.button(label="Permit", emoji="✅", style=discord.ButtonStyle.secondary, custom_id="tv:permit", row=1)
    async def permit(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(PermitModal(vc))

    # Row 3
    @discord.ui.button(label="Rename", emoji="✏️", style=discord.ButtonStyle.secondary, custom_id="tv:rename", row=2)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(RenameModal(vc))

    @discord.ui.button(label="Bitrate", emoji="🎧", style=discord.ButtonStyle.secondary, custom_id="tv:bitrate", row=2)
    async def bitrate(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(BitrateModal(vc))

    @discord.ui.button(label="Region", emoji="🌐", style=discord.ButtonStyle.secondary, custom_id="tv:region", row=2)
    async def region(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(RegionModal(vc))

    @discord.ui.button(label="Template", emoji="📋", style=discord.ButtonStyle.secondary, custom_id="tv:template", row=2)
    async def template(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(TemplateModal(vc))

    # Row 4
    @discord.ui.button(label="Chat", emoji="💬", style=discord.ButtonStyle.secondary, custom_id="tv:chat", row=3)
    async def chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ You must be in a temp voice channel.", ephemeral=True)
            return
        vc = member.voice.channel
        temp = get_temp_channels(interaction.guild.id)
        info = temp.get(str(vc.id))
        if not info:
            await interaction.response.send_message("❌ You are not in a temp voice channel.", ephemeral=True)
            return
        if interaction.user.id != info.get("owner"):
            await interaction.response.send_message("❌ Only the channel owner can use this.", ephemeral=True)
            return
        text_id = info.get("text_channel")
        if text_id:
            channel = interaction.guild.get_channel(text_id)
            if channel:
                await interaction.response.send_message(f"💬 Your text channel: {channel.mention}", ephemeral=True)
                return
        category = vc.category
        text_channel = await interaction.guild.create_text_channel(
            name=vc.name,
            category=category,
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            },
            reason="TempVoice chat channel",
        )
        temp[str(vc.id)]["text_channel"] = text_channel.id
        save_temp_channels(interaction.guild.id, temp)
        embed = discord.Embed(description=f"💬 Created your text channel: {text_channel.mention}", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Waiting", emoji="⏳", style=discord.ButtonStyle.secondary, custom_id="tv:waiting", row=3)
    async def waiting(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        temp = get_temp_channels(interaction.guild.id)
        info = temp.get(str(vc.id), {})
        waiting = info.get("waiting_enabled", False)
        if not waiting:
            overwrite = vc.overwrites_for(interaction.guild.default_role)
            overwrite.connect = False
            overwrite.view_channel = True
            await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            temp[str(vc.id)]["waiting_enabled"] = True
            save_temp_channels(interaction.guild.id, temp)
            embed = discord.Embed(description="⏳ **Waiting room** enabled. Members can see but not join.", color=0x5865F2)
        else:
            overwrite = vc.overwrites_for(interaction.guild.default_role)
            overwrite.connect = None
            await vc.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            temp[str(vc.id)]["waiting_enabled"] = False
            save_temp_channels(interaction.guild.id, temp)
            embed = discord.Embed(description="⏳ **Waiting room** disabled.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Claim", emoji="👑", style=discord.ButtonStyle.secondary, custom_id="tv:claim", row=3)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.voice or not member.voice.channel:
            await interaction.response.send_message("❌ You must be in a temp voice channel to claim it.", ephemeral=True)
            return
        vc = member.voice.channel
        temp = get_temp_channels(interaction.guild.id)
        if str(vc.id) not in temp:
            await interaction.response.send_message("❌ This is not a temp voice channel.", ephemeral=True)
            return
        owner_id = temp[str(vc.id)].get("owner")
        owner = interaction.guild.get_member(owner_id)
        if owner and owner.voice and owner.voice.channel and owner.voice.channel.id == vc.id:
            await interaction.response.send_message("❌ The current owner is still in the channel.", ephemeral=True)
            return
        temp[str(vc.id)]["owner"] = interaction.user.id
        save_temp_channels(interaction.guild.id, temp)
        await vc.edit(name=f"{member.display_name}'s VC")
        embed = discord.Embed(description=f"👑 {member.mention} is now the owner of this channel.", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Transfer", emoji="🔄", style=discord.ButtonStyle.secondary, custom_id="tv:transfer", row=3)
    async def transfer(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = await self._get_user_channel(interaction)
        if not vc:
            return
        await interaction.response.send_modal(TransferModal(vc))


# ── Modals ────────────────────────────────────────────────────────────────────

class LimitModal(discord.ui.Modal, title="Set User Limit"):
    limit_input = discord.ui.TextInput(
        label="User Limit (0 = unlimited, max 99)",
        placeholder="Enter a number between 0 and 99",
        min_length=1,
        max_length=2,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.limit_input.value)
            if val < 0 or val > 99:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("❌ Invalid number. Enter 0–99.", ephemeral=True)
            return
        await self.vc.edit(user_limit=val)
        txt = "unlimited" if val == 0 else str(val)
        embed = discord.Embed(description=f"👥 User limit set to **{txt}**.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class RenameModal(discord.ui.Modal, title="Rename Channel"):
    name_input = discord.ui.TextInput(
        label="New Channel Name",
        placeholder="Enter a new name",
        min_length=1,
        max_length=100,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        await self.vc.edit(name=self.name_input.value)
        embed = discord.Embed(description=f"✏️ Channel renamed to **{self.name_input.value}**.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class BitrateModal(discord.ui.Modal, title="Set Bitrate"):
    bitrate_input = discord.ui.TextInput(
        label="Bitrate (kbps, 8–384)",
        placeholder="Enter bitrate e.g. 64",
        min_length=1,
        max_length=3,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.bitrate_input.value)
            if val < 8 or val > 384:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("❌ Invalid bitrate. Enter 8–384.", ephemeral=True)
            return
        await self.vc.edit(bitrate=val * 1000)
        embed = discord.Embed(description=f"🎧 Bitrate set to **{val} kbps**.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class RegionModal(discord.ui.Modal, title="Set Region"):
    region_input = discord.ui.TextInput(
        label="Region (leave blank for auto)",
        placeholder="e.g. us-east, europe, singapore, auto",
        required=False,
        max_length=50,
    )

    REGIONS = {
        "auto": None,
        "us-east": "us-east",
        "us-west": "us-west",
        "us-central": "us-central",
        "us-south": "us-south",
        "europe": "europe",
        "india": "india",
        "singapore": "singapore",
        "south-korea": "south-korea",
        "japan": "japan",
        "brazil": "brazil",
        "sydney": "sydney",
        "rotterdam": "rotterdam",
        "russia": "russia",
    }

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        val = self.region_input.value.strip().lower() or "auto"
        if val not in self.REGIONS:
            regions_list = ", ".join(self.REGIONS.keys())
            await interaction.response.send_message(
                f"❌ Invalid region. Valid options: `{regions_list}`", ephemeral=True
            )
            return
        await self.vc.edit(rtc_region=self.REGIONS[val])
        label = "Automatic" if val == "auto" else val
        embed = discord.Embed(description=f"🌐 Region set to **{label}**.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class TemplateModal(discord.ui.Modal, title="Save as Template"):
    template_name = discord.ui.TextInput(
        label="Template Name",
        placeholder="Enter a name for this template",
        min_length=1,
        max_length=50,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        data = load_data()
        guild_str = str(interaction.guild.id)
        if guild_str not in data:
            data[guild_str] = {}
        if "templates" not in data[guild_str]:
            data[guild_str]["templates"] = {}
        data[guild_str]["templates"][self.template_name.value] = {
            "name": self.vc.name,
            "user_limit": self.vc.user_limit,
            "bitrate": self.vc.bitrate // 1000,
        }
        save_data(data)
        embed = discord.Embed(
            description=f"📋 Template **{self.template_name.value}** saved!\nName: `{self.vc.name}`, Limit: `{self.vc.user_limit}`, Bitrate: `{self.vc.bitrate // 1000}kbps`",
            color=0x5865F2,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class InviteModal(discord.ui.Modal, title="Invite a Member"):
    user_input = discord.ui.TextInput(
        label="User ID or @mention",
        placeholder="Enter a User ID",
        min_length=1,
        max_length=30,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        raw = self.user_input.value.strip().replace("<@", "").replace(">", "").replace("!", "")
        try:
            user_id = int(raw)
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID.", ephemeral=True)
            return
        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message("❌ Member not found in this server.", ephemeral=True)
            return
        await self.vc.set_permissions(member, connect=True, view_channel=True)
        embed = discord.Embed(description=f"📨 **{member.display_name}** has been invited to join your channel.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        try:
            await member.send(f"📨 You've been invited to join **{self.vc.name}** in **{interaction.guild.name}**!")
        except Exception:
            pass


class BanModal(discord.ui.Modal, title="Ban a Member"):
    user_input = discord.ui.TextInput(
        label="User ID or @mention",
        placeholder="Enter a User ID",
        min_length=1,
        max_length=30,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        raw = self.user_input.value.strip().replace("<@", "").replace(">", "").replace("!", "")
        try:
            user_id = int(raw)
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID.", ephemeral=True)
            return
        if user_id == interaction.user.id:
            await interaction.response.send_message("❌ You cannot ban yourself.", ephemeral=True)
            return
        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message("❌ Member not found in this server.", ephemeral=True)
            return
        await self.vc.set_permissions(member, connect=False, view_channel=False)
        if member.voice and member.voice.channel and member.voice.channel.id == self.vc.id:
            await member.move_to(None)
        embed = discord.Embed(description=f"🔨 **{member.display_name}** has been banned from your channel.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class PermitModal(discord.ui.Modal, title="Permit a Member"):
    user_input = discord.ui.TextInput(
        label="User ID or @mention",
        placeholder="Enter a User ID",
        min_length=1,
        max_length=30,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        raw = self.user_input.value.strip().replace("<@", "").replace(">", "").replace("!", "")
        try:
            user_id = int(raw)
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID.", ephemeral=True)
            return
        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message("❌ Member not found in this server.", ephemeral=True)
            return
        await self.vc.set_permissions(member, connect=True, view_channel=True)
        embed = discord.Embed(description=f"✅ **{member.display_name}** has been permitted to join your channel.", color=0x5865F2)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class TransferModal(discord.ui.Modal, title="Transfer Ownership"):
    user_input = discord.ui.TextInput(
        label="User ID or @mention",
        placeholder="Enter a User ID",
        min_length=1,
        max_length=30,
    )

    def __init__(self, vc: discord.VoiceChannel):
        super().__init__()
        self.vc = vc

    async def on_submit(self, interaction: discord.Interaction):
        raw = self.user_input.value.strip().replace("<@", "").replace(">", "").replace("!", "")
        try:
            user_id = int(raw)
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID.", ephemeral=True)
            return
        if user_id == interaction.user.id:
            await interaction.response.send_message("❌ You already own this channel.", ephemeral=True)
            return
        member = interaction.guild.get_member(user_id)
        if not member:
            await interaction.response.send_message("❌ Member not found.", ephemeral=True)
            return
        if not (member.voice and member.voice.channel and member.voice.channel.id == self.vc.id):
            await interaction.response.send_message("❌ That member must be in your voice channel.", ephemeral=True)
            return
        temp = get_temp_channels(interaction.guild.id)
        temp[str(self.vc.id)]["owner"] = member.id
        save_temp_channels(interaction.guild.id, temp)
        await self.vc.edit(name=f"{member.display_name}'s VC")
        embed = discord.Embed(
            description=f"🔄 Channel ownership transferred to **{member.display_name}**.",
            color=0x5865F2,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ── Cog ───────────────────────────────────────────────────────────────────────

class TempVoice(commands.Cog):
    """Join2Create temp voice channel system."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TempVoiceView())

    def _build_interface_embed(self, guild: discord.Guild) -> discord.Embed:
        embed = discord.Embed(
            title="🎙️ Voice Channel Control Panel",
            description=(
                "Join the **➕ Create Voice** channel to get your own private voice channel!\n\n"
                "Once you have a channel, use the buttons below to manage it."
            ),
            color=0x5865F2,
        )
        embed.add_field(
            name="🔒 Lock / 🔓 Unlock",
            value="Prevent or allow others from joining.",
            inline=True,
        )
        embed.add_field(
            name="🙈 Hide / 👁️ Unhide",
            value="Make channel invisible or visible.",
            inline=True,
        )
        embed.add_field(
            name="👥 Limit",
            value="Set a member cap for your channel.",
            inline=True,
        )
        embed.add_field(
            name="📨 Invite / 🔨 Ban / ✅ Permit",
            value="Manage who can access your channel.",
            inline=True,
        )
        embed.add_field(
            name="✏️ Rename",
            value="Give your channel a custom name.",
            inline=True,
        )
        embed.add_field(
            name="🎧 Bitrate / 🌐 Region",
            value="Adjust audio quality and server region.",
            inline=True,
        )
        embed.add_field(
            name="📋 Template",
            value="Save current settings as a reusable template.",
            inline=True,
        )
        embed.add_field(
            name="💬 Chat",
            value="Create a private text channel for your VC.",
            inline=True,
        )
        embed.add_field(
            name="⏳ Waiting / 👑 Claim / 🔄 Transfer",
            value="Waiting room, claim an ownerless channel, transfer ownership.",
            inline=True,
        )
        embed.set_footer(text="OrinCron • TempVoice System")
        return embed

    # ── /setup ────────────────────────────────────────────────────────

    @app_commands.command(name="setup", description="Set up the TempVoice system in this server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild

        config = get_guild_config(guild.id)
        if config.get("category_id"):
            existing_cat = guild.get_channel(config["category_id"])
            if existing_cat:
                await interaction.followup.send(
                    f"❌ TempVoice is already set up! Category: {existing_cat.mention}\n"
                    f"Use `/resetup` to reconfigure.",
                    ephemeral=True,
                )
                return

        # Create category
        category = await guild.create_category(
            name="OrinCron",
            reason="TempVoice setup by OrinCron",
        )

        # Create interface text channel
        interface_channel = await guild.create_text_channel(
            name="interface",
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(
                    send_messages=False,
                    read_messages=True,
                    add_reactions=False,
                ),
                guild.me: discord.PermissionOverwrite(
                    send_messages=True,
                    read_messages=True,
                    manage_messages=True,
                ),
            },
            reason="TempVoice interface channel",
        )

        # Create generator voice channel
        generator_channel = await guild.create_voice_channel(
            name="➕ Create Voice",
            category=category,
            reason="TempVoice generator channel",
        )

        # Post interface embed with buttons
        embed = self._build_interface_embed(guild)
        view = TempVoiceView()
        msg = await interface_channel.send(embed=embed, view=view)

        # Save config
        set_guild_config(guild.id, {
            "category_id": category.id,
            "interface_channel_id": interface_channel.id,
            "interface_message_id": msg.id,
            "generator_channel_id": generator_channel.id,
            "temp_channels": {},
        })

        embed_reply = discord.Embed(
            title="✅ TempVoice Setup Complete!",
            description=(
                f"**Category:** {category.mention}\n"
                f"**Interface:** {interface_channel.mention}\n"
                f"**Generator:** {generator_channel.mention}\n\n"
                "Members can now join **➕ Create Voice** to get their own channel!"
            ),
            color=discord.Color.green(),
        )
        await interaction.followup.send(embed=embed_reply, ephemeral=True)

    @app_commands.command(name="resetup", description="Reset and re-run the TempVoice setup.")
    @app_commands.checks.has_permissions(administrator=True)
    async def resetup(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        config = get_guild_config(guild.id)

        # Delete old channels/category
        for key in ["interface_channel_id", "generator_channel_id"]:
            ch_id = config.get(key)
            if ch_id:
                ch = guild.get_channel(ch_id)
                if ch:
                    try:
                        await ch.delete()
                    except Exception:
                        pass

        cat_id = config.get("category_id")
        if cat_id:
            cat = guild.get_channel(cat_id)
            if cat:
                try:
                    await cat.delete()
                except Exception:
                    pass

        # Clear config
        set_guild_config(guild.id, {})

        # Run setup fresh
        await self.setup.callback(self, interaction)

    @app_commands.command(name="tvstatus", description="Show the TempVoice configuration for this server.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def tvstatus(self, interaction: discord.Interaction):
        config = get_guild_config(interaction.guild.id)
        if not config.get("category_id"):
            await interaction.response.send_message("❌ TempVoice is not set up. Use `/setup`.", ephemeral=True)
            return
        temp = config.get("temp_channels", {})
        embed = discord.Embed(title="TempVoice Status", color=0x5865F2)
        embed.add_field(name="Category", value=f"<#{config.get('category_id')}>", inline=True)
        embed.add_field(name="Interface", value=f"<#{config.get('interface_channel_id')}>", inline=True)
        embed.add_field(name="Generator", value=f"<#{config.get('generator_channel_id')}>", inline=True)
        embed.add_field(name="Active Temp Channels", value=str(len(temp)), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ── Voice state ───────────────────────────────────────────────────

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild
        config = get_guild_config(guild.id)
        if not config:
            return

        generator_id = config.get("generator_channel_id")
        category_id = config.get("category_id")
        temp = get_temp_channels(guild.id)

        # Member joined generator channel → create temp VC
        if after.channel and after.channel.id == generator_id:
            category = guild.get_channel(category_id)
            new_vc = await guild.create_voice_channel(
                name=f"{member.display_name}'s VC",
                category=category,
                reason=f"TempVoice for {member}",
            )
            await new_vc.set_permissions(
                member,
                connect=True,
                manage_channels=True,
                move_members=True,
                mute_members=True,
                deafen_members=True,
            )
            try:
                await member.move_to(new_vc)
            except Exception:
                await new_vc.delete()
                return
            temp[str(new_vc.id)] = {
                "owner": member.id,
                "text_channel": None,
                "waiting_enabled": False,
            }
            save_temp_channels(guild.id, temp)

        # Member left a temp channel → check if empty and delete
        if before.channel and str(before.channel.id) in temp:
            vc = before.channel
            if len(vc.members) == 0:
                ch_id = str(vc.id)
                info = temp.pop(ch_id, {})
                save_temp_channels(guild.id, temp)
                # Delete linked text channel if any
                text_ch_id = info.get("text_channel")
                if text_ch_id:
                    text_ch = guild.get_channel(text_ch_id)
                    if text_ch:
                        try:
                            await text_ch.delete()
                        except Exception:
                            pass
                try:
                    await vc.delete(reason="TempVoice empty")
                except Exception:
                    pass

    # ── Prefix commands (admin helpers) ──────────────────────────────

    @commands.command(name="tvsetup")
    @commands.has_permissions(administrator=True)
    async def prefix_setup(self, ctx):
        """Set up TempVoice via prefix command."""
        interaction_like = ctx
        embed = discord.Embed(
            description="Please use the slash command `/setup` to configure TempVoice.",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @commands.command(name="tvreset")
    @commands.has_permissions(administrator=True)
    async def prefix_reset(self, ctx):
        """Clear TempVoice data for this server."""
        set_guild_config(ctx.guild.id, {})
        embed = discord.Embed(
            description="✅ TempVoice data cleared. Use `/setup` to set it up again.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TempVoice(bot))
