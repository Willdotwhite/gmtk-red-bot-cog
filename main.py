import discord
from discord import app_commands
from redbot.core import commands
from redbot.core.bot import Red

# =========================================================================
# CONFIGURATION
# =========================================================================
# List of Role IDs (integers) that are allowed to use these slash commands.
ALLOWED_ROLE_IDS = [
    1511691465544306820,
]

# List of channel names to listen in for auto-responses
TARGET_CHANNELS = ["general", "help", "support"]

# List of keywords that will trigger the auto-response
TARGET_KEYWORDS = ["help", "stuck", "error", "broken", "how to"]
# =========================================================================

class JamCommands(commands.Cog):
    """Game Jam Management Commands and Auto-Responders."""

    def __init__(self, bot: Red):
        self.bot = bot
        # Pre-process lists to lowercase for efficient case-insensitive matching
        self.target_channels = [c.lower() for c in TARGET_CHANNELS]
        self.target_keywords = [k.lower() for k in TARGET_KEYWORDS]

    async def _check_permissions(self, interaction: discord.Interaction) -> bool:
        """Helper to enforce Role ID restrictions on slash commands."""
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("❌ This command must be used in a server.", ephemeral=True)
            return False

        # Allow if the user has any of the target Role IDs OR has administrator privileges
        has_role = any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles)
        
        if not has_role and not interaction.user.guild_permissions.administrator:
            # Rejections are always ephemeral so chat doesn't get cluttered
            await interaction.response.send_message("❌ You do not have the required roles to use this command.", ephemeral=True)
            return False
            
        return True

    # =========================================================================
    # KEYWORD AUTO-RESPONDER (Listens in multiple channels for multiple words)
    # =========================================================================
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        # Check if the message is in one of the target channels
        if message.channel.name.lower() in self.target_channels:
            msg_lower = message.content.lower()
            # Check if any keyword exists in the message
            if any(keyword in msg_lower for keyword in self.target_keywords):
                try:
                    await message.reply(
                        "🤖 **Auto-Response**: It looks like you might need help! Please check the pinned FAQ channel.\n*(Deleting in 10s)*",
                        delete_after=10.0
                    )
                except discord.HTTPException:
                    pass

    @app_commands.command(name="ai", description="Print AI usage rules.")
    @app_commands.default_permissions()
    async def ai(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**AI Rules**: You must not use generative AI to make art or audio assets for your game, or your itch.io page. This will lead to your game being disqualified. Full rules are [on the itch.io page](https://itch.io/jam/gmtk-jam-2026)", ephemeral=False)

    @app_commands.command(name="jaminfo", description="Print general jam information.")
    @app_commands.default_permissions()
    async def jaminfo(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Jam Info**: All information you need about the jam can be found on itch.io: https://itch.io/jam/gmtk-jam-2026", ephemeral=False)

    @app_commands.command(name="jamruling", description="Print jam rules and criteria.")
    @app_commands.default_permissions()
    async def jamruling(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Jam Ruling**: Discord moderators can *not* make any ruling regarding jam rules, so if you are uncertain about something we ask you to read the jam rules and use your own judgement: https://itch.io/jam/gmtk-jam-2026\nIf you’re still unsure if something is OK or not, we recommend that you err on the side of safety and refrain from doing it! <:linkThumbsUp:948315490076487742>", ephemeral=False)

    @app_commands.command(name="itch", description="Print the itch.io submission link.")
    @app_commands.default_permissions()
    async def itch(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("<:gmtk:407473480703934464> https://itch.io/jam/gmtk-jam-2026 <:gmtk:407473480703934464>", ephemeral=False)

    @app_commands.command(name="hype", description="Print hype message/warning.")
    @app_commands.default_permissions()
    async def teamfinder(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Please keep hype, countdowns and spam to https://discord.com/channels/248204508960653312/1270435373666926613!**", ephemeral=False)

    @app_commands.command(name="teamfinder", description="Print team finding instructions.")
    @app_commands.default_permissions()
    async def teamfinder(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**If you're looking for a team, head over to https://findyourjam.team/gmtk and https://discord.com/channels/248204508960653312/1270438349114703983 !**", ephemeral=False)

    @app_commands.command(name="theme", description="Print jam theme info.")
    @app_commands.default_permissions()
    async def teamfinder(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("## **THE THEME FOR THE GMTK GAME JAME 2026 IS...**\n# *** ??? ***\n[Link to video here!](https://www.youtube.com/watch?v=z_kAvHKPWYo&ab_channel=GameMaker%27sToolkit)", ephemeral=False)

    @app_commands.command(name="health", description="Print health and wellness tips.")
    @app_commands.default_permissions()
    async def health(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("We strongly recommend you take care of yourself during the jam! Make sure to: sleep well, take regular breaks and stay on top of eating and drinking. You make a better game when you're healthy, not when you're crunching!", ephemeral=False)

    @app_commands.command(name="jamtips", description="Print useful jam tips.")
    @app_commands.default_permissions()
    async def jamtips(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("Here are some important tips for having a great jam! https://discord.com/channels/248204508960653312/1379068723809222787/1399378216002785391", ephemeral=False)

    @app_commands.command(name="jamstart", description="Print jam countdown timer.")
    @app_commands.default_permissions()
    async def jamtips(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**The jam starts at <t:1784739600:f> (<t:1784739600:R>).**\n**You can view the rules and sign up here: <https://itch.io/jam/gmtk-jam-2026>**\n**Please keep countdowns to https://discord.com/channels/248204508960653312/1270435373666926613!**", ephemeral=False)

    @app_commands.command(name="extension", description="Print extension info.")
    @app_commands.default_permissions()
    async def jamtips(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**There are NO PLANS for time extension this year!**\n**The jam ends when the timer on <https://itch.io/jam/gmtk-jam-2026> is up!**", ephemeral=False)

    @app_commands.command(name="jamend", description="Print extension info.")
    @app_commands.default_permissions()
    async def jamtips(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Submissions close on <t:1785085200:F> (<t:1785085200:R>).**\n**We strongly recommend you upload your game** ***before*** **the last hour! If something goes wrong in the last minutes of the jam, we will be unable assist you!**", ephemeral=False)

    @app_commands.command(name="build", description="Print game build instructions.")
    @app_commands.default_permissions()
    async def build(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Don't forget to plan for the time it takes to build and test your game!**\n**You can upload multiple builds of your game to itch.io and update your game submission, so make sure you submit early! You can freely change which game files are part of your submission** ***up until the jam deadline***, **even after you've submitted the game!**", ephemeral=False)

    @app_commands.command(name="extraextension", description="Print extra extension info.")
    @app_commands.default_permissions()
    async def build(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**To account for issues with late submissions, the jam has received an extra** ***1 hour*** **added to the original submission time. The final time is at <t:1754244000:t> <t:1754244000:R>!**\n# This is not time for you to add extra features or bugfix. This is to help those who had slow builds or issues with submitting to itch.io get their games in.\n**If you have successfully submitted your game, congratulations! We recommend you use this time to relax, you made it!**", ephemeral=False)

    @app_commands.command(name="gamelink", description="Print game submission link info.")
    @app_commands.default_permissions()
    async def gamelink(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Please do not link your itch.io game page outside of https://discord.com/channels/248204508960653312/1270438107296043122.**\n**If someone is requesting to play your game, please DM them instead.**", ephemeral=False)

    @app_commands.command(name="jamover", description="Print jam end info.")
    @app_commands.default_permissions()
    async def gamelink(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**The jam submission deadline is now over! It is no longer possible to upload or edit submissions to the jam. If you did not manage to get your game submitted in time there is unfortunately nothing we can do at this stage.**\n**DO NOT DELETE YOUR GAME FILES - IT WILL NOT LET YOU UPLOAD NEW ONES, AND WE ARE UNABLE TO RESTORE THEM IF YOU DO! YOU WILL BE DISQUALIFIED!**\nFeel free to edit your game's itch.io page, thumbnail and description, but do not add links to other builds of your game!", ephemeral=False)

    @app_commands.command(name="closing", description="Print closing info.")
    @app_commands.default_permissions()
    async def gamelink(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("<:linkConfetti:922817487295361124> **THE GMTK Game Jam is now over! Thank you everyone for participating! The server will be closing for non-patrons <t:1754740800:R>! See you next year! ** <:linkConfetti:922817487295361124> \nOr, if you want to keep hanging around, please consider becoming a GMTK patron and gain access to the discord all year round!", ephemeral=False)

    @app_commands.command(name="r4r", description="Print Rate 4 Rate info.")
    @app_commands.default_permissions()
    async def r4r(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**R4R (Rate for Rate)**: WORDS GO HERE PLS", ephemeral=False)

# Required RedBot Cog setup function
async def setup(bot: Red):
    await bot.add_cog(JamCommands(bot))

# =========================================================================
# LOCAL DEVELOPMENT RUNNER
# =========================================================================
# This block will ONLY run if you execute this script directly via Python.
# It uses a local mock environment rather than loading into the full RedBot.
if __name__ == "__main__":
    import logging
    from discord.ext import commands as dpy_commands
    
    # Configure basic logging to see commands/errors locally
    logging.basicConfig(level=logging.INFO)

    # --- LOCAL TEST CONFIGURATION ---
    LOCAL_BOT_TOKEN = "YOUR_REST_BOT_TOKEN_HERE"
    LOCAL_GUILD_ID = 1470708876998344861  # Replace with your local test server/guild ID

    class LocalDevBot(dpy_commands.Bot):
        def __init__(self):
            # Message content intent is required for the auto-responder to read messages
            intents = discord.Intents.default()
            intents.message_content = True 
            super().__init__(command_prefix="!", intents=intents)

        async def setup_hook(self):
            # Load the exact same Cog that RedBot will use
            await self.add_cog(JamCommands(self)) # type: ignore
            
            # Sync slash commands directly to your test guild for INSTANT updates.
            # (Global syncs normally take up to an hour; this avoids that)
            test_guild = discord.Object(id=LOCAL_GUILD_ID)
            self.tree.copy_global_to(guild=test_guild)
            await self.tree.sync(guild=test_guild)
            print(f"\n[LOCAL DEV] Commands synced directly to test guild: {LOCAL_GUILD_ID}")

        async def on_ready(self):
            print(f"\n[LOCAL DEV] Logged in successfully as {self.user}!")
            print("[LOCAL DEV] Ready for fast iteration. Press Ctrl+C to stop.\n")

    if LOCAL_BOT_TOKEN == "YOUR_TEST_BOT_TOKEN_HERE":
        print("\n❌ Please set LOCAL_BOT_TOKEN and LOCAL_GUILD_ID at the bottom of the script to run locally.\n")
    else:
        # Create and run our lightweight test bot
        local_bot = LocalDevBot()
        local_bot.run(LOCAL_BOT_TOKEN)