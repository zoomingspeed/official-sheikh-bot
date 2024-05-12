import discord
from discord.utils import get
from discord.ext import commands
from discord import default_permissions
from discord.ext import tasks
import random
import json
import quranpy
import pyquran as q
import dotenv
from dotenv import load_dotenv
import chat_exporter
import io
import asyncio
import os

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
                self.disable_all_items()
                await interaction.response.edit_message(view=self)
        
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
                user = interaction.user
                embed2=discord.Embed(title="",
                                    description="Bookmark saved!",
                                    color=discord.Color.green())
                embed2.set_author(name=f"{surah_variable}:{verse_variable} ({surah_name}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{surah_variable}_{verse_variable}.png")
                await ctx.respond("Bookmark saved!", ephemeral=True)
                message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                await message.pin()
        
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
                    embed2=discord.Embed(title="",
                                        description="Bookmark saved!",
                                        color=discord.Color.green())
                    embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                    embed2.add_field(name="Translation (Sahih International):", value=f"{print_short_string}...", inline=False)
                    embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                    embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
                    await ctx.respond("Bookmark saved!", ephemeral=True)
                    message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                    await message.pin()
                else:
                    embed2=discord.Embed(title="",
                                        description="Bookmark saved!",
                                        color=discord.Color.green())
                    embed2.set_author(name=f"{integer1_int}:{integer2_int} ({surah_variable}):", icon_url="https://cdn6.aptoide.com/imgs/6/a/6/6a6336c9503e6bd4bdf98fda89381195_icon.png")
                    embed2.add_field(name="Translation (Sahih International):", value=f"{translation}", inline=False)
                    embed2.add_field(name="The Ayah/Verse (In the name of Allah, the most gracious, the most merciful):", value="", inline=False)
                    embed2.set_image(url=f"https://cdn.islamic.network/quran/images/high-resolution/{integer1_int}_{integer2_int}.png")
                    await ctx.respond("Bookmark saved!", ephemeral=True)
                    message = await user.send(embed=embed2, view=CoolBookMark(timeout=None))
                    await message.pin()
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
    if ctx.author.guild_permissions.ban_members:
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
                                        color=discord.Color.greed())
                    await member.ban(embed=embed)
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
                    embed.add_field(title="**Reason:**", value=reason, inline=False)
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
    else:
        embed=discord.Embed(title="",
                            description="You do not have permissions to ban other members!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed)
        print(f"Bot could not ban {member} from {guild} due to {ctx.author} having insufficient permissions")

# kick command
@bot.slash_command(name="kick", description="Kick other members from your server!")
@default_permissions(kick_members = True)
@commands.guild_only()
async def kick(ctx, member : discord.Member, reason=None):
    guild = ctx.guild
    coolbotvar = guild.me
    if ctx.author.guild_permissions.kick_members:
        if member == coolbotvar:
            embed=discord.Embed(title="",
                                description="I cannot kick myself!",
                                color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            if reason == None:
                guild = ctx.guild
                embed=discord.Embed(title="Kick successful!",
                                    color=discord.Color.green())
                embed.add_field(name="", value=f"Successfully kicked {member.mention}, no reason provided.")
                await member.send(f"You have been kicked from {guild}, no reason provided.")
                await ctx.respond(embed=embed)
                await member.kick()
                print(f"{ctx.author} has successfully kicked {member} from {guild}, no reason provided.")
            else:
                embed=discord.Embed(title="Kick successful!",
                                    color=discord.Color.green())
                embed.add_field(name="", value=f"Successfully kicked {member.mention}!", inline=False)
                embed.add_field(name="**Reason:**", value=reason, inline=False)
                await ctx.respond(embed=embed)
                await member.send(f"You have been kicked from {guild} due to the following reason: ```{reason}```")
                await member.kick()
                print(f"{ctx.author} has successfully kicked out {member} from {guild} due to the following reason: {reason}")
    else:
        embed=discord.Embed(title="",
                            description="You do not have permissions to kick other members!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed)

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
async def help(ctx, option=None):
    if option == None:
        embed=discord.Embed(title="HELP",
                            description="Here are the different ways you can call the help command:",
                            color=discord.Color.blurple())
        embed.add_field(name="**COMMANDS:**", value="/help commands")
        embed.add_field(name="**ADMINISTRATOR COMMANDS:**", value="/help admin")
        await ctx.respond(embed=embed)
    elif option == "commands":
        embed=discord.Embed(title="Commands:",
                            description="Here are all of the commands available with the bot:",
                            color=discord.Color.green())
        embed.add_field(name="**Quran Commands**", value="/vquran (surah number, verse number), /quran (surah number, verse number)", inline=False)
        embed.add_field(name="**Prayertime Command**", value="/prayertimes", inline=False)
        embed.add_field(name="**Close ticket:**", value="/closeticket (only works in ticket channel)")
        await ctx.respond(embed=embed)
    elif option == "admin":
        embed=discord.Embed(title="**ADMINISTRATOR COMMANDS:**",
                            description="Administrator commands for Sheikh Bot",
                            color=discord.Color.yellow())
        embed.add_field(name="Ban command:", value="/ban (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Mute command:", value="/mute (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Kick command:", value="/kick (ping user) (**OPTIONAL:** reason)", inline=False)
        embed.add_field(name="Activate tickets:", value="/activatetickets **(REQUIRES ADMINISTRATOR)**")
        await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="",
                            description="Invalid help category!",
                            color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
        
# prayer time command
@bot.slash_command(name="prayertimes", description="Check your local towns prayer times")
async def prayertimes(ctx):
    guild = ctx.guild
    await ctx.respond("Here are your local prayer times: https://islamicfinder.org/")
    print(f"Successfully sent prayer times to {ctx.author} in {guild}")

# letting the bot run
bot.run("")
