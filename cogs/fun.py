import discord
from discord.ext import commands
from discord import app_commands
import random
import os

PREFIX = os.getenv("BOT_PREFIX", "+")

FACTS = [
    "Honey never spoils — archaeologists have found 3,000-year-old honey in Egyptian tombs.",
    "A group of flamingos is called a 'flamboyance'.",
    "Octopuses have three hearts and blue blood.",
    "The shortest war in history lasted only 38–45 minutes.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than a year on Venus.",
    "Hot water can freeze faster than cold water under certain conditions — this is the Mpemba effect.",
    "There are more possible iterations of a chess game than there are atoms in the observable universe.",
    "The average person walks about 100,000 miles in a lifetime — that's more than four times around the Earth.",
    "Wombat poop is cube-shaped.",
    "The human nose can detect over 1 trillion different scents.",
    "Sharks are older than trees — they've been around for about 450 million years.",
    "An ostrich's eye is bigger than its brain.",
    "A bolt of lightning is five times hotter than the surface of the sun.",
]

ROASTS = [
    "You're the reason they put instructions on shampoo bottles.",
    "I'd roast you, but my parents taught me not to burn trash.",
    "You're a grey sprinkle on a rainbow cupcake.",
    "If your brain were dynamite, there wouldn't be enough to blow your hat off.",
    "You're proof that even evolution makes mistakes.",
    "I'd give you a nasty look but you've already got one.",
    "Somewhere out there, a tree is tirelessly producing oxygen for you. You owe that tree an apology.",
    "You're like a cloud — when you disappear, it's a beautiful day.",
    "The only way you'll ever get laid is if you crawl up a chicken's butt and wait.",
    "You're not stupid; you just have bad luck thinking.",
]

COMPLIMENTS = [
    "You light up every room you walk into!",
    "Your smile could end world conflicts.",
    "You have the energy of a golden retriever on a sunny day.",
    "The world is genuinely a better place because you're in it.",
    "You're more fun than a pool full of rubber ducks.",
    "You have an incredible ability to make people feel valued.",
    "Your laugh is absolutely contagious in the best way.",
    "You're someone people can always count on.",
    "You're one of those rare people who makes everything more interesting.",
    "Talking to you is the highlight of anyone's day.",
]

EIGHT_BALL_RESPONSES = [
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.",
    "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
    "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
    "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
    "Don't count on it.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful.",
]

SLOTS_SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]


