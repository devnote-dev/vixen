from discord.ext.commands import Cog, Bot, command


class General(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
    
    @command(description='Pings the foxes')
    async def ping(self, ctx):
        msg = await ctx.send('PONG!')
        return await msg.edit('Pong! ᓚᘏᗢ\nWS: %ims\nAPI: %ims' % (
            round(self.bot.latency * 1000),
            (msg.created_at.microsecond - ctx.message.created_at.microsecond) / 1000
        ))


def setup(bot):
    bot.add_cog(General(bot))
