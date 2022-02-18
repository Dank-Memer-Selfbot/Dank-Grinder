from discord.errors import DiscordException
import discord
class Component():
    def __init__(self, compo):
        self.compo = compo
        self.compo_child = compo.children
        self.labels = [comp.label for comp in compo.children] if any(hasattr(compo,'label') for compo in self.compo.children) else None
        
    async def click_label(self,label:str):
        if self.labels:
            if label in self.labels:
                index = self.labels.index(label)
                try: 
                    await self.compo_child[index].click()
                except discord.errors.DiscordServerError:
                    print("discord fking lagged bro")
            else:
                print(f"The label [{label}] is not found in [{self.labels}]")