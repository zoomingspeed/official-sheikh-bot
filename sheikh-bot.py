import discord
from discord.utils import get
from discord.ext import commands
from discord import default_permissions
from discord.ext import tasks
from discord.commands import Option
import random
import quranpy
import pyquran as q
import asyncio
import os
import requests
import datetime
from datetime import datetime
from collections import namedtuple
from discord import FFmpegPCMAudio

# declaring the bot variable
intents = discord.Intents.all()
bot = discord.Bot(intents=intents, status=discord.Status.idle)
guild_id = "1119428346485407744"
official_guild = "1166153827033030730"

# tells us client is ready
@bot.event
async def on_ready():
    clear = lambda: os.system('cls')
    clear()
    bot.add_view(MakeTicket())
    await bot.register_commands()
    for guild in bot.guilds:
        print(f"We have logged into {guild} as {bot.user}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="The Holy Quran"))

# on guild join
@bot.event
async def on_guild_join(guild):
    role = discord.utils.get(guild.roles, name="Muted")
    if role == None:
        role = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False)
        try:
            embed=discord.Embed(title="Introduction",
                                description="**السلام عليكم!**",
                                color=discord.Color.blurple())
            embed.add_field(name='**What is Sheikh Bot?**', value='Sheikh Bot is a bot that is used for moderation and Islamic purposes. To get started, please run "/help"', inline=False)
            await guild.text_channels[0].send(embed=embed)
            print(f"Bot has successfully joined {guild}")
        except Exception as e:
            print(f"Bot has ran into an error while running on_guild_join function: {e}")
    else:
        try:
            embed=discord.Embed(title="Introduction",
                                    description="**السلام عليكم!**",
                                    color=discord.Color.blurple())
            embed.add_field(name='**What is Sheikh Bot?**', value='Sheikh Bot is a bot that is used for moderation and Islamic purposes. To get started, please run "/help"', inline=False)
            await guild.text_channels[0].send(embed=embed)
            print(f"Bot has successfully joined {guild}")
        except Exception as e:
            print(f"Bot has ran into an error while running on_guild_join function: {e}")

