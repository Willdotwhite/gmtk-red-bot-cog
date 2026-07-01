import discord
import os
import logging
from discord import app_commands
from discord.ext import commands

# =========================================================================
# CONFIGURATION
# =========================================================================
# List of Role IDs (integers) that are allowed to use these slash commands.
ALLOWED_ROLE_IDS = [
    307496422150897671,  # Mark
    321298669741670400,  # Server mods
    977139806784073768,  # Chat mods
]


class JamCommands(commands.Cog):
    """Game Jam Management Commands and Auto-Responders."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
    # SLASH COMMANDS
    # =========================================================================
    @app_commands.command(name="ai", description="Print AI usage rules.")
    async def cmd_ai(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**AI Rules**: You _must not use generative AI_ for any part of your game or itch.io page - ideas, art, code, anything. This goes against the idea of the jam, and will lead to your game being disqualified.\nFull rules are on the itch.io page: <https://itch.io/jam/gmtk-jam-2026>\n-# This is non-negotiable - arguing for it or attacking the rule will get you muted.", ephemeral=False)

    @app_commands.command(name="jaminfo", description="Print general jam information.")
    async def cmd_jaminfo(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Jam Info**: All information you need about the jam can be found on itch.io: <https://itch.io/jam/gmtk-jam-2026>", ephemeral=False)

    @app_commands.command(name="jamruling", description="Print jam rules and criteria.")
    async def cmd_jamruling(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Jam Ruling**: Discord moderators can *not* make any ruling regarding jam rules, so if you are uncertain about something we ask you to read the jam rules and use your own judgement: <https://itch.io/jam/gmtk-jam-2026>\nIf you’re still unsure if something is OK or not, we recommend that you err on the side of safety and refrain from doing it! <:linkThumbsUp:948315490076487742>", ephemeral=False)

    @app_commands.command(name="itch", description="Print the itch.io submission link.")
    async def cmd_itch(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("<:gmtk:407473480703934464> <https://itch.io/jam/gmtk-jam-2026> <:gmtk:407473480703934464>", ephemeral=False)

    @app_commands.command(name="hype", description="Print hype message/warning.")
    async def cmd_hype(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Please keep hype, countdowns, and spam to https://discord.com/channels/248204508960653312/1520881894328238141!**", ephemeral=False)

    @app_commands.command(name="teamfinder", description="Print team finding instructions.")
    async def cmd_teamfinder(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**If you're looking for a team, head over to https://findyourjam.team/gmtk and https://discord.com/channels/248204508960653312/1520884363171201074!**", ephemeral=False)

    @app_commands.command(name="theme", description="Print jam theme info.")
    async def cmd_theme(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**The theme for the GMTK Game Jam 2026 will be revealed closer to the start of the jam! Stay tuned!", ephemeral=False)
            # await interaction.response.send_message("## **THE THEME FOR THE GMTK GAME JAM 2026 IS...**\n# *** ??? ***\n[Link to video here!]()", ephemeral=False)

    @app_commands.command(name="health", description="Print health and wellness tips.")
    async def cmd_health(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("We strongly recommend you take care of yourself during the jam! Make sure to: sleep well, take regular breaks and stay on top of eating and drinking. :apple: :cup_with_straw: You make a better game when you're healthy, not when you're crunching!", ephemeral=False)

    @app_commands.command(name="jamtips", description="Print useful jam tips.")
    async def cmd_jamtips(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("Here are some important tips for having a great jam! https://discord.com/channels/248204508960653312/1520882478792048650/1521767562784800838", ephemeral=False)

    @app_commands.command(name="jamstart", description="Print jam countdown timer.")
    async def cmd_jamstart(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**The jam starts at <t:1784739600:f> (<t:1784739600:R>).**\n**You can view the rules and sign up here: <https://itch.io/jam/gmtk-jam-2026>**\n**Please keep countdowns to https://discord.com/channels/248204508960653312/1520881894328238141!**", ephemeral=False)

    @app_commands.command(name="extension", description="Print extension info.")
    async def cmd_extension(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**There are NO PLANS for time extension this year!**\n**The jam ends when the timer on <https://itch.io/jam/gmtk-jam-2026> is up!**", ephemeral=False)

    @app_commands.command(name="jamend", description="Print extension info.")
    async def cmd_jamend(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Submissions close on <t:1785085200:F> (<t:1785085200:R>).**\n**We strongly recommend you upload your game** ***before*** **the last hour! If something goes wrong in the last minutes of the jam, we will be unable assist you!**", ephemeral=False)

    @app_commands.command(name="build", description="Print game build instructions.")
    async def cmd_build(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Don't forget to plan for the time it takes to build and test your game!**\n**You can upload multiple builds of your game to itch.io and update your game submission, so make sure you submit early! You can freely change which game files are part of your submission** ***up until the jam deadline***, **even after you've submitted the game!**", ephemeral=False)

    @app_commands.command(name="extraextension", description="Print extra extension info.")
    async def cmd_extraextension(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**To account for issues with late submissions, the jam has received an extra** ***1 hour*** **added to the original submission time. The final time is at <t:1785088800:t> <t:1785088800:R>!**\n# This is not time for you to add extra features or bugfix. This is to help those who had slow builds or issues with submitting to itch.io get their games in.\n**If you have successfully submitted your game, congratulations! We recommend you use this time to relax, you made it!**", ephemeral=False)

    @app_commands.command(name="gamelink", description="Print game submission link info.")
    async def cmd_gamelink(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**Please do not link your itch.io game page outside of https://discord.com/channels/248204508960653312/1520884041472282664.**\n**If someone is requesting to play your game, please DM them instead.\nDM-ing people your game without warning will get you banned.**", ephemeral=False)

    @app_commands.command(name="jamover", description="Print jam end info.")
    async def cmd_jamover(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**The jam submission deadline is now over! It is no longer possible to upload or edit submissions to the jam. If you did not manage to get your game submitted in time there is unfortunately nothing we can do at this stage.**\n**DO NOT DELETE YOUR GAME FILES - IT WILL NOT LET YOU UPLOAD NEW ONES, AND WE ARE UNABLE TO RESTORE THEM IF YOU DO! YOU WILL BE DISQUALIFIED!**\nFeel free to edit your game's itch.io page, thumbnail and description, but do not add links to other builds of your game!\nIf you had a technical issue, we are unable to resolve it and you need to raise a support ticket with itch.", ephemeral=False)

    @app_commands.command(name="closing", description="Print closing info.")
    async def cmd_closing(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("<:linkConfetti:922817487295361124> **THE GMTK Game Jam is now over! Thank you everyone for participating! The server will be closing for non-patrons <t:1785668400:R>! See you next year! ** <:linkConfetti:922817487295361124> \nOr, if you want to keep hanging around, please consider becoming a GMTK patron and gain access to the discord all year round!", ephemeral=False)

    @app_commands.command(name="r4r", description="Print Rate-4-Rate info.")
    async def cmd_r4r(self, interaction: discord.Interaction):
        if await self._check_permissions(interaction):
            await interaction.response.send_message("**R4R (Rate-for-Rate)**: R4R isn't allowed in this server - check out https://discord.com/channels/248204508960653312/1520891797335707901 for info.", ephemeral=False)


# =========================================================================
# BOT SETUP & EXECUTION
# =========================================================================
class PlainDiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required for the auto-responder
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Load the commands
        await self.add_cog(JamCommands(self))
        
        # Command Syncing Logic
        guild_id = os.environ.get("GUILD_ID")
        if guild_id:
            try:
                target_guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=target_guild)
                await self.tree.sync(guild=target_guild)
                logging.info(f"Synced slash commands directly to guild: {guild_id}")
            except Exception as e:
                logging.error(f"Failed to sync commands to guild {guild_id}: {e}")
        else:
            await self.tree.sync()
            logging.info("Synced slash commands globally. (Note: Global syncs can take up to 1 hour to appear in Discord client).")

    async def on_ready(self):
        logging.info(f"Logged in successfully as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    
    # Securely retrieve the token from the environment
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    if not BOT_TOKEN:
        logging.critical("BOT_TOKEN environment variable is not set. Exiting.")
        exit(1)

    bot = PlainDiscordBot()
    bot.run(BOT_TOKEN)
