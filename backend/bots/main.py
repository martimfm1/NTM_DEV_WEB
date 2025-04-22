import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    ROLE_ID = 1303727367901941822
    guild = member.guild
    role = guild.get_role(ROLE_ID)
    
    if role:
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
        print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")

#contadores
@tasks.loop(seconds=30)
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

@tasks.loop(seconds=30)
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

@tasks.loop(seconds=30)
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

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="™ NTM DEV")
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'{bot.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot.change_presence(activity=activity)
    atualizar_canal_members.start()
    atualizar_canal_clients.start()
    atualizar_canal_bots.start()