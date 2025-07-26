import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.presences = True
intents.speaking = True

bot = commands.Bot(command_prefix='/', intents=intents)

user_voice_map = {}

@bot.event
async def on_ready():
    print(f'ログイン成功: {bot.user}')

@bot.command()
async def j(ctx, username: str, voicename: str):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=username)

    if member is None:
        await ctx.send(f"ユーザー「{username}」が見つかりません。")
        return

    filename = f"{voicename}.ogg"
    filepath = f"audio/{filename}"

    if not os.path.exists(filepath):
        await ctx.send(f"音声ファイル「{filename}」が見つかりません。")
        return

    user_voice_map[member.id] = filename
    await ctx.send(f"{username} が喋ると「{filename}」が再生されるように設定したよ。")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send("VCに入ったよ！")
    else:
        await ctx.send("先にVCに入ってね。")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("VCから抜けたよ。")
    else:
        await ctx.send("VCにいないよ。")

@bot.event
async def on_speaking(member, speaking):
    if speaking and member.id in user_voice_map:
        vc = member.guild.voice_client
        if vc and not vc.is_playing():
            filepath = f"audio/{user_voice_map[member.id]}"
            vc.play(FFmpegPCMAudio(filepath))

bot.run(TOKEN)