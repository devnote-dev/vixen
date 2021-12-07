from discord.ext.commands import Cog, Bot, command, is_owner


class Admin(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
    
    @command()
    @is_owner()
    async def reload(self, ctx, cog: str):
        cog = cog.title()
        if not self.bot.get_cog(cog):
            return await ctx.reply('Cog not found!')
        
        self.bot.unload_extension('vixen.ext.%s' % cog.lower())
        self.bot.load_extension('vixen.ext.%s' % cog.lower())
        return await ctx.reply(f'Reloaded the `{cog}` cog!')


def setup(bot):
    bot.add_cog(Admin(bot))
