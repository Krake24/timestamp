import disnake



class TimeChange(disnake.ui.Button):
    def __init__(self, func, label, style: disnake.ButtonStyle):
        super().__init__(
            label=label,
            style=style
        )
        self.func=func

    async def callback(self, inter: disnake.MessageInteraction):
        timestamp = int(inter.message.content.replace("<t:","").replace(">",""))
        await inter.response.edit_message(f"<t:{self.func(timestamp)}>")


