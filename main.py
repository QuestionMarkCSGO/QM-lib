import discord
import time
import asyncio
from discord.ext import commands
import lib.bembed
import lib.timer
import lib.helper as hlp

# create bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or('-'), description='Random Team Generator')

# show connected servers if ready
@bot.event
async def on_ready():

    hlp.log_guilds(bot)

@bot.event
async def on_message(msg):
    if msg.author.id == bot.id: # ignore if message was send by the bot
        return

    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    #
    # async def some_callback(timer, time):
    #     print('callback: ' + timer.name + ", time: " + str(time))
    #
    # def end_func(timer):
    #     print(f'Custom callback end from {timer.name}')

    # timer1 = Timer(time=15, name="Timer 1", callback=some_callback, end_func=end_func)


    emb = Bembed('txt', 'Test!', 'Hallo Test Embed!!', 'BLuE', bot=bot, author={'name': 'Jichael Mackson', 'url':'https://google.de', 'icon': 'https://cdn.onlinewebfonts.com/svg/img_311588.png'})
    await emb.send(ctx.channel)
    await emb.update('addfields', {'test':['myval', False] , 'moretest':['mrevlue', False]})
    #await emb.update('addfields', {'testing':['myvale2', True] , 'moretestino':['mrevlue', True]})
    await emb.update('remfield', 'test')
    await emb.update('clearfields')
    await emb.update('addimage', 'image.jpg')
    # await emb.update('remimage')
    # time.sleep(3)
    # await emb.update('addfields', {'Loww':['Heloowwww', True] , 'Brrrt':['Pow', False]})
    await emb.add_reaction('😊')
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
