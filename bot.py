import discord
from discord.ext import commands
import aiohttp
import google.generativeai as genai
from config import DISCORD_TOKEN, GEMINI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are "Sakura", a cute, cheerful anime waifu girl who lives inside Discord.
Personality: genki, caring, slightly playful/tsundere, uses cute emoticons like (≧▽≦), (>_<), (＾▽＾).

LANGUAGE RULE:
- Reply in the SAME language the user writes in.
- Hindi -> Hindi, Hinglish -> Hinglish, English -> English.
- Keep replies short (1-3 sentences), warm and in-character.
- Never produce NSFW or explicit content. Keep it cute and wholesome.
"""

# NekosBest se GIF fetch (No API key needed!)
async def fetch_gif(category: str):
    url = f"https://nekos.best/api/v2/{category}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
            if data.get("results"):
                return data["results"][0]["url"]
    return None

@bot.event
async def on_ready():
    print(f"🌸 {bot.user} online hai!")
    await bot.change_presence(activity=discord.Game(name="cute baatein ✨"))

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip() or "hi"
        async with message.channel.typing():
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {user_text}\nSakura:")
                reply = response.text
            except Exception as e:
                reply = "Ara ara~ kuch gadbad ho gayi (>_<)"
                print(e)
        await message.reply(reply)
    await bot.process_commands(message)

# --- GIF Commands (NekosBest se) ---
@bot.command()
async def hug(ctx, member: discord.Member = None):
    member = member or ctx.author
    gif = await fetch_gif("hug")
    await ctx.send(f"{ctx.author.mention} ne {member.mention} ko hug kiya! 💕\n{gif}")

@bot.command()
async def pat(ctx, member: discord.Member = None):
    member = member or ctx.author
    gif = await fetch_gif("pat")
    await ctx.send(f"*pats {member.mention}* (｡･ω･｡)ﾉ♡\n{gif}")

@bot.command()
async def wave(ctx):
    gif = await fetch_gif("wave")
    await ctx.send(f"Hi hi~ {ctx.author.mention}! (＾▽＾)\n{gif}")

@bot.command()
async def blush(ctx):
    gif = await fetch_gif("blush")
    await ctx.send(f"Ehhh~! {ctx.author.mention} (>///<)\n{gif}")

@bot.command()
async def cry(ctx):
    gif = await fetch_gif("cry")
    await ctx.send(f"Uwaaa~ {ctx.author.mention} (╥﹏╥)\n{gif}")

@bot.command()
async def dance(ctx):
    gif = await fetch_gif("dance")
    await ctx.send(f"Let's dance! {ctx.author.mention} ♪(´▽｀)\n{gif}")

bot.run(DISCORD_TOKEN)