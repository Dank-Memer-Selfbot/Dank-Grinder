import rich, discord, yaml
from discord.ext import commands

# Personal files
from messageparser import *



# --- Constants --- #
class InitBot():
    def __init__(self):
        self.config = self.get_config()
        self.token = self.config['token']
        self.ch_cmd = self.config['grinderConfig']['channel']
        
        # --- Initialize bot --- #
        bot = DiscordBot(self.ch_cmd)
        bot.run(self.token)
    
    def get_config(self):
        with open('config2.yml', "r", encoding="utf-8") as config_file:
            config = yaml.load(config_file,Loader=yaml.FullLoader)
        return config
        

class DiscordBot(commands.Bot):
    def __init__(self, ch_cmd):
        super().__init__(command_prefix="")
        self.ch_cmd = ch_cmd

    async def on_ready(self):
        print(f"Bot {self.user} is connected to server.")
    
    # --- Events --- #
    async def on_message(self, message):
        msg = MessageParser(message)
        
        if msg.user_id() == self.user:
            return
        
        if msg.in_dms():
            print("this message is in dms")
        else:
            
            if msg.embed:
                title = msg.embed.title
                desc = msg.embed.description
                
            if msg.component and msg.channel_id() == self.ch_cmd:
                if msg.component.labels:
                    print(msg.component.labels)
                    # Lets say pls hl
                    await msg.component.click_label('Lower')
                    
        return
        
        
        

if __name__ == '__main__':
    b = InitBot()