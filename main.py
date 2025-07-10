import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import os
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

async def handle(request):
    return web.Response(text="OK")


async def start_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    await site.start()
    print("Web server started on port", os.environ.get('PORT', 8080))


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print("Synced " + str(len(synced)) + " commands.")
    except Exception as e:
        print(e)


@bot.tree.command(name="test")
@app_commands.describe(test="test")
async def test(interaction: discord.Interaction, test: Optional[str]):
    if not test:
        await interaction.response.send_message("Hello!", ephemeral=True)
        return
    await interaction.response.send_message(
        "Hello, this is super awesome {}".format(test), ephemeral=True)


@bot.event
async def on_member_join(member: discord.Member):
    role = 1392625209906954372
    x = member.guild.get_role(role)
    member.add_roles(role)
    embed = discord.Embed(
        title=f"Welcome {member.display_name}!",
        description=
        "It's nice to see you here! We hope you'll enjoy your stay!!",
        color=discord.Color.random())

    if member.avatar is None:
        avatar_url = member.default_avatar.url
    else:
        avatar_url = member.avatar.url

    embed.set_thumbnail(url=avatar_url)

    channel = member.guild.system_channel
    if channel:
        await channel.send(embed=embed)


@bot.tree.command(name="warn",
                  description="Give someone a warning for a rule break.")
@app_commands.describe(
    member="The member to warn.",
    reason="Why the warning is issued.",
    proof=
    "Link to the image or screenshot proof (upload it somewhere and paste link)."
)
async def warn(interaction: discord.Interaction, member: discord.Member,
               reason: str, proof: str):
    channel = 1392974737101029456
    x = interaction.guild.get_channel(channel)
    if not proof.startswith("http"):
        await interaction.response.send_message(
            "❌ Please provide a valid link to the proof.", ephemeral=True)
        return

    await interaction.response.send_message("The user has been warned.",
                                            ephemeral=True)

    await x.send(
        f"⚠️ {member.mention} has been warned for: **{reason}**\n📎 Proof: {proof}"
    )


bot.run(TOKEN)
