import discord
import os
from discord.ext import commands
import requests
import asyncio
from beem.account import Account


client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("bot is ready")
    await client.change_presence(game=discord.Game(name='Hd Porn', type=3))

@client.command(pass_context=True)
async def ping(ctx):
    await client.say('pong')
    await client.delete_message(ctx.message)

@client.command(pass_conetext=True)
async def flw(username):
    try:
        account = Account(username)
        inf = account.get_follow_count()
        msg = await client.say("Digging Steem Blockchain......")
        await asyncio.sleep(1)
        await client.edit_message(msg, "```" + username + " has " + str(
            inf["follower_count"]) + " followers and he is following " + str(inf["following_count"]) + " others```")
    except Exception as tut: await client.say("Username not found")

@client.command(pass_context=True)
@commands.has_role("bot-commander")
async def clr(ctx,amount=10):
    if amount<=100:
        channel=ctx.message.channel
        messages=[]
        async for message in client.logs_from(channel,limit=int(amount)+1):
            messages.append(message)
        old =await client.say("```Deleting message for you......```")
        await client.delete_messages(messages)
        await asyncio.sleep(1)
        new_m = await client.edit_message(old,"```Deleted "+str(amount)+" Messages```")
        await asyncio.sleep(2)
        await client.delete_message(new_m)
    else:
        await client.say("Sorry, can't delete more than 100 messages at once, please try within 2-100")

@client.command()
async def steem(amountt):
    url = 'https://api.coinmarketcap.com/v1/ticker/steem/'
    response = requests.get(url)
    value = response.json()[0]["price_usd"]
    amount = float(amountt)
    fl_value = float(value)
    tot_value = fl_value * amount
    bn_value = tot_value * 85
    await client.say("```The current price of " + str(amountt) + " steem is " + str(round(tot_value, 2)) + "$ or "+ str(round(bn_value, 2))+ " BDT```")


@client.command()
async def sbd(amountt):
    url = 'https://api.coinmarketcap.com/v1/ticker/steem-dollars/'
    response = requests.get(url)
    value = response.json()[0]["price_usd"]
    amount = float(amountt)
    fl_value = float(value)
    tot_value = fl_value * amount
    bn_value = tot_value * 85
    await client.say("```The current price of " + str(amountt) + " sbd is " + str(round(tot_value, 2)) + "$ or "+ str(round(bn_value, 2))+ " BDT```")

@clr.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await client.send_message(ctx.message.channel,"You don't have required permission to delete messages")
    else:
        await client.send_message(ctx.message.channel, "Seems you are trying to delete messages which are older than 14 days. Sorry it can't be done")
        messages = []
        async for message in client.logs_from(ctx.message.channel, limit=3):
            messages.append(message)
        await asyncio.sleep(2)
        await client.delete_messages(messages)


@steem.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await client.send_message(ctx.message.channel,"Please type an amount. Example: `.steem 1`")
    else:
       await client.send_message(ctx.message.channel, "Command mismatch! Correct formation `.steem <amount>`")

@sbd.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await client.send_message(ctx.message.channel,"Please type an amount. Example: `.sbd 1`")
    else:
       await client.send_message(ctx.message.channel, "Command mismatch! Correct formation `.sbd <amount>`")

@client.command(pass_context=True)
async def echo(ctx,*args):
    await client.delete_message(ctx.message)
    output=''
    for word in args:
        output+=word
        output+=' '
    await client.say(output)

@client.event
async def on_message(msg):

    if msg.content.lower() == "/who r u":
        await client.send_message(msg.channel,'Hi, i am a discord py bot. I was summoned by my master :fire: <@397972596207124480> :fire:')
    if msg.content.lower() == "/mamacheck":
        role_names = [role.name for role in msg.author.roles]
        if "bot-commander" in role_names:
            await client.delete_message(msg)
            await client.send_message(msg.channel, " আরে  মাম্মা  আমি লাইনে আছি 😉  কুছ চেক কর  নেকি জারুরত নেহি 😘")
        else:
            await client.send_message(msg.channel, "you do not have the permission to use this command")

    if msg.content.lower() == "ayasha is beautiful":
        await client.add_reaction(msg,'😂')
        await client.send_message(msg.channel, " মাম্মা মিছা করা কওয়া বাদ দেন,  হেয় কি আপনেরে  এর লাইগা টাকা দিব মনে করছেন? ")
    await client.process_commands(msg)
    
client.run(os.environ.get('TOKEN'))
