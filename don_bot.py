from typing import Optional, Literal
from secret_info import my_token
import discord
import sqlite3
import logging
from discord.ext import commands
from discord import ui, app_commands


MY_GUILD = discord.Object(id=684162731196153896)  # replace with your guild id

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


conn = sqlite3.connect('character.db')
c = conn.cursor()

all_classes = Literal['Warrior (Male)', 'Warrior (Female)',
                      'Mage' ,'Martial Artist (Male)' , 'Martial Artist (Female)',
                      'Gunner (Male)', 'Gunner (Female)', 'Assassin', 'Specialist']

class test_modal(ui.Modal, title = "Test Modal"):
    answer = ui.TextInput(label = "peepee", style=discord.TextStyle.short, placeholder="pensballs", default="csss", required=True)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title, description=f"**{self.answer.label}**\n{self.answer}")
        embed.set_author(name = interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

class PaginationTest(ui.View):

    def __init__(self, roster):
        self.roster = roster

    current_page : int = 1
    async def send(self, interaction):
        self.message = await interaction.send(view=self)
    
    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        pass


# class add_character_modal(ui.Modal, title = "Add Character"):
#     character_name = ui.TextInput(label = "Character Name", style=discord.TextStyle.short, placeholder="Please enter the character's name.", required=True)
#     character_name = ui.TextInput(label = "Character Name", style=discord.TextStyle.short, placeholder="Please enter the character's name.", required=True)
#     async def on_submit(self, interaction: discord.Interaction):
#         #embed = discord.Embed(title=self.title, description=f"**{self.answer.label}**\n{self.answer}")
#         #embed.set_author(name = interaction.user, icon_url=interaction.user.avatar)
#         #await interaction.response.send_message(embed=embed)
    



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



@bot.tree.command()
async def modal_test(interaction: discord.Interaction):
    await interaction.response.send_modal(test_modal())


@bot.tree.command()
async def pagination_test(interaction: discord.Interaction):
    data = range(1,15)
    pagination_view = PaginationTest()
    pagination_view.data = data
    await pagination_view.send(interaction)


@bot.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')




#This command adds another character to the user's roster.
@bot.tree.command()
@app_commands.rename(character_class='class')
@app_commands.describe(
    name='The name of the character',
    character_class='The class of the character',
    item_level='The item_level of the character',
    gold_earning='If the character is gold earning or not',
)
async def add_character(interaction: discord.Interaction, name: str, character_class: all_classes, item_level: int, gold_earning: Literal['Yes', 'No']):
    gold = 1 if gold_earning == 'Yes' else 0
    c.execute("INSERT INTO character VALUES (?, ?, ?, ?, ?)", (interaction.user.id, name, character_class, item_level, gold))
    conn.commit()
    if c.rowcount >= 0:
        await interaction.response.send_message(f'{name} has been added to your list of characters!')
    else:
        await interaction.response.send_message(f'Character was unsucessfully added.')

# #This command adds another character to the user's roster.
# @bot.tree.command()
# @app_commands.rename(character_class='class')
# async def test_add_character(interaction: discord.Interaction, name: str, character_class: str, item_level: int, gold_earning: Literal['Yes', 'No']):
#     #c.execute("INSERT INTO character VALUES (?, ?, ?, ?, ?)", (interaction.user.id, name, character_class, item_level, gold_earning))
#     #conn.commit()
#     #print(gold_earning)
#    # if c.rowcount >= 0:
#     await interaction.response.send_message(f'{name} has been added to your list of characters!')
#     #else:
#         #await interaction.response.send_message(f'Character was unsucessfully added.')


@bot.tree.command()
async def roster(interaction: discord.Interaction):
    characters = ""
    c.execute("SELECT * FROM character WHERE user_id=?", (interaction.user.id,))
    result = c.fetchall()
    for character in result:
        characters += f"Character: {character[1]}, Class: {character[2]}, ilvl: {character[3]}\n"
    conn.commit()
    await interaction.response.send_message(f'{characters}')




#syncs the bot's commands to all guilds 
@bot.command()
async def sync(ctx):
    if ctx.author.id == 289901600078692352:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')


bot.run(my_token)