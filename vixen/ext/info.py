from discord.embeds import Embed
from discord.member import Member
from discord.utils import find
from discord.ext.commands import Cog, Bot, command
from typing import Union


class Info(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
    
    @command(description='Sends info about a user', aliases=['user', 'ui'])
    async def userinfo(self, ctx, user: Union[int, str, Member] = None):        
        if user is None:
            user = ctx.author
        else:
            if isinstance(user, Member):
                pass
            elif isinstance(user, str):
                user = find(lambda m: user.lower() in m.name.lower(), ctx.guild.members)
            
            else:
                user = ctx.guild.get_member(user)
                if user is None:
                    try:
                        user = await ctx.guild.fetch_member(user)
                    except:
                        pass
        
        if user is None:
            return await ctx.reply('User not found! `▱ᗢ')
        
        print(type(user), user)
        colour = user.colour if isinstance(user, Member) else 0x2F3136
        embed = Embed(
            title=('Bot' if getattr(user, 'bot', False) is True else 'User') +f': {str(user)}',
            colour=colour
        ).set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name='ID', value=user.id)
        embed.add_field(name='Images', value=f'- [Avatar]'+ (f'\n[Banner]' if user.banner is not None else ''))
        # embed.add_field(name='Created At', value='<t:%i>' % int(user._user.created_at.microsecond) / 1000)
        if (user.banner is not None): embed.set_image(url=user.banner.url)
        
        return await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
