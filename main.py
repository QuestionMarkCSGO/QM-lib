import discord
import time
import asyncio
from discord.ext import commands
from bembed import Bembed
from log_guilds import log_guilds
import brofile # better profiles for dicord
#from lib.timer import Timer

# create bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), description='Random Team Generator')

# show connected servers if ready
@bot.event
async def on_ready():
    log_guilds(bot)

@bot.event
async def on_message(msg):
    if msg.author == bot.user: # ignore if message was send by the bot
        return
    brofile.set_player(msg.author)
    brofile.add_xp(msg.author, 10)
    await bot.process_commands(msg)

@bot.command()
async def test(ctx):
    #
    # async def some_callback(timer, time):
    #     print('callback: ' + timer.name + ", time: " + str(time))
    #
    # def end_func(timer):
    #     print(f'Custom callback end from {timer.name}')

    # timer1 = Timer(time=15, name="Timer 1", callback=some_callback, end_func=end_func)

    bemb = Bembed(bot=bot, title='test')
    await bemb.send(ctx.channel)
    #await bemb.update('addimg', 'image.jpg')
    #warning =  Bembed()
    #await warning.set_error('Marko Dog!')
    #await warning.send(ctx.channel)
    #emb = Bembed('txt', 'Test!', 'Hallo Test Embed!!', 'BLuE', bot=bot, author={'name': 'Jichael Mackson', 'url':'https://google.de', 'icon': 'https://cdn.onlinewebfonts.com/svg/img_311588.png'})
    #await emb.send(ctx.channel)
    #await emb.update('addfields', {'test':['myval', False] , 'moretest':['mrevlue', False]})
    #print(f'emb type: {emb.type}')
    #await emb.update('addfields', {'testing':['myvale2', True] , 'moretestino':['mrevlue', True]})
    #await emb.update('remfield', 'test')
    #await emb.update('clearfields')
    await bemb.update('addthb', 'image.jpg')


    # await emb.update('remimg')
    # time.sleep(3)
    # await emb.update('addfields', {'Loww':['Heloowwww', True] , 'Brrrt':['Pow', False]})
    await bemb.add_reaction('😊')
    await bemb.add_reaction('❤')
    #await emb.update('remimage')

    await ctx.message.delete()


@bot.command()
async def emb(ctx, title, desc, color='red'):
    emb = Bembed('txt', title, desc, color)
    await emb.send(ctx.channel)
    await ctx.message.delete()

# get the token
from get_token import token

# run the bot
bot.run(token)
