from discord.ext.commands import Bot
from os import listdir
from json import load


class Vixen(Bot):
    def __init__(self) -> None:
        super().__init__()
        with open('./config.json') as file:
            self.config = load(file)
            file.close()
            self.owner_ids = set(self.config['owners'])
            self.command_prefix = self.config['prefix']
    
    def run(self):
        for ext in listdir('./vixen/ext/'):
            if not ext.endswith('.py'):
                continue
            
            self.load_extension('vixen.ext.%s' % ext[:-3])
        
        super().run(self.config['token'])
