from .gmtkcog import GmtkCog


async def setup(bot):
    await bot.add_cog(GmtkCog(bot))
