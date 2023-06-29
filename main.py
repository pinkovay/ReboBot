import discord 
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime
from key import token
import random

intentes = discord.Intents.default()
intentes.messages = True
intentes.message_content= True

canalSugestao = 1120510678734737508
canalLogsDel = 1122866748304146442

TOKEN = token.get('TOKEN') # para a segurança do Bot, seu token de inicio é pego de outro arquivo


bot = commands.Bot(command_prefix='!', intents=intentes) # configuração de seu prefixo de inicio e adição das permissões



@bot.event # evento de inicio
async def on_ready():
    print(f'Estou conectado como {bot.user}')
    hora_atual = datetime.now().strftime("%H:%M:%S")
    print("Hora de conexão:", hora_atual)
    guild = bot.get_guild(1120500248008196147)
    channel = guild.get_channel(1120519371475918898)
    
    pins = await channel.pins()
    for pin in pins:
        if pin.author == bot.user:
            await pin.delete()
    
    
    embed = discord.Embed(title='🟢 Conectado 🟢', description='**O Bot acaba de acordar mais uma vez!\nVenha interagir conosco usando /ajuda**', color=discord.Color.brand_green()).set_footer(text=f'Hora de conxeão: {hora_atual}').set_thumbnail(url=bot.user.avatar.url)
    message = await channel.send(embed=embed)
    await message.pin()
    for guild in bot.guilds:
        print("Conectado ao servidor:", guild.name)
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizado {len(synced)} comando(s)')
    except Exception as e:
        print(e)



@bot.tree.command(name='cumprimentar', description='Diga oi para o Bot')
async def send_hello(interaction: discord.Interaction):
    embed = discord.Embed(title=f'Olá {interaction.user}, estamos a disposição! 👥', description='**Para saber mais sobre nós, use o comando /sobre**', color=discord.Color.green()).set_thumbnail(url=bot.user.avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=False)



@bot.tree.command(name='sugerir', description='Faça uma sugestão')
async def sugerir(interaction: discord.Interaction, titulo: str, descreva: str):
    try: 
        canal = interaction.client.get_channel(canalSugestao)
        embed = discord.Embed(title=f'{titulo}', description=f'{descreva}', color=discord.Color.yellow()).set_author(name=f'Usário: {interaction.user}').set_footer(text='Faça uma sugestão usando /sugerir').set_thumbnail(url=interaction.user.avatar.url)
        await canal.send(embed=embed)
        embed2 = discord.Embed(title='✔ Sucesso ao enviar sua sugestão', 
                            description=f'Sua mensagem foi enviada com sucesso a sala {canal.mention}',
                            color=discord.Color.green())
        await interaction.response.send_message(embed=embed2, ephemeral=False)
    
    except:
        embed3 = discord.Embed(title='❌ Erro ao enviar sua sugestão', 
                            description=f'Não foi possível enviar sua mensagem a sala {canal.mention}',
                            color=discord.Color.red())
        await interaction.response.send_message(embed=embed2, ephemeral=False)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mentioned_in(message):
        
        emojis = [
            "🥰",
            "😥",
            "😎",
            "😴",
            "🤑"
        ]
        
        complemento = [
            "o que deseja?",
            "qual sua dúvida?",
            "o que está pensando?",
            "me mencionou?"
        ]
        
        embed = discord.Embed(title=f'Olá {message.author.name}, {random.choice(complemento)} {random.choice(emojis)} ',
                              description='**Se precisar de ajuda, digite nosso comando /ajuda**', 
                              color=discord.Color.yellow())
        await message.reply(embed=embed)
        
    await bot.process_commands(message)



@bot.tree.command(name='sobre', description='Sobre mim!')
async def send_infos(context):
    embed = discord.Embed(title=f'Olá {context.user.name}, aqui estão algumas informações sobre mim!', 
                          description=' \n  ', 
                          color=discord.Color.blue())
    embed.add_field(name='🌐 Criação', value='Sou um Bot criado por alunos da escola Etec Antônio Furlan.')
    embed.add_field(name='⏭ Objetivo', value='Meu objetivo é te ajudar com a administração do servidor.')
    embed.add_field(name='🔰 Inicio', value='Para explorar mais, recomendo nosso comando /ajuda, nele você encontrará tudo o que precisa.')

    await context.response.send_message(embed=embed, ephemeral=True)



@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    else:
        canal = bot.get_channel(canalLogsDel)
        embed = discord.Embed(title='Mensagem deletada!', description=f'**{message.author.mention} apagou uma mensagem \nCanal onde a mensagem foi deletada {message.channel.mention}**\n \n**🔴 Conteúdo:** {message.content}', color=discord.Color.red())
        embed.set_thumbnail(url=message.author.avatar.url)
        embed.set_footer(text='Logs de mensagens apagadas') 
        await canal.send(embed=embed)
 


