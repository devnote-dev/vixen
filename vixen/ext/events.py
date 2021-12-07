from discord import Activity
from discord.enums import ActivityType
from discord.ext.commands import Cog, Bot


class Events(Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        print('Vixen is ready!')
        await self.bot.change_presence(
            status='idle',
            activity=Activity(name='foxes ᓚᘏᗢ', type=ActivityType.watching)
        )


def setup(bot):
    bot.add_cog(Events(bot))