class Fun(commands.Cog):
    """Fun and entertainment commands."""

    def __init__(self, bot):
        self.bot = bot

    # ── 8Ball ─────────────────────────────────────────────────────────

    @commands.command(name="8ball", aliases=["8b"])
    async def eight_ball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question."""
        response = random.choice(EIGHT_BALL_RESPONSES)
        positive = EIGHT_BALL_RESPONSES[:10]
        color = 0x57F287 if response in positive else (0xED4245 if response in EIGHT_BALL_RESPONSES[15:] else 0xFEE75C)
        embed = discord.Embed(color=color)
        embed.add_field(name="🎱 Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question.")
    @app_commands.describe(question="Your yes/no question")
    async def slash_eight_ball(self, interaction: discord.Interaction, question: str):
        response = random.choice(EIGHT_BALL_RESPONSES)
        embed = discord.Embed(color=0x5865F2)
        embed.add_field(name="🎱 Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Roll ──────────────────────────────────────────────────────────

    @commands.command(name="roll", aliases=["dice"])
    async def roll(self, ctx, sides: int = 6):
        """Roll a dice. Default is 6-sided."""
        if sides < 2:
            await ctx.send("❌ A dice must have at least 2 sides.")
            return
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling a **d{sides}**...\n\nYou rolled **{result}**!",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="roll", description="Roll a dice.")
    @app_commands.describe(sides="Number of sides (default 6)")
    async def slash_roll(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 2:
            await interaction.response.send_message("❌ A dice must have at least 2 sides.", ephemeral=True)
            return
        result = random.randint(1, sides)
        embed = discord.Embed(title="🎲 Dice Roll", description=f"Rolling a **d{sides}**...\n\nYou rolled **{result}**!", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Flip ──────────────────────────────────────────────────────────

    @commands.command(name="flip", aliases=["coin"])
    async def flip(self, ctx):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        emoji = "🪙"
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"**{result}!**",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="flip", description="Flip a coin.")
    async def slash_flip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(title="🪙 Coin Flip", description=f"**{result}!**", color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Rock Paper Scissors ───────────────────────────────────────────

    @commands.command(name="rps")
    async def rps(self, ctx, choice: str):
        """Play Rock Paper Scissors."""
        choices = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        choice = choice.lower()
        if choice not in choices:
            await ctx.send("❌ Choose: `rock`, `paper`, or `scissors`.")
            return
        bot_choice = random.choice(list(choices.keys()))
        wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if choice == bot_choice:
            result = "It's a **tie**!"
            color = 0xFEE75C
        elif wins[choice] == bot_choice:
            result = "You **win**! 🎉"
            color = 0x57F287
        else:
            result = "You **lose**! 😢"
            color = 0xED4245
        embed = discord.Embed(title="✂️ Rock Paper Scissors", color=color)
        embed.add_field(name="Your pick", value=f"{choices[choice]} {choice.capitalize()}", inline=True)
        embed.add_field(name="My pick", value=f"{choices[bot_choice]} {bot_choice.capitalize()}", inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="rps", description="Play Rock Paper Scissors against the bot.")
    @app_commands.describe(choice="rock, paper, or scissors")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors"),
    ])
    async def slash_rps(self, interaction: discord.Interaction, choice: str):
        choices = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        bot_choice = random.choice(list(choices.keys()))
        wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if choice == bot_choice:
            result, color = "It's a **tie**!", 0xFEE75C
        elif wins[choice] == bot_choice:
            result, color = "You **win**! 🎉", 0x57F287
        else:
            result, color = "You **lose**! 😢", 0xED4245
        embed = discord.Embed(title="✂️ Rock Paper Scissors", color=color)
        embed.add_field(name="Your pick", value=f"{choices[choice]} {choice.capitalize()}", inline=True)
        embed.add_field(name="My pick", value=f"{choices[bot_choice]} {bot_choice.capitalize()}", inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Choose ────────────────────────────────────────────────────────

    @commands.command(name="choose")
    async def choose(self, ctx, *, options: str):
        """Choose between options separated by | or commas."""
        if "|" in options:
            choices = [o.strip() for o in options.split("|") if o.strip()]
        else:
            choices = [o.strip() for o in options.split(",") if o.strip()]
        if len(choices) < 2:
            await ctx.send("❌ Provide at least 2 options separated by `|` or `,`.")
            return
        pick = random.choice(choices)
        embed = discord.Embed(
            title="🎯 I Choose...",
            description=f"**{pick}**",
            color=0x5865F2,
        )
        embed.set_footer(text=f"From: {', '.join(choices)}")
        await ctx.send(embed=embed)

    # ── Reverse ───────────────────────────────────────────────────────

    @commands.command(name="reverse")
    async def reverse(self, ctx, *, text: str):
        """Reverse text."""
        embed = discord.Embed(
            title="🔁 Reversed",
            description=text[::-1],
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    # ── Mock ──────────────────────────────────────────────────────────

    @commands.command(name="mock")
    async def mock(self, ctx, *, text: str):
        """MoCkIfY tExT."""
        result = "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
        embed = discord.Embed(title="🤡 Mocked", description=result, color=0x5865F2)
        await ctx.send(embed=embed)

    # ── Rate ──────────────────────────────────────────────────────────

    @commands.command(name="rate")
    async def rate(self, ctx, *, thing: str):
        """Rate something out of 10."""
        score = random.randint(0, 10)
        bar = "█" * score + "░" * (10 - score)
        embed = discord.Embed(
            title=f"⭐ Rating: {thing[:50]}",
            description=f"**{score}/10**\n`{bar}`",
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    # ── Ship ──────────────────────────────────────────────────────────

    @commands.command(name="ship")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        """Ship two users together."""
        user2 = user2 or ctx.author
        score = random.randint(0, 100)
        bar = "❤️" * (score // 10) + "🖤" * (10 - score // 10)
        embed = discord.Embed(
            title="💘 Ship Meter",
            description=f"**{user1.display_name}** + **{user2.display_name}**\n\n{bar}\n\n**{score}%** compatibility!",
            color=0xFF6B9D,
        )
        await ctx.send(embed=embed)

    # ── Fact ──────────────────────────────────────────────────────────

    @commands.command(name="fact")
    async def fact(self, ctx):
        """Get a random fun fact."""
        embed = discord.Embed(
            title="💡 Fun Fact",
            description=random.choice(FACTS),
            color=0x5865F2,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="fact", description="Get a random fun fact.")
    async def slash_fact(self, interaction: discord.Interaction):
        embed = discord.Embed(title="💡 Fun Fact", description=random.choice(FACTS), color=0x5865F2)
        await interaction.response.send_message(embed=embed)

    # ── Roast ─────────────────────────────────────────────────────────

    @commands.command(name="roast")
    async def roast(self, ctx, member: discord.Member = None):
        """Roast a member."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"🔥 Roasting {member.display_name}",
            description=random.choice(ROASTS),
            color=0xED4245,
        )
        await ctx.send(embed=embed)

    # ── Compliment ────────────────────────────────────────────────────

    @commands.command(name="compliment")
    async def compliment(self, ctx, member: discord.Member = None):
        """Compliment a member."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"💐 Complimenting {member.display_name}",
            description=random.choice(COMPLIMENTS),
            color=0x57F287,
        )
        await ctx.send(embed=embed)

    # ── Slots ─────────────────────────────────────────────────────────

    @commands.command(name="slots")
    async def slots(self, ctx):
        """Play the slot machine."""
        s1, s2, s3 = [random.choice(SLOTS_SYMBOLS) for _ in range(3)]
        if s1 == s2 == s3:
            result = "🎉 **JACKPOT!** You matched all three!"
            color = 0xFFD700
        elif s1 == s2 or s2 == s3 or s1 == s3:
            result = "✨ **Two of a kind!** Not bad!"
            color = 0x57F287
        else:
            result = "❌ No match. Better luck next time!"
            color = 0xED4245
        embed = discord.Embed(
            title="🎰 Slot Machine",
            description=f"[ {s1} | {s2} | {s3} ]\n\n{result}",
            color=color,
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="slots", description="Play the slot machine.")
    async def slash_slots(self, interaction: discord.Interaction):
        s1, s2, s3 = [random.choice(SLOTS_SYMBOLS) for _ in range(3)]
        if s1 == s2 == s3:
            result, color = "🎉 **JACKPOT!** You matched all three!", 0xFFD700
        elif s1 == s2 or s2 == s3 or s1 == s3:
            result, color = "✨ **Two of a kind!** Not bad!", 0x57F287
        else:
            result, color = "❌ No match. Better luck next time!", 0xED4245
        embed = discord.Embed(title="🎰 Slot Machine", description=f"[ {s1} | {s2} | {s3} ]\n\n{result}", color=color)
        await interaction.response.send_message(embed=embed)

    # ── ASCII ─────────────────────────────────────────────────────────

    @commands.command(name="ascii")
    async def ascii_art(self, ctx, *, text: str):
        """Simple block-letter ASCII art."""
        if len(text) > 20:
            await ctx.send("❌ Text too long (max 20 characters).")
            return
        big = " ".join(text.upper())
        embed = discord.Embed(title="🔡 ASCII", description=f"```{big}```", color=0x5865F2)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