# mute command
@bot.slash_command(name="mute", description="Mute a member in your server (REQUIRES MANAGE ROLES)")
@default_permissions(manage_roles = True)
@commands.guild_only()
async def mute(ctx, member:discord.Member, *, reason=None):
    coolbotvar = ctx.guild.me
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role in member.roles:
        embed=discord.Embed(title="",
                            description="This user is already muted!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        if reason == None:
            if member == coolbotvar:
                embed=discord.Embed(title="",
                                    description="I cannot mute myself!",
                                    color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)
            else:
                if member.guild_permissions.manage_roles:
                    embed=discord.Embed(title="",
                                        description="I cannot mute this member because they have `Manage Roles` permissions!",
                                        color=discord.Color.red())
                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    await member.add_roles(role)
                    embed=discord.Embed(title="Successfully muted!",
                                        description=f"Successfully muted {member.mention}, no reason provided.",
                                        color=discord.Color.green())
                    await ctx.respond(embed=embed)
                    for channel in guild.channels:
                        await channel.set_permissions(role, speak=False, send_messages=False)
                    print(f"{ctx.author} has successfully muted {member} in {guild}, no reason provided.")
        else:
            if member == coolbotvar:
                embed=discord.Embed(title="",
                                    description="I cannot mute myself!",
                                    color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)
            else:
                if member.guild_permissions.manage_roles:
                    embed=discord.Embed(title="",
                                        description="I cannot mute this member because they have `Manage Roles` permissions!",
                                        color=discord.Color.red())
                    await ctx.respond(embed=embed, ephemeral=True)
                else:
                    await member.add_roles(role)
                    embed=discord.Embed(title="Successfully muted!",
                                        description=f"Successfully muted {member.mention}!",
                                        color=discord.Color.green())
                    embed.add_field(name="**Reason:**", value=reason, inline=False)
                    await ctx.respond(embed=embed)
                    for channel in guild.channels:
                        await channel.set_permissions(role, speak=False, send_messages=False)
                    print(f"{ctx.author} has successfully muted {member} in {guild}, no reason provided.")

# quran command
@bot.slash_command(name="quran", description="Read Quran through Sheikh Bot")
async def quran(ctx, surah: int, verse: int):
    surah_variable = surah
    verse_variable = verse
    surah_name = q.quran.get_sura_name(surah_variable)
    e1 = surah_variable - 1
    e2 = verse_variable - 1
    class NextAndPreviousVerse(discord.ui.View):
        @discord.ui.button(label="Previous Verse", row=1, style=discord.ButtonStyle.primary, emoji=None)
        async def button_callback1(self, button, interaction):
            nonlocal surah_variable
            nonlocal verse_variable
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                try:
                    verse_variable -= 1
                    translation = quranpy.show_verses(
                        ayah=f"{surah_variable}:{verse_variable}",
                        edition=quranpy.Editions.sahih_international
                    )
                    string = f"{translation}"
                    check_string = len(string)
                    print_short_string = string[:960]
                    if check_string > 990:
                        embed2=discord.Embed(title="",
                                             description="",
                                             color=discord.Color.orange())
                        embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        if verse_variable > 0:
                            await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                        else:
                            embed=discord.Embed(title="",
                                                description="You cannot go past the first verse!",
                                                color=discord.Color.red())
                            verse_variable = 1
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed2=discord.Embed(title="",
                                             description="",
                                             color=discord.Color.orange())
                        embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        if verse_variable > 0:
                            await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                        else:
                            embed=discord.Embed(title="",
                                                description="You cannot go past the first verse!",
                                                color=discord.Color.red())
                            verse_variable = 1
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                except quranpy.exceptions.SurahNotFound:
                    surah_variable -= 1
                    verse_variable -= 1
            
        @discord.ui.button(label="Next Verse", row=1, style=discord.ButtonStyle.primary, emoji=None)
        async def button_callback2(self, button, interaction):
            nonlocal surah_variable
            nonlocal verse_variable
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                try:
                    verse_variable += 1
                    translation = quranpy.show_verses(
                        ayah=f"{surah_variable}:{verse_variable}",
                        edition=quranpy.Editions.sahih_international
                    )
                    string = f"{translation}"
                    check_string = len(string)
                    surah_name = q.quran.get_sura_name(surah_variable)
                    if check_string > 990:
                        print_short_string = string[:960]
                        embed2=discord.Embed(title="",
                                            description="",
                                            color=discord.Color.orange())
                        embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                    else:
                        embed2=discord.Embed(title="",
                                            description="",
                                            color=discord.Color.orange())
                        embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                except quranpy.exceptions.IncorrectAyahArguments:
                    if surah_variable == 114:
                        embed2 = discord.Embed(title="",
                                               description="This is the last Surah!",
                                               color=discord.Color.red())
                        verse_variable = 6
                        await ctx.respond(embed=embed2, ephemeral=True)
                    else:
                        verse_variable = 1
                        surah_variable += 1
                        translation = quranpy.show_verses(
                            ayah=f"{surah_variable}:{verse_variable}",
                            edition=quranpy.Editions.sahih_international
                        )
                        surah_name = q.quran.get_sura_name(surah_variable)
                        embed2=discord.Embed(title="",
                                            description="",
                                            color=discord.Color.orange())
                        embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))

        @discord.ui.button(label="Previous Surah", row=2, style=discord.ButtonStyle.primary, emoji=None)
        async def button_callback3(self, button, interaction):
            nonlocal surah_variable
            nonlocal verse_variable
            nonlocal e1
            e1 = verse_variable - 1
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                try:
                    verse_variable = 1
                    surah_variable -= 1
                    surah_name = q.quran.get_sura_name(surah_variable)
                    translation = quranpy.show_verses(
                        ayah=f"{surah_variable}:{verse_variable}",
                        edition=quranpy.Editions.sahih_international
                    )
                    embed2=discord.Embed(title="",
                                        description="",
                                        color=discord.Color.orange())            
                    embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                    embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                    embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                    embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                    await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                except quranpy.exceptions.SurahNotFound:
                    embed=discord.Embed(title="",
                                        description="You cannot go past the first Surah!",
                                        color=discord.Color.red())
                    surah_variable = 1
                    verse_variable = e1 + 1
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        
        @discord.ui.button(label="Next Surah", row=2, style=discord.ButtonStyle.primary, emoji=None)
        async def button_callback4(self, button, interaction):
            nonlocal surah_variable
            nonlocal verse_variable
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                try:
                    verse_variable = 1
                    surah_variable += 1
                    surah_name = q.quran.get_sura_name(surah_variable)
                    translation = quranpy.show_verses(
                        ayah=f"{surah_variable}:{verse_variable}",
                        edition=quranpy.Editions.sahih_international
                    )
                    embed2=discord.Embed(title="",
                                        url="",
                                        description="",
                                        color=discord.Color.orange())
                    embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                    embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                    embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                    embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                    await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                except IndexError:
                    embed=discord.Embed(title="",
                                        description="This is the last Surah!",
                                        color=discord.Color.red())
                    await ctx.respond(embed=embed, ephemeral=True)
                    surah_variable -= 1
                    verse_variable = 1
                    surah_name = q.quran.get_sura_name(surah_variable)
                    translation = quranpy.show_verses(
                        ayah=f"{surah_variable}:{verse_variable}",
                        edition=quranpy.Editions.sahih_international
                    )
                    embed2=discord.Embed(title="",
                                        url="",
                                        description="",
                                        color=discord.Color.orange())
                    embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                    embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                    embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                    embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                    await interaction.response.edit_message(embed=embed2, view=NextAndPreviousVerse(timeout=None))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        
        @discord.ui.button(label="Stop", row=3, style=discord.ButtonStyle.danger, emoji="🛑")
        async def button_callback5(self, button, interaction):
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                if interaction.user != ctx.author:
                    embed=discord.Embed(title="",
                                        description="This is not your Quran panel!",
                                        color=discord.Color.red())
                    await interaction.response.send(embed=embed, ephemeral=True)
                else:
                    try:
                        await ctx.author.send(f"If you want to continue off the last ayah, then you stopped at `{surah_variable}:{verse_variable}`!")
                        await interaction.message.delete()
                    except discord.errors.Forbidden:
                        await interaction.message.delete()
                        embed=discord.Embed(title="",
                                            description=f"Your `Direct Messages` are off for this server! Please enable them, as the bot sends in them the last ayah you were on. The last ayah you were on was `{surah_variable}:{verse_variable}`",
                                            color=discord.Color.red())
                        await interaction.response.send(embed=embed, ephemeral=True)
        
        @discord.ui.button(label="Bookmark", row=3, style=discord.ButtonStyle.success, emoji="⭐")
        async def button_callback6(self, button, interaction):
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                nonlocal surah_variable
                nonlocal verse_variable
                class CoolBookMark(discord.ui.View):
                    @discord.ui.button(label="Share", style=discord.ButtonStyle.primary, emoji="🔗")
                    async def button_is_clicked_yay(self, button, interaction):
                        await interaction.response.send_message(f"https://quran.com/{surah_variable}/{verse_variable}/", ephemeral=True)
                    @discord.ui.button(label="Remove Bookmark", style=discord.ButtonStyle.danger, emoji=None)
                    async def button_was_clicked(self, button, interaction):
                        await interaction.message.delete()
                        await interaction.response.send_message("Bookmark removed!", ephemeral=True)
                surah_name = q.quran.get_sura_name(surah_variable)
                translation = quranpy.show_verses(
                    ayah=f"{surah_variable}:{verse_variable}",
                    edition=quranpy.Editions.sahih_international
                )
                translation_string = f"{translation}"
                check_length = len(translation_string)
                shorten = translation_string[:960]
                user = interaction.user
                embed2=discord.Embed(title="",
                                    description="Bookmark saved!",
                                    color=discord.Color.green())
                embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")

                
                if check_length > 990:
                    try:
                        embed=discord.Embed(title="",
                                            description="Bookmark saved!",
                                            color=discord.Color.green())
                        embed.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed.add_field(name="Translation (Sahih International):", value=f"{shorten}...", inline=False)
                        embed.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                        message = await user.send(embed=embed, view=CoolBookMark(timeout=None))
                        await message.pin()
                        await ctx.respond("Bookmark saved!", ephemeral=True)
                    except discord.errors.Forbidden:
                        embed3=discord.Embed(title="",
                                            description="I cannot message you because you have `Direct Messages` off for this server!",
                                            color=discord.Color.red())
                        await ctx.respond(embed=embed3 , ephemeral=True)
                else:
                    try:
                        message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                        await message.pin()
                        await ctx.respond("Bookmark saved!", ephemeral=True)
                    except discord.errors.Forbidden:
                        embed3=discord.Embed(title="",
                                             description="I cannot message you because you have `Direct Messages` off for this server!",
                                             color=discord.Color.red())
                        await ctx.respond(embed=embed3, ephemeral=True)
        
        @discord.ui.button(label="Share", row=3, style=discord.ButtonStyle.primary, emoji="🔗")
        async def button_callback7(self, button, interaction):
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                await interaction.response.send_message(f"https://quran.com/{surah_variable}/{verse_variable}/", ephemeral=True)
    try:
        translation = quranpy.show_verses(
            ayah=f"{surah_variable}:{verse_variable}",
            edition=quranpy.Editions.sahih_international
        )
        string = f"{translation}"
        check_string = len(string)
        print_short_string = string[:960]
        if check_string > 990:
            embed2=discord.Embed(title="",
                                 url="",
                                 description="",
                                 color=discord.Color.orange())
            embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
            embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
            embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
            embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
            await ctx.respond(embed=embed2, view=NextAndPreviousVerse(timeout=None))
            guild = ctx.guild
            user = ctx.author
            print(f"{user} has successfully called the Quran command in {guild}")
        else:
            embed2=discord.Embed(title="",
                                 url="",
                                 description="",
                                 color=discord.Color.orange())
            embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
            embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
            embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
            embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
            await ctx.respond(embed=embed2, view=NextAndPreviousVerse(timeout=None))
            guild = ctx.guild
            user = ctx.author
            print(f"{user} has successfully called the Quran command in {guild}")
    except:
        embed=discord.Embed(title="",
                            description="This is not a real Surah/Verse number! There are 114 chapters in the Quran. The verse depends on what Surah you choose.",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)

