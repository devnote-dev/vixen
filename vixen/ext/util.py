from discord.errors import Forbidden
from discord.ext.commands import Cog, Bot, command, Context


class Util(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
    
    @command(
        description='Index a specific field in a message embed or attachment',
        usage='index <message id> <type>'
    )
    async def index(self, ctx: Context, _id: int, _type: str):
        try:
            message = await ctx.fetch_message(_id)
        except Forbidden:
            return await ctx.send('I am missing __View Channel History__ permissions for this channel!')
        except:
            return await ctx.send('Message not found!')
        
        if len(message.embeds) and len(message.attachments):
            await ctx.send(
                'This message has embeds and attachments, which do you want to index?'
                '\nType "embeds" or "attachments"'
            )
            res = self.bot.wait_for('message', check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
            if res.content.lower() in ('emb', 'embed', 'embeds'):
                pass
            elif res.content.lower() in ('att', 'atts', 'attachment', 'attachments'):
                pass
            else:
                return await ctx.send('Invalid type option!')
    
    def run_embeds(self, ctx):
        # TODO
        pass
    
    def run_atts(self, ctx):
        # TODO
        pass
