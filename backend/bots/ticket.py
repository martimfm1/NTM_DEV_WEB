import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot = commands.Bot(command_prefix="0001", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Desenvolvido por NTM DEV")
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'{bot.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot.change_presence(activity=activity)


class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_option:
            ticket_name = f"{self.ticket_option}"
            role_to_mention = discord.utils.get(interaction.guild.roles, name="NTM DEV")
            role_mention = role_to_mention.mention
            user = interaction.user
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket {self.ticket_option}. Send all possible information about your case and wait until the {role_mention} reply."
            if self.ticket_text:
                ticket_message += f"\n\n{self.ticket_text}"
            if self.image_url:
                ticket_message += f"\n{self.image_url}"
            await ticket_channel.send(ticket_message)
            await interaction.response.send_message(f"You opened the ticket {self.ticket_option} in {ticket_channel.mention}", ephemeral=True)
            view = discord.ui.View()
            close_button = CloseButton("Close", ticket_channel.id)
            view.add_item(close_button)
            await ticket_channel.send("Click the button below to close this ticket:", view=view)
        else:
            await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        ticket_channel = interaction.guild.get_channel(self.channel_id)
        if ticket_channel:
            await ticket_channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒", description='Ticket for shopping'),
            discord.SelectOption(value="support", label="Support", emoji="💳", description='Ticket for support'),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔", description='Ticket for doubts'),
            discord.SelectOption(value="bugs", label="Bugs", emoji="🐌", description='Ticket for bugs'),
            discord.SelectOption(value='partners', label='Partners', emoji='🤝', description='Ticket to close partnership')
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] in ["shopping", "support", "doubts", "bugs", 'partners']:
            selected_option = self.values[0]
            await interaction.response.defer()
            view = discord.ui.View()
            open_button = TicketButton(label=f"Open {selected_option} Ticket", ticket_option=selected_option)
            view.add_item(open_button)
            await interaction.followup.send(content=f"Press the button below to open a {selected_option} ticket", view=view, ephemeral=True)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

@bot.command()
async def ticket(ctx, interaction = None):
    embed = discord.Embed(
        title="**SERVICE**",
        description="➡️ - To open a ticket, select one of the options below:",
        color=0x2f336b
    )
    embed.add_field(name="", value="```ㅤㅤㅤㅤㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
    embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
    embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
    embed.set_image(url="https://i.imgur.com/b1dqBpP.png")
    message = await ctx.send(embed=embed)
    await ctx.send(view=PersistentView())
    
    if any(role.id == 1303726904569892884 for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!")
    else:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