# quran verse search command
@bot.slash_command(name="vquran", description="Search for verses in the Holy Quran")
async def vquran(ctx, surah: int, verse: int):
    integer1_int = surah
    integer2_int = verse
    class ShareAndDelete(discord.ui.View):
        @discord.ui.button(label="Share", style=discord.ButtonStyle.primary, emoji="🔗")
        async def hello_this_button_was_clicked(self, button, interaction):
            await interaction.response.send_message(f"https://quran.com/{integer1_int}/{integer2_int}/", ephemeral=True)
        @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, emoji="🗑️")
        async def this_button_was_clicked(self, button, interaction):
            if interaction.user != ctx.author:
                embed=discord.Embed(title="",
                                    description="You can't delete this verse!",
                                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.message.delete()
                await interaction.response.send_message("Verse deleted!", ephemeral=True)
        @discord.ui.button(label="Bookmark", style=discord.ButtonStyle.green, emoji="⭐")
        async def did_i_click_yes(self, button, interaction):
            if interaction.user != ctx.author:
                embedsomething=discord.Embed(title="",
                                             description="This is not your Quran panel!",
                                             color=discord.Color.red())
                await interaction.response.send_message(embed=embedsomething, ephemeral=True)
            else:
                class CoolBookMark(discord.ui.View):
                    @discord.ui.button(label="Share", style=discord.ButtonStyle.primary, emoji="🔗")
                    async def button_is_clicked_yay(self, button, interaction):
                        await interaction.response.send_message(f"https://quran.com/{integer1_int}/{integer2_int}/", ephemeral=True)
                    @discord.ui.button(label="Remove Bookmark", style=discord.ButtonStyle.danger, emoji=None)
                    async def button_was_clicked(self, button, interaction):
                        await interaction.message.delete()
                        await interaction.response.send_message("Bookmark removed!", ephemeral=True)
                translation = quranpy.show_verses(
                    ayah=f"{integer1_int}:{integer2_int}",
                    edition=quranpy.Editions.sahih_international
                )
                user = interaction.user
                string = f"{translation}"
                check_string = len(string)
                print_short_string = string[:960]
                if check_string > 990:
                    try:
                        embed2=discord.Embed(title="",
                                             description="Bookmark saved!",
                                             color=discord.Color.green())
                        embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
                        message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                        await message.pin()
                        await ctx.respond("Bookmark saved!", ephemeral=True)
                    except discord.errors.Forbidden:
                        embed=discord.Embed(title="",
                                            description="I cannot message you because you have `Direct Messages` off for this server!",
                                            color=discord.Color.red())
                        await ctx.respond(embed=embed, ephemeral=True)
                else:
                    try:
                        embed2=discord.Embed(title="",
                                             description="Bookmark saved!",
                                             color=discord.Color.green())
                        embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
                        message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                        await message.pin()
                        await ctx.respond("Bookmark saved!", ephemeral=True)
                    except discord.errors.Forbidden:
                        embed=discord.Embed(title="",
                                            description="I cannot message you because you have `Direct Messages` off for this server!",
                                            color=discord.Color.red())
                        await ctx.respond(embed=embed, ephemeral=True)
    guild = ctx.guild
    surah_variable = q.quran.get_sura_name(integer1_int)
    translation = quranpy.show_verses(
        ayah=f"{integer1_int}:{integer2_int}",
        edition=quranpy.Editions.sahih_international
    )
    string = f"{translation}"
    check_string = len(string)
    print_short_string = string[:960]
    if check_string > 990:
        embed2=discord.Embed(title="",
                             url="",
                             description="",
                             color=discord.Color.orange())
        embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
        embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
        await ctx.respond(embed=embed2, view=ShareAndDelete(timeout=None))
        print(f"Successfully sent surah {integer1_int}, ayah/verse {integer2_int} to {ctx.author} in {guild}")
    else:
        embed2=discord.Embed(title="",
                             url="",
                             description="",
                             color=discord.Color.orange())
        embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
        embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
        embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
        embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
        await ctx.respond(embed=embed2, view=ShareAndDelete(timeout=None))
        print(f"Successfully sent surah {integer1_int}, ayah/verse {integer2_int} to {ctx.author} in {guild}")

# quran by page command
@bot.slash_command(name="pquran", description="Browse the Quran by page")
async def pquran(ctx, page: int):
    page_range = range(1, 604)
    page_format = str(page).zfill(3)
    if page not in page_range:
        embed=discord.Embed(title="",
                            description="This is not a valid page number! A valid page number is a number between 1-604.",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        class QuranByPage(discord.ui.View):
            @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.blurple, emoji="⬅️", row=1)
            async def button_callback(self, button, interaction):
                if interaction.user != ctx.author:
                    embed=discord.Embed(title="",
                                        description="This is not your Quran panel!",
                                        color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    nonlocal page
                    nonlocal page_format
                    if page > 1:
                        page -= 1
                        page_format = str(page).zfill(3)
                        embed=discord.Embed(title=f"Page Number: {page}",
                                            description="",
                                            color=discord.Color.orange())
                        embed.set_author(name="Quran By Page", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed.set_image(url=f"https://www.searchtruth.org/quran/images1/{page_format}.jpg")
                        await interaction.response.edit_message(embed=embed, view=QuranByPage(timeout=None))
                    else:
                        page = 604
                        page_format = str(page).zfill(3)
                        embed=discord.Embed(title=f"Page Number: {page}",
                                            description="",
                                            color=discord.Color.orange())
                        embed.set_author(name="Quran By Page", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed.set_image(url=f"https://www.searchtruth.org/quran/images1/{page_format}.jpg")
                        await interaction.response.edit_message(embed=embed, view=QuranByPage(timeout=None))
            @discord.ui.button(label="Next Page ➡️", style=discord.ButtonStyle.green, emoji=None, row=1)
            async def button_callback1(self, button, interaction):
                if interaction.user != ctx.author:
                    embed=discord.Embed(title="",
                                        description="This is not your Quran panel!",
                                        color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    nonlocal page
                    nonlocal page_format
                    if page < 604:
                        page += 1
                        page_format = str(page).zfill(3)
                        embed=discord.Embed(title=f"Page Number: {page}",
                                            description="",
                                            color=discord.Color.orange())
                        embed.set_author(name="Quran By Page", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed.set_image(url=f"https://www.searchtruth.org/quran/images1/{page_format}.jpg")
                        await interaction.response.edit_message(embed=embed, view=QuranByPage(timeout=None))
                    else:
                        page = 1
                        page_format = str(page).zfill(3)
                        embed=discord.Embed(title=f"Page Number: {page}",
                                            description="",
                                            color=discord.Color.orange())
                        embed.set_author(name="Quran By Page", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                        embed.set_image(url=f"https://www.searchtruth.org/quran/images1/{page_format}.jpg")
                        await interaction.response.edit_message(embed=embed, view=QuranByPage(timeout=None))
            @discord.ui.button(label="Stop", style=discord.ButtonStyle.red, emoji="🛑", row=2)
            async def button_callback2(self, button, interaction):
                if interaction.user != ctx.author:
                    embed=discord.Embed(title="",
                                        description="This is not your Quran panel!",
                                        color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        await ctx.author.send(f"If you want to continue off the last page, then you stopped at page `{page}`!")
                        await interaction.message.delete()
                    except discord.errors.Forbidden:
                        embed=discord.Embed(title="",
                                            description=f"Your `Direct Messages` are off for this server! Please enable them, as the bot sends in them the last page you were on before you stopped. The last page you were on is `{page}`.",
                                            color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        await interaction.message.delete()
    
    embed=discord.Embed(title=f"Page Number: {page}",
                        description="",
                        color=discord.Color.orange())
    embed.set_author(name="Quran By Page", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
    embed.set_image(url=f"https://www.searchtruth.org/quran/images1/{page_format}.jpg")
    await ctx.respond(embed=embed, view=QuranByPage(timeout=None))
                    
# unmute command
@bot.slash_command(name="unmute", description="Unmute a member that is muted in your server")
@default_permissions(manage_roles = True)
@commands.guild_only()
async def unmute(ctx, member : discord.Member):
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if ctx.author.guild_permissions.manage_roles:
        if role in member.roles:
            embed=discord.Embed(title="Unmute successful!",
                                description=f"Successfully unmuted {member.mention}!",
                                color=discord.Color.green())
            await ctx.respond(embed=embed)
            await member.remove_roles(role)
            print(f"{ctx.author} has successfully unmuted {member} in {guild}")
        else:
            embed=discord.Embed(title="",
                                description=f"{member.mention} is not muted!",
                                color=discord.Color.red())
            await ctx.respond(embed=embed)
            print(f"{ctx.author} could not unmute {member} due to {member} not being muted")
    else:
        embed=discord.Embed(title="",
                            description="You do not have permission to unmute other members!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed)
        print(f"Could not unmute {member} in {guild} due to {ctx.author} having insufficient permissions")

# ban command
@bot.slash_command(name="ban", description="Ban a member inside your server")
@default_permissions(ban_members = True)
@commands.guild_only()
async def ban(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    coolbotvar = guild.me
    if member.guild_permissions.ban_members:
        embed=discord.Embed(title="",
                            description="I cannot ban this member because they have the `Ban Members` permission!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        if reason == None:
            if member == coolbotvar:
                embed=discord.Embed(title="",
                                    description="I cannot ban myself!",
                                    color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)
            else:
                try:
                    embed=discord.Embed(title="Ban successful!",
                                        description=f"Successfully banned {member.mention}, no reason provided.",
                                        color=discord.Color.green())
                    await member.send(f"You have been banned from {guild}, no reason provided.")
                    await member.ban()
                    await ctx.respond(embed=embed)
                    print(f"{ctx.author} has successfully banned {member} from {guild}, no reason provided.")
                except discord.errors.Forbidden:
                    embed=discord.Embed(title="Ban successful!",
                                        description=f"Successfully banned {member.mention}, no reason provided.",
                                        color=discord.Color.green())
                    await member.ban()
                    await ctx.respond(embed=embed)
                    print(f"{ctx.author} has successfully banned {member} from {guild}, no reason provided.")
        else:
            if member == coolbotvar:
                embed=discord.Embed(title="",
                                    description="I cannot ban myself!",
                                    color=discord.Color.red())
                await ctx.respond(embed=embed, ephemeral=True)
            else:
                try:
                    embed=discord.Embed(title="Ban successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully banned {member.mention}!", inline=False)
                    embed.add_field(name="**Reason:**", value=reason, inline=False)
                    await member.send(f"You have been banned from {guild} due to the following reason:\n\n```{reason}```")
                    await member.ban()
                    await ctx.respond(embed=embed)
                    print(f"{ctx.author} has successfully banned {member} from {guild} due to the following reason: {reason}")
                except discord.errors.Forbidden:
                    embed=discord.Embed(title="Ban successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully banned {member.mention}!", inline=False)
                    embed.add_field(title="**Reason:**", value=reason, inline=False)
                    await member.ban()
                    await ctx.respond(embed=embed)

# kick command
@bot.slash_command(name="kick", description="Kick other members from your server!")
@default_permissions(kick_members = True)
@commands.guild_only()
async def kick(ctx, member : discord.Member, reason=None):
    guild = ctx.guild
    coolbotvar = guild.me
    if member.guild_permissions.kick_members:
        embed=discord.Embed(title="",
                            description="I cannot kick this member because they have the `Kick Members` permission!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        if member == coolbotvar:
            embed=discord.Embed(title="",
                                description="I cannot kick myself!",
                                color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            if reason == None:
                try:
                    guild = ctx.guild
                    embed=discord.Embed(title="Kick successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully kicked {member.mention}, no reason provided.")
                    await member.send(f"You have been kicked from {guild}, no reason provided.")
                    await ctx.respond(embed=embed)
                    await member.kick()
                    print(f"{ctx.author} has successfully kicked {member} from {guild}, no reason provided.")
                except discord.errors.HTTPException:
                    guild = ctx.guild
                    embed=discord.Embed(title="Kick successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully kicked {member.mention}, no reason provided.")
                    await ctx.respond(embed=embed)
                    await member.kick()
                    print(f"{ctx.author} has successfully kicked {member} from {guild}, no reason provided.")
            else:
                try:
                    embed=discord.Embed(title="Kick successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully kicked {member.mention}!", inline=False)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    await ctx.respond(embed=embed)
                    await member.send(f"You have been kicked from {guild} due to the following reason: ```{reason}```")
                    await member.kick()
                    print(f"{ctx.author} has successfully kicked out {member} from {guild} due to the following reason: {reason}")
                except discord.errors.HTTPException:
                    embed=discord.Embed(title="Kick successful!",
                                        color=discord.Color.green())
                    embed.add_field(name="", value=f"Successfully kicked {member.mention}!", inline=False)
                    embed.add_field(name="**Reason:**", value=reason, inline=False)
                    await ctx.respond(embed=embed)
                    await member.kick()
                    print(f"{ctx.author} has successfully kicked out {member} from {guild} due to the following reason: {reason}")

# activate tickets
@bot.slash_command(name="activatetickets", description="Send the embed with the button to create a ticket (REQUIRES administrator)")
@default_permissions(administrator = True)
@commands.guild_only()
async def ticket(ctx):
    embed=discord.Embed(title="Create a ticket!",
                        description="If you need support from staff, then make a ticket!",
                        color=discord.Color.dark_blue())
    await ctx.defer()
    await asyncio.sleep(3)
    await ctx.send("Activated tickets!", ephemeral=True)
    await ctx.send(embed=embed, view=MakeTicket())
    print(f"{ctx.author} has activated tickets for {ctx.guild}")
class MakeTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Create a ticket!", custom_id="make-ticket", style=discord.ButtonStyle.primary, emoji="🎫")
    async def button_pressed(self, button, interaction):
        number1 = random.randint(0,9)
        number2 = random.randint(0,9)
        number3 = random.randint(0,9)
        number4 = random.randint(0,9)
        user = interaction.user
        guild = interaction.guild
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True),
            muted_role: discord.PermissionOverwrite(send_messages=True)
        }
        channel = await interaction.guild.create_text_channel(f"ticket-{number1}{number2}{number3}{number4}", overwrites=overwrites)
        embed=discord.Embed(title="Welcome!",
                            description="In order for staff to answer your ticket faster, please follow these steps:",
                            color=discord.Color.blurple())
        embed.add_field(name="**STEP 1:**", value="Introduce yourself to the staff.")
        embed.add_field(name="**STEP 2:**", value="Enter your timezone (EST, CST, etc. This is for staff to answer your ticket faster).")
        embed.add_field(name="**STEP 3:**", value="Explain your problem/issue as detailed as possible, so staff can understand your problem easier.")
        await channel.send(f"{interaction.user.mention}", embed=embed)
        await interaction.response.send_message(f"Your ticket has been created: {channel.mention}", ephemeral=True)

# close ticket
@bot.slash_command(name="closeticket", description="Close a ticket", guild_id=["1119428346485407744"])
async def closeticket(ctx):
    channel_name = ctx.channel.name
    channel = ctx.channel
    if channel_name.__contains__("ticket-"):
        await channel.delete()
    else:
        embed=discord.Embed(title="",
                            description="This is not a ticket channel!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)

# help command
@bot.slash_command(name="help", description="See what commands are available")
@discord.option("option", description="The type of help that you want to receive back from the bot", choices=['Main', 'Commands', 'Admin', 'Prayer', 'Quran'])
async def help(ctx: discord.ApplicationContext, option: str):
    if option == "Main":
        embed=discord.Embed(title="HELP",
                            description="Here are the different ways you can call the help command:",
                            color=discord.Color.blurple())
        embed.add_field(name="**COMMANDS:**", value="/help commands")
        embed.add_field(name="**ADMINISTRATOR COMMANDS:**", value="/help admin", inline=False)
        embed.add_field(name="**PRAYER COMMANDS:**", value="/help prayer", inline=False)
        embed.add_field(name="**QURAN COMMANDS**", value="/help quran", inline=False)
        await ctx.respond(embed=embed)
    elif option == "Commands":
        embed=discord.Embed(title="Commands:",
                            description="Here are all of the commands available with the bot:",
                            color=discord.Color.green())
        embed.add_field(name="**Quran Commands**", value="/vquran (surah number, verse number), /quran (surah number, verse number)", inline=False)
        embed.add_field(name="**Prayertime Command**", value="/prayertimes `city` `country (if needed)` `method (integer)` `", inline=False)
        embed.add_field(name="**Close ticket:**", value="/closeticket (only works in ticket channel)")
        await ctx.respond(embed=embed)
    elif option == "Admin":
        embed=discord.Embed(title="**ADMINISTRATOR COMMANDS:**",
                            description="Administrator commands for Sheikh Bot",
                            color=discord.Color.yellow())
        embed.add_field(name="Ban command:", value="/ban (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Mute command:", value="/mute (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Kick command:", value="/kick (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Activate tickets:", value="/activatetickets **(REQUIRES ADMINISTRATOR)**", inline=False)
        await ctx.respond(embed=embed)
    elif option == "Prayer":
        embed=discord.Embed(title="**PRAYER TIME GUIDE**",
                            description="Guide for using /prayertimes with Sheikh Bot",
                            color=discord.Color.dark_green())
        embed.add_field(name="**METHODS:**", value="The bot uses aladhan.com, which persists of a lot of prayer time methods, including one to use your own custom prayer time method. We use fifteen of them, which are listed here: ``/methodslist``. Any integer besides 0-16 (15 not included) will raise a message telling you it is an invalid integer.", inline=False)
        embed.add_field(name="**CITY AND/OR COUNTRY:**", value="The command gives you a prompt for the location you want to gather prayer times with. It can be formatted in anyway, but if you want it to be most accurate, do it by state (New York City, NY) or by country (Moscow, RU)", inline=False)
        embed.add_field(name="**PRIVATE MESSAGE:**", value='Sheikh Bot respects your privacy. As a result of respecting your privacy, Sheikh Bot provides a parameter that shows two options, which are true and false. If you select true, it sends you a direct message with the prayer times included. Pressing false will make the bot print the prayer times on the server you called the command in.', inline=False)
        await ctx.respond(embed=embed)
    elif option == "Quran":
        embed=discord.Embed(title="**QURAN COMMANDS:**",
                            description="Commands relating to Quran",
                            color=discord.Color.orange())
        embed.add_field(name="Print one verse:", value="/vquran (surah number) (verse number)", inline=False)
        embed.add_field(name="Read Quran by Ayah:", value="/quran (surah number) (verse number)", inline=False)
        embed.add_field(name="Read Quran by page:", value="/pquran (page number)", inline=False)

# prayer time command
PrayerTimeMethod = namedtuple('PrayerTimeMethod', ["id"])
prayer_methods = {
    "Shia Ithna-Ashari": PrayerTimeMethod(id=0),
    "University of Islamic Sciences, Karachi": PrayerTimeMethod(id=1),
    "Islamic Society of North America": PrayerTimeMethod(id=2),
    "Muslim World League": PrayerTimeMethod(id=3),
    "Umm Al-Qura University, Makkah": PrayerTimeMethod(id=4),
    "Egyptian General Authority of Survey": PrayerTimeMethod(id=5),
    "Institue of Geophysics, University of Tehran": PrayerTimeMethod(id=7),
    "Gulf Region": PrayerTimeMethod(id=8),
    "Kuwait": PrayerTimeMethod(id=9),
    "Qatar": PrayerTimeMethod(id=10),
    "Majlis Ugama Islam Singapura, Singapore": PrayerTimeMethod(id=11),
    "Union Organization islamic de France": PrayerTimeMethod(id=12),
    "Diyanet İşleri Başkanlığı, Turkey": PrayerTimeMethod(id=13),
    "Spiritual Administration of Muslims of Russia": PrayerTimeMethod(id=14),
    "Dubai (unofficial)": PrayerTimeMethod(id=16)
}
prayer_methods_list = [
    "Shia Ithna-Ashari",
    "University of Islamic Sciences, Karachi",
    "Islamic Society of North America",
    "Muslim World League",
    "Umm Al-Qura University, Makkah",
    "Egyptian General Authority of Survey",
    "Institue of Geophysics, University of Tehran",
    "Gulf Region",
    "Kuwait",
    "Qatar",
    "Majlis Ugama Islam Singapura, Singapore",
    "Union Organization islamic de France",
    "Diyanet İşleri Başkanlığı, Turkey",
    "Spiritual Administration of Muslims of Russia",
    "Dubai (unofficial)"
]
@bot.slash_command(name="prayertimes", description="Check your local towns prayer times")
@discord.option("method", description="The calculation method used for your prayer times", choices=prayer_methods_list)
async def prayertimes(ctx, location: str, method: str, private_message: bool, twelve_hour_format: bool):
    await ctx.defer(ephemeral = private_message)
    method_get = prayer_methods[method]
    m = method_get.id
    if ctx.channel.type == discord.ChannelType.private:
        prayer_url = f"http://api.aladhan.com/v1/timingsByAddress?address={location}&method={m}&school=0"
        asr_hanafi_link = f"http://api.aladhan.com/v1/timingsByAddress?address={location}&method={m}&school=1"
        try:
            prayer_requests = requests.get(prayer_url)
            prayer_response = prayer_requests.json()
            prayer_date = prayer_response['data']['date']['readable']
        except TypeError:
            embed=discord.Embed(title="",
                                description="This is not a valid location! (A valid location for example: New York City, New York)",
                                color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:
            asr_hanafi_request = requests.get(asr_hanafi_link)
            prayer_response = prayer_requests.json()
            asr_hanafi_response = asr_hanafi_request.json()
            prayer_date = prayer_response['data']['date']['readable']
            embedmain=discord.Embed(title=f"Prayer times of {location}:",
                                    description=f'',
                                    color=discord.Color.orange())
            embedmain.set_author(name=prayer_date, icon_url="https://images-ext-1.discordapp.net/external/u3RRy2sqPlkHUgO2HXkx-JEjTu0aZnFJfT4omEfrPM8/https/images-na.ssl-images-amazon.com/images/I/51q8CGXOltL.png")
            embedmain.add_field(name="Fajr:", value=prayer_response['data']['timings']['Fajr'], inline=False)
            embedmain.add_field(name="Sunrise:", value=prayer_response['data']['timings']['Sunrise'], inline=False)
            embedmain.add_field(name="Dhuhr:", value=prayer_response['data']['timings']['Dhuhr'], inline=False)
            embedmain.add_field(name="Asr:", value=prayer_response['data']['timings']['Asr'], inline=False)
            embedmain.add_field(name="Asr (Hanafi):", value=asr_hanafi_response['data']['timings']['Asr'], inline=False)
            embedmain.add_field(name="Sunset:", value=prayer_response['data']['timings']['Sunset'], inline=False)
            embedmain.add_field(name="Maghrib:", value=prayer_response['data']['timings']['Maghrib'], inline=False)
            embedmain.add_field(name="Isha:", value=prayer_response['data']['timings']['Isha'], inline=False)
            embedmain.add_field(name="Imsak:", value=prayer_response['data']['timings']['Imsak'], inline=False)
            embedmain.set_footer(text="If you aren't sure if your prayer times are correct, you can do it by state (New York City, NY), or by country (Moscow, RU)", icon_url="https://cdn.discordapp.com/attachments/1174896701526511666/1255684889911492709/warning-sign-30915_1280.png?ex=667e072f&is=667cb5af&hm=1f7578a95680876530da2a1830d7079cc7eb85b796e2a69b2f7a37e5bd935683&")
            if twelve_hour_format == True:
                fajr_12hr = datetime.strptime(prayer_response['data']['timings']['Fajr'], "%H:%M")
                sunrise_12hr = datetime.strptime(prayer_response['data']['timings']['Sunrise'], "%H:%M")
                dhuhr_12hr = datetime.strptime(prayer_response['data']['timings']['Dhuhr'], "%H:%M")
                asr_12hr = datetime.strptime(prayer_response['data']['timings']['Asr'], "%H:%M")
                asr_hanafi_12hr = datetime.strptime(asr_hanafi_response['data']['timings']['Asr'], "%H:%M")
                sunset_12hr = datetime.strptime(prayer_response['data']['timings']['Sunset'], "%H:%M")
                maghrib_12hr = datetime.strptime(prayer_response['data']['timings']['Maghrib'], "%H:%M")
                isha_12hr = datetime.strptime(prayer_response['data']['timings']['Isha'], "%H:%M")
                imsak_12hr = datetime.strptime(prayer_response['data']['timings']['Imsak'], "%H:%M")
                embed12=discord.Embed(title=f"Prayer times of {location}:",
                                      description=f'',
                                      color=discord.Color.orange())
                embed12.set_author(name=prayer_date, icon_url="https://images-ext-1.discordapp.net/external/u3RRy2sqPlkHUgO2HXkx-JEjTu0aZnFJfT4omEfrPM8/https/images-na.ssl-images-amazon.com/images/I/51q8CGXOltL.png")
                embed12.add_field(name="Fajr:", value=fajr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Sunrise:", value=sunrise_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Dhuhr:", value=dhuhr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Asr:", value=asr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Asr (Hanafi):", value=asr_hanafi_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Sunset:", value=sunset_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Maghrib:", value=maghrib_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Isha:", value=isha_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Imsak:", value=imsak_12hr.strftime("%I:%M %p"), inline=False)
                embed12.set_footer(text="If you aren't sure if your prayer times are correct, you can do it by state (New York City, NY), or by country (Moscow, RU)", icon_url="https://cdn.discordapp.com/attachments/1174896701526511666/1255684889911492709/warning-sign-30915_1280.png?ex=667e072f&is=667cb5af&hm=1f7578a95680876530da2a1830d7079cc7eb85b796e2a69b2f7a37e5bd935683&")
                if private_message == True:
                    await ctx.respond(embed=embed12)
                    print(f"Successfully sent prayer times to {ctx.author}")
                else:
                    await ctx.respond(embed=embed12)
                    print(f"Successfully sent prayer times to {ctx.author}")
            else:
                if private_message == True:
                    await ctx.respond(embed=embedmain)
                    print(f"Successfully sent prayer times to {ctx.author}")
                else:
                    await ctx.respond(embed=embedmain)
                    print(f"Successfully sent prayer times to {ctx.author}")
    else:
        prayer_url = f"http://api.aladhan.com/v1/timingsByAddress?address={location}&method={m}&school=0"
        asr_hanafi_link = f"http://api.aladhan.com/v1/timingsByAddress?address={location}&method={m}&school=1"
        try:
            prayer_requests = requests.get(prayer_url)
            prayer_response = prayer_requests.json()
            prayer_date = prayer_response['data']['date']['readable']
        except TypeError:
            embed=discord.Embed(title="",
                                description="This is not a valid location! (A valid location for example: New York City, New York)",
                                color=discord.Color.red())
            await ctx.respond(embed=embed)
        else:    
            asr_hanafi_request = requests.get(asr_hanafi_link)
            asr_hanafi_response = asr_hanafi_request.json()
            embedmain=discord.Embed(title=f"Prayer times of {location}:",
                                    description=f'',
                                    color=discord.Color.orange())
            embedmain.set_author(name=prayer_date, icon_url="https://images-ext-1.discordapp.net/external/u3RRy2sqPlkHUgO2HXkx-JEjTu0aZnFJfT4omEfrPM8/https/images-na.ssl-images-amazon.com/images/I/51q8CGXOltL.png")
            embedmain.add_field(name="Fajr:", value=prayer_response['data']['timings']['Fajr'], inline=False)
            embedmain.add_field(name="Sunrise:", value=prayer_response['data']['timings']['Sunrise'], inline=False)
            embedmain.add_field(name="Dhuhr:", value=prayer_response['data']['timings']['Dhuhr'], inline=False)
            embedmain.add_field(name="Asr:", value=prayer_response['data']['timings']['Asr'], inline=False)
            embedmain.add_field(name="Asr (Hanafi):", value=asr_hanafi_response['data']['timings']['Asr'], inline=False)
            embedmain.add_field(name="Sunset:", value=prayer_response['data']['timings']['Sunset'], inline=False)
            embedmain.add_field(name="Maghrib:", value=prayer_response['data']['timings']['Maghrib'], inline=False)
            embedmain.add_field(name="Isha:", value=prayer_response['data']['timings']['Isha'], inline=False)
            embedmain.add_field(name="Imsak:", value=prayer_response['data']['timings']['Imsak'], inline=False)
            embedmain.set_footer(text="If you aren't sure if your prayer times are correct, you can do it by state (New York City, NY), or by country (Moscow, RU)", icon_url="https://cdn.discordapp.com/attachments/1174896701526511666/1255684889911492709/warning-sign-30915_1280.png?ex=667e072f&is=667cb5af&hm=1f7578a95680876530da2a1830d7079cc7eb85b796e2a69b2f7a37e5bd935683&")
            if twelve_hour_format == True:
                fajr_12hr = datetime.strptime(prayer_response['data']['timings']['Fajr'], "%H:%M")
                sunrise_12hr = datetime.strptime(prayer_response['data']['timings']['Sunrise'], "%H:%M")
                dhuhr_12hr = datetime.strptime(prayer_response['data']['timings']['Dhuhr'], "%H:%M")
                asr_12hr = datetime.strptime(prayer_response['data']['timings']['Asr'], "%H:%M")
                asr_hanafi_12hr = datetime.strptime(asr_hanafi_response['data']['timings']['Asr'], "%H:%M")
                sunset_12hr = datetime.strptime(prayer_response['data']['timings']['Sunset'], "%H:%M")
                maghrib_12hr = datetime.strptime(prayer_response['data']['timings']['Maghrib'], "%H:%M")
                isha_12hr = datetime.strptime(prayer_response['data']['timings']['Isha'], "%H:%M")
                imsak_12hr = datetime.strptime(prayer_response['data']['timings']['Imsak'], "%H:%M")
                embed12=discord.Embed(title=f"Prayer times of {location}:",
                                      description=f'',
                                      color=discord.Color.orange())
                embed12.set_author(name=prayer_date, icon_url="https://images-ext-1.discordapp.net/external/u3RRy2sqPlkHUgO2HXkx-JEjTu0aZnFJfT4omEfrPM8/https/images-na.ssl-images-amazon.com/images/I/51q8CGXOltL.png")
                embed12.add_field(name="Fajr:", value=fajr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Sunrise:", value=sunrise_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Dhuhr:", value=dhuhr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Asr:", value=asr_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Asr (Hanafi):", value=asr_hanafi_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Sunset:", value=sunset_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Maghrib:", value=maghrib_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Isha:", value=isha_12hr.strftime("%I:%M %p"), inline=False)
                embed12.add_field(name="Imsak:", value=imsak_12hr.strftime("%I:%M %p"), inline=False)
                embed12.set_footer(text="If you aren't sure if your prayer times are correct, you can do it by state (New York City, NY), or by country (Moscow, RU)", icon_url="https://cdn.discordapp.com/attachments/1174896701526511666/1255684889911492709/warning-sign-30915_1280.png?ex=667e072f&is=667cb5af&hm=1f7578a95680876530da2a1830d7079cc7eb85b796e2a69b2f7a37e5bd935683&")
                if private_message == True:
                    try:
                        await ctx.author.send(embed=embed12)
                        embed=discord.Embed(title="",
                                            description="Successfully retrieved prayer times and sent them to direct messages!",
                                            color=discord.Color.green())
                        await ctx.respond(embed=embed)
                        print(f"Successfully sent prayer times to {ctx.author}")
                    except discord.errors.Forbidden:
                        embed=discord.Embed(title="",
                                            description="I cannot send you the prayer times because you have `Direct Messages` for this server off!",
                                            color=discord.Color.red())
                        await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=embed12)
                    print(f"Successfully sent prayer times to {ctx.author}")
            else:
                if private_message == True:
                    try:
                        await ctx.author.send(embed=embedmain)
                        embed2=discord.Embed(title="",
                                             description="Successfully retrieved prayer times and sent them to direct messages!",
                                             color=discord.Color.dark_green())
                        await ctx.respond(embed=embed2)
                        print(f"Successfully sent prayer times to {ctx.author}")
                    except discord.errors.Forbidden:
                        embed=discord.Embed(title="",
                                            description="I cannot send you the prayer times because you have `Direct Messages` for this server off!",
                                            color=discord.Color.red())
                        await ctx.respond(embed=embed)
                else:
                    await ctx.respond(embed=embedmain)
                    print(f"Successfully sent prayer times to {ctx.author}")

# letting the bot run
bot.run("")
