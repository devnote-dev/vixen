from discord.embeds import Embed
from discord.ext.commands import Cog, Bot, command
import os


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
    
    @command(description='Sends Vixen\'s status')
    async def status(self, ctx):
        embed = Embed(
            title='Vixen Status',
            color=0xe1c4b9
        ).set_author(name='ᓚᘏᗢ', icon_url=self.bot.user.display_avatar.url)
        embed.add_field(name='Uptime', value='<t:%d> (<t:%d:R>)' % (self.bot.uptime, self.bot.uptime), inline=False)
        embed.add_field(name='Servers', value=str(len(self.bot.guilds)))
        embed.add_field(name='Channels', value=len(self.bot.private_channels))
        embed.add_field(name='Process', value='%iMB' % os.cpu_count())
        return await ctx.send(embed=embed)
    
    @command(description='Smart math calculating stuff', aliases=['ma', 'm'])
    async def math(self, ctx, *, args: str):
        try:
            res = eval(args)
            return await ctx.send('```\n%s\n```' % str(res))
        except Exception as e:
            return await ctx.send('```\n%s\n```' % repr(e))


def setup(bot):
    bot.add_cog(General(bot))
