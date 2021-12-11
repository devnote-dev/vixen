from discord.embeds import Embed
from discord.ext.commands import Cog, Bot, errors, BotMissingPermissions
from traceback import format_exception


class Errors(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        if bot.config.get('log_channel') is None:
            raise KeyError('log channel is required')
        
        self.bot = bot
        self.channel = bot.get_channel(self.bot.config['log_channel'])
    
    def embed(self, title: str, message: str):
        return Embed(
            title=title,
            description=message,
            colour=0xe05151
        )
    
    async def log_error(self, err, ctx):
        path: str
        if ctx is None:
            path = '/'
        else:
            path = (str(ctx.guild.id) if ctx.guild is not None else 'DM') +'/'+ str(ctx.channel.id)
        
        show_trace = self.bot.config['log_trace']
        if show_trace:
            stack = format_exception(type(err), err, err.__traceback__)
            stack.pop() if len(stack) > 1 else None
        
        print(
            'ERROR! %s\n%s\n\nPATH: %s\n%s' % (
                err.__class__.__name__, str(err), path,
                'TRACE:\n%s\n' % '\n'.join(stack) if show_trace else ''
            )
        )
        if self.channel is None:
            return
        
        return await self.channel.send(
            embed=self.embed(
                f'Error: {err.__class__.__name__}',
                '%s\n\n**Path:** %s\n```\n%s\n```' % (
                    str(err), path, '\n'.join(stack) if show_trace else 'Stack Trace Disabled'
                )
            )
        )
    
    @Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, (errors.CommandNotFound, errors.DisabledCommand)):
            return
        
        if isinstance(err, errors.MissingRequiredArgument):
            arg = str(err).split('is')[0][:-1]
            count = len(ctx.command.name)
            if len(ctx.command.params) > 3:
                for p in ctx.command.params:
                    count += len(p)
                
                count -= len(arg)
            
            spaces = [' ' for _ in range(count + 2)]
            bar = ''.join(spaces) + ('^' * len(arg))
            
            return await ctx.reply(
                'Missing Arguments! `▱ᗢ\n```\n%s %s\n%s\n```' %
                (ctx.command, ctx.command.signature, bar)
            )
        
        if isinstance(err, BotMissingPermissions):
            if 'send_messages' in err.missing_permissions:
                try:
                    return await ctx.author.send(
                        embed=self.embed(
                            'Missing Permissions',
                            'I don\'t have the __Send Messages__ permission for that channel!'
                            ' If you\'re sure that I do, contact support about this using'
                            ' `@Vixen support`.'
                        )
                    )
                except:
                    pass
            
            if (
                'embed_links' in err.missing_permissions or
                'attach_files' in err.missing_permissions
            ):
                return await ctx.reply(
                    '**Error!**\nI don\'t have __Embed Links__ or __Attach Files__ permissions'
                    ' for this channel!'
                )
        
        try:
            await ctx.reply(
                'An unknown error occurred! My owner has been notified, please'
                ' contact support if this keeps happening using `@Vixen support`.'
            )
        except:
            pass
        
        return await self.log_error(err, ctx)


def setup(bot):
    bot.add_cog(Errors(bot))