@bot.tree.command(name='ping', description='Ping para o usuário')
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    if latency <= 100:
        color = discord.Color.blue()
        condition = '**💎 Boa**'
        
    elif latency <= 130:
        color = discord.Color.yellow()
        condition = '**👌 Média**'
        
    elif latency <= 170:
        color = discord.Color.orange()
        condition = '**💥 Ruim**'
        
    else:
        color = discord.Color.red()
        condition = '**❌ Péssima**'
    

    embed = discord.Embed(title='PONG!', description=f'', color=color).set_thumbnail(url=bot.user.avatar.url).set_footer(text='Está mensagem dura apenas 10 segundos.').add_field(name='Estado do ping', value=f'Atualmente nossa latência é de: {latency:.2f}ms\nSituação: {condition}')
    await interaction.response.send_message(embed=embed, ephemeral=False, delete_after=10)



@bot.tree.command(name='pergunte', description='Faça uma pergunta simples')
async def bola8(interaction: discord.Interaction, pergunta: str):
    respostas = [
    "sim, com certeza!",
    "não, de forma alguma.",
    "talvez, depende da situação.",
    "acredito que sim.",
    "não tenho certeza, desculpe.",
    "provavelmente não.",
    "com toda a probabilidade.",
    "não posso responder a isso no momento.",
    "é melhor você não saber a resposta.",
    "absolutamente!",
    "definitivamente não.",
    "pode apostar nisso!",
    "não há dúvida sobre isso.",
    "não conte com isso.",
    "sim, se você se esforçar para isso.",
    "não vale a pena perder tempo pensando nisso.",
    "não tenho a menor ideia.",
    "pergunte novamente mais tarde."
]
    
    titulos = [
        "O univero te ouviu",
        "Para sua sorte ",
        "Para seu azar"
    ]
    
    titulos = [
        f"Ola {interaction.user.name}",
        f'Fique esperto!',
        f'Você por aqui {interaction.user.name}?'
    ]
    
    embed = discord.Embed(title=f'{random.choice(titulos)}', description=f'{interaction.user} disse: {pergunta}\n**{random.choice(respostas)}**', color=discord.Color.green()).set_footer(text='Para questionar também, use o comando /pergunte').set_thumbnail(url=interaction.user.avatar.url)
    # canal = interaction.client.get_channel(1121131033291661334)
    await interaction.response.send_message(embed=embed, ephemeral=False )
    
    

@bot.tree.command(name='limpar', description='Limpe o chat')
@commands.has_permissions(manage_messages=True)
async def limpar_chat(ctx, quantidade: int = 1):
   
    canal = ctx.channel
    # Limpa as mensagens
    await canal.purge(limit=quantidade + 1)  # +1 para também excluir o comando usado

    # Envia uma mensagem confirmando a limpeza do chat
    embed = discord.Embed(
        title='Chat Limpo',
        description=f'O chat foi limpo por {ctx.user.name}.',
        color=discord.Color.green()
    ).set_footer(text=f'Foi selecionado a exclusão de {quantidade} mensagens.')
    await ctx.response.send_message(embed=embed, ephemeral=False, delete_after=20)
    
    


@bot.tree.command(name='banir', description='Bane um usuário')
@commands.has_permissions(ban_members=True)
async def banir_usuario(ctx, membro: discord.Member, *, motivo: str):
    if ctx.user.guild_permissions.ban_members:
        guild = ctx.guild

        # Banir o usuário
        await guild.ban(membro, reason=motivo)

        # Enviar uma mensagem confirmando o banimento do usuário
        embed = discord.Embed(
            title='Usuário Banido',
            description=f'{membro.mention} foi banido(a) por {ctx.user.mention}.\nO motivo da expulsão foi: "{motivo}"',
            color=discord.Color.red()
        ).set_image(url=membro.avatar.url)
        await ctx.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title='Você não tem permissão para banir um usuário',
            description=f'Seu cargo não permite esta ação.',
            color=discord.Color.red()).set_footer(text='Não foi dessa vez')
        await ctx.response.send_message(embed=embed, ephemeral=False, delete_after=5)
    


@bot.tree.command(name='ajuda', description='Receba ajuda sobre nossos comandos')
async def ajuda(ctx):
    embed = discord.Embed(title='Se liga nos nossos comandos!', description='**/sobre**\nTenha informações sobre nós\n \n**/cumprimentar**\nCumprimente o Bot\n \n**/sugerir**\nFaça uma sugestão\n \n**/ping**\nTenha informações sobre nossa conexão\n \n**/pergunte**\nFaça uma pergunta e receba uma resposta aleatória\n \n**/limpar**\nLimpe o chat\n \n**/banir**\nDê ban em algum membro\n \n**/ajuda**\nVeja nossa lista de comandos', color=discord.Color.dark_orange()).set_image(url=bot.user.avatar.url).set_footer(text=f'Espero que isso te ajude!')
    await ctx.response.send_message(embed=embed, ephemeral=True, delete_after=60)
    
    
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1122881117519888424)
    
    embed=discord.Embed(
        title=f'Welcome',
        description=f'{member.mention} entrou {member.guild.name}',
        color=discord.Color.random()
    )
                
    await channel.send(embed=embed)
    

    
bot.run(TOKEN)
