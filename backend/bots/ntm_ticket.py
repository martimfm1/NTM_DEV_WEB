import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot = commands.Bot(command_prefix='0001', intents=intents)

class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label, custom_id=f"ticket:{ticket_option}")
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        role_to_mention = discord.utils.get(guild.roles, name="NTM DEV")

        if not self.ticket_option:
            return await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

        if not role_to_mention:
            return await interaction.response.send_message("Support role 'NTM DEV' not found.", ephemeral=True)

        ticket_name = f"{self.ticket_option}-{user.name.lower()}"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        try:
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
        except discord.Forbidden:
            return await interaction.response.send_message("I don't have permission to create channels.", ephemeral=True)
        except Exception as e:
            return await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

        role_mention = role_to_mention.mention
        ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket **{self.ticket_option}**.\nSend all possible information about your case and wait for {role_mention} to reply."

        if self.ticket_text:
            ticket_message += f"\n\n{self.ticket_text}"
        if self.image_url:
            ticket_message += f"\n{self.image_url}"

        await ticket_channel.send(ticket_message)

        view = discord.ui.View()
        close_button = CloseButton("Close", ticket_channel.id)
        view.add_item(close_button)
        await ticket_channel.send("Click the button below to close this ticket:", view=view)

        await interaction.response.send_message(f"You opened the **{self.ticket_option}** ticket in {ticket_channel.mention}", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label, custom_id=f"close:{channel_id}")
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        channel = interaction.guild.get_channel(self.channel_id)
        if not channel:
            return await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

        try:
            await channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete this channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error deleting the ticket: {e}", ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒", description='Ticket for shopping'),
            discord.SelectOption(value="support", label="Support", emoji="💳", description='Ticket for support'),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔", description='Ticket for doubts'),
            discord.SelectOption(value="partners", label="Partners", emoji="🤝", description='Ticket to close partnership')
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        await interaction.response.defer()

        view = discord.ui.View()
        open_button = TicketButton(
            label=f"Open {selected_option.capitalize()} Ticket",
            ticket_option=selected_option
        )
        view.add_item(open_button)
        await interaction.followup.send(
            content=f"Press the button below to open a **{selected_option}** ticket",
            view=view,
            ephemeral=True
        )

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class TicketCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup_tickets")
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        embed = discord.Embed(
            title="**SERVICE**",
            description="➡️ - To open a ticket, select one of the options below:",
            color=0x2f336b
            )
        embed.add_field(name="", value="```ㅤㅤㅤㅤㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
        embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
        embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
        embed.set_image(url="https://i.imgur.com/C0dX3ac.png")
        view = PersistentView()
        await ctx.send(embed=embed, view=view)

    @setup_tickets.error
    async def setup_tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Only administrators can use this command.", delete_after=10)
        else:
            await ctx.send(f"❌ An error occurred: {error}", delete_after=10)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Developed by NTM DEV")
    await bot.add_cog(TicketCommands(bot))
    bot.add_view(PersistentView())
    print(f"✅ {bot.user} Ligou!")
    await bot.change_presence(activity=activity)

