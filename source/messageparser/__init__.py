from .embed import *
from .component import *


class MessageParser():
    """
    embed = embeddings
    component = Components to click on
    """
    def __init__(self, msg):
        self.msg = msg
        self.embed = None if len(self.msg.embeds) < 1 else Embed(self.msg.embeds)
        self.component = None if len(self.msg.components) < 1 else Component(self.msg.components[0])
        #self.reaction = None if len(self.msg.reactions) < 1 else self.msg.reactions[0]
    
    
    @property
    def in_dms(self): return not self.msg.guild
    
    # --- ID --- #
    @property
    def user_id(self): return self.msg.author
    @property
    def channel_id(self): return self.msg.channel.id
    @property
    def guild_id(self): return self.msg.guild.id
    
    
    
    
    