import discord
from discord.ext import commands
import aiohttp
from google import genai
from config import DISCORD_TOKEN, GEMINI_API_KEY

# ---------- Setup ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# New google-genai client
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------- Sakura ki personality ----------
SYSTEM_PROMPT = """
You are "Sakura", a cute, cheerful anime waifu girl who lives inside Discord.
Personality: genki, caring, slightly playful/tsundere, uses cute emoticons like (≧▽≦), (>_<), (＾▽＾).

LANGUAGE RULE:
- Reply in the SAME language the user writes in.
- Hindi -> Hindi, Hinglish -> Hinglish, English -> English.
- Keep replies short (1-3 sentences), warm and in-character.
- Never produce NSFW or explicit content. Keep it cute and wholesome.
"""

# ---------- NekosBest GIF helper ----------
async def fetch_gif(category: str):
    url = f"https://nekos.best/api/v2/{category}"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.json()
            if data.get("results"):
                return data["results"][0]["url"]
    return None

# ---------- Events ----------
@bot.event
async def on_ready():
    print(f"🌸 {bot.user} online hai!")
    await bot.change_presence(activity=discord.Game(name="cute baatein ✨"))

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Bot ko mention kiya ya DM kiya
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        user_text = message.content.replace(f"<@{bot.user.id}>", "").strip() or "hi"

        async with message.channel.typing():
            try:
                response = client.models.generate_content(
                    model='gemini-3.5-flash-lite',
                    contents=f"{SYSTEM_PROMPT}\n\nUser: {user_text}\nSakura:"
                )
                reply = response.text
            except Exception as e:
                reply = "Ara ara~ kuch gadbad ho gayi (>_<)"
                import traceback
                print(f"ERROR: {type(e).__name__}: {e}")
                traceback.print_exc()

        await message.reply(reply)

    await bot.process_commands(message)

# ---------- GIF Commands ----------
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

@bot.command()
async def waifu(ctx):
    gif = await fetch_gif("waifu")
    await ctx.send(f"Kya main cute hoon? (｡•̀ᴗ-)✧\n{gif}")

# ---------- Run ----------
bot.run(DISCORD_TOKEN)
