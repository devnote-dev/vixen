from discord.flags import Intents
from discord.mentions import AllowedMentions
from discord.ext.commands import Bot
from os import listdir
from json import load
from time import time


class Vixen(Bot):
    def __init__(self) -> None:
        super().__init__(intents=Intents(guilds=True, messages=True, members=True))
        with open('./config.json') as file:
            self.config = load(file)
            file.close()
            self.owner_ids = set(self.config['owners'])
            self.command_prefix = self.config['prefix']
        
        self.uptime: float
        self.allowed_mentions = AllowedMentions(everyone=False, users=False, roles=False)
    
    def run(self):
        for ext in listdir('./vixen/ext/'):
            if not ext.endswith('.py'):
                continue
            
            self.load_extension('vixen.ext.%s' % ext[:-3])
        
        self.uptime = time()
        super().run(self.config['token'])
