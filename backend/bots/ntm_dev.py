import discord
from discord.ext import commands, tasks
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot = commands.Bot(command_prefix='0001', intents=intents)

#role automatica
@bot.event
async def on_member_join(member):
    ROLE_ID = 1303727367901941822
    guild = member.guild
    role = guild.get_role(ROLE_ID)
    
    if role:
        bot_role = guild.me.top_role
        if bot_role > role:
            try:
                await member.add_roles(role)
                print('-----------------------------------')
                print(f'Adicionada a role "{role.name}" ao membro {member.name}.')
                print('-----------------------------------')
            except discord.Forbidden:
                print(f"Permissão insuficiente para adicionar a role '{role.name}' ao membro {member.name}.")
            except discord.HTTPException as e:
                print(f"Erro ao tentar adicionar a role: {e}")
        else:
            print(f"A role do bot não é suficientemente alta para adicionar a role '{role.name}' ao membro {member.name}.")
    else:
        print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")

#contadores
@tasks.loop(seconds=60)
async def atualizar_canal_members():
    CANAL_ID = 1303520594649677894
    try:
        canal = bot.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            membros_reais = [m for m in guild.members if not m.bot]
            numero_membros_reais = len(membros_reais)
            novo_nome = f'members-{numero_membros_reais}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=60)
async def atualizar_canal_clients():
    CANAL_ID = 1303719327601655828
    ROLE_ID = 1303727484965224509
    try:
        canal = bot.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            role = guild.get_role(ROLE_ID)
            if role:
                numero_membros_com_role = len(role.members)
                novo_nome = f'clients-{numero_membros_com_role}'
                await canal.edit(name=novo_nome)
            else:
                print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=60)
async def atualizar_canal_bots():
    CANAL_ID = 1307465880745017366
    try:
        canal = bot.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            bots = [m for m in guild.members if m.bot]
            numero_bots = len(bots)
            novo_nome = f'bots-{numero_bots}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@bot.tree.command(name="suggestion", description="Send a suggestion in the suggestions channel!")
@app_commands.describe(texto="Send a suggestion")
async def suggestion(interaction: discord.Interaction, texto: str):
    CANAL_PERMITIDO_ID = 1364604088800772209

    if interaction.channel_id != CANAL_PERMITIDO_ID:
        await interaction.response.send_message(
            "This command can only be used in the allowed channel.", ephemeral=True
        )
        return

    if not texto.strip():
        await interaction.response.send_message(
            "You need to provide a suggestion text!", ephemeral=True
        )
        return

    embed = discord.Embed(
        title="Suggestion",
        description=texto,
        color=discord.Color.yellow()
    )

    if interaction.user:
        user = interaction.user
        embed.set_author(name=user.display_name, icon_url=user.avatar.url if user.avatar else None)

    await interaction.channel.send(embed=embed)

@bot.tree.command(name="delete", description="Command to delete messages")
async def delete(interaction: discord.Interaction, amount: int):
    required_role_id = 1303726904569892884

    if not any(role.id == required_role_id for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!", ephemeral=True)
        return
    
    if interaction.user.guild_permissions.manage_messages:
        if 0 < amount <= 100:
            await interaction.response.defer(ephemeral=True)
            await interaction.channel.purge(limit=amount + 1)
            await interaction.followup.send(f"{amount} messages were deleted.", ephemeral=True)
        else:
            await interaction.response.send_message("The number of messages to delete must be between 1 and 100.", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to delete messages on this server.", ephemeral=True)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="™ NTM DEV")
    print(f"✅ {bot.user} Ligou!")
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot.change_presence(activity=activity)
    atualizar_canal_members.start()
    atualizar_canal_clients.start()
    atualizar_canal_bots.start()