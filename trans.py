
import discord
from discord.ext import commands
from beem import Steem
from beem.account import Account
import asyncio
import os

steem = Steem(offline=True)
steem.set_default_nodes("https://api.steemit.com")

client = commands.Bot(command_prefix=';;')

@client.event
async def on_ready():
    print("bot is ready")
    await testt()

async def testt():
    while(True):
        account = Account('sourovafrin')
        mana = account.get_manabar()
        mana = round(mana["current_mana_pct"], 2)
        await client.change_presence(game=discord.Game(name="Manabar: " + str(mana), type=3))
        await asyncio.sleep(20)

SR=os.environ.get('SR')
SV=os.environ.get('SV')

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Vp checking command-----------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

@client.command()
async def vp(username):
    try:
        account = Account(username)
        mana = account.get_manabar()
        mana = round(mana["current_mana_pct"], 2)
        await client.say("**" + username + "'s** current voting power is **" + str(mana) + " %**")
    except Exception as exc:
        await client.say("i digged hard the steem blockchain but couldn't find :`"+username+ "`\nThat must be a typo, try again")
       
@vp.error
async def on_command_error(error , ctx):
    if isinstance(error, Exception,):
        await client.send_message(ctx.message.channel,str(error)+ " \nInput a valid username after the command. Formation: `;;vp <username>`")
        
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------Sending money on specific vp--------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

async def chk(ctx, username,amount,asset,vp,memo):
    asset = asset.upper()
    vp = float(vp)
    mana_base = 0
    while mana_base < vp:
        account = Account(username)
        mana = account.get_manabar()
        mana = round(mana["current_mana_pct"], 3)
        mana_base = mana
        await asyncio.sleep(1)

    if mana_base == vp:
        stm = Steem(node="https://api.steemit.com", keys=[SR])
        account = Account('sourovafrin', steem_instance=stm)
        account.transfer(username, amount, asset, memo)


@client.command(pass_context=True)
async def start(ctx,username, amount, asset, vp, memo):
    if ctx.message.author.id == "397972596207124480":
        vp=float(vp)
        account = Account(username)
        mana = account.get_manabar()
        mana = round(mana["current_mana_pct"], 3)
        if mana>vp:
            await client.say(username + "'s vp: " + str(mana) + " which is more than " + str(vp))
        elif mana<=vp:
            await client.say("**On vp reach, send money** process started. You will be mentioned after vp being reached and money being sent")
            await asyncio.ensure_future(chk(ctx,username,amount,asset,vp,memo))
            await client.say("<@397972596207124480> Successfully transferred " + str(amount) + " " + asset + " to " + username + " with following memo: `" + memo+"`")
    else:
        await client.say("You can't use this feature")
        

@start.error
async def on_command_error(error , ctx):
    if isinstance(error, Exception,):
        await client.send_message(ctx.message.channel,str(error)+ " \nCheck out if you have input something wrong.\n`Formation: ;;start <username> <amount> <asset> <vp> <memo>`")
    else:
        await client.send_message(ctx.message.channel, 'Something fishy')
        
#---------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------Transfer money command-----------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
        
@client.command(pass_context=True)
async def transfer(ctx,to,amount,asset_name,memo="Sent using sourovafrin's discord py bot"):
    asset_name = asset_name.upper()
    if ctx.message.author.id=="397972596207124480":
        await client.say("Type the username from which you want to send steem/sbd")
        response= await client.wait_for_message(timeout=30,author=ctx.message.author)
        res=str(response.clean_content)
        old = await client.say("Hold on, sending and counting your new balances ")
        stm = Steem(node="https://api.steemit.com", keys=[SR,SV])
        account = Account(res, steem_instance=stm)
        account.transfer(to, amount, asset_name, memo)
        await asyncio.sleep(2)
        acc = Account(res)
        inf = acc.get_balances()
        stm = inf['available'][0]
        sbdd = inf['available'][1]
        await client.delete_message(old)
        await client.say(res + " has successfully transferred `" + str(amount) + " " + asset_name + "` to `" + to + "` with following memo: `" + memo + "`.\nNew Balance: " + str(stm) + " and " + str(sbdd))
    else:
        await client.say("You can't use this feature")


@transfer.error
async def on_command_error(error ,ctx):
    if isinstance(error, Exception):
        if str(error)== "Command raised an exception: UnhandledRPCError: Assert Exception:_db.get_balance( o.from, o.amount.symbol ) >= o.amount: Account does not have sufficient funds for transfer.":
            await client.send_message(ctx.message.channel, "You don't have enough balance")
        else:
            await client.send_message(ctx.message.channel, str(error)+" \nCheck out if you have input something wrong.\n`Formation: ;;transfer <from> <to> <amount> <asset> <memo>`")


client.run(os.environ.get('TOKEN'))
