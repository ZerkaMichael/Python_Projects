from functions import *
from embeds import *

client = commands.Bot(command_prefix = '.')
intents = discord.Intents.all()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    crypto_prices_channel_loop.start()
    channel_status_loop.start()
    critical_notifications.start()
    stock_prices_channel_loop.start()

@tasks.loop(minutes=1)
async def critical_notifications():
    channel = client.get_channel(803499281612013568)
    temp = await get_crypto('bitcoin','1hr')
    if(temp*100 > 1):
        await channel.send("BITCOIN MOVES!")
    temp = await get_crypto('ethereum','1hr')
    if(temp *100 > 1):
        await channel.send("ETHEREUM MOVES!")

@tasks.loop(minutes=10)
async def channel_status_loop():
        response_BTC = await get_crypto('bitcoin','price')
        guild = client.get_guild(775232804660969504);
        members = str(guild.member_count)
        channel_btc = client.get_channel(799181755260862504)
        channel_members = client.get_channel(799096256424574986)
        await channel_btc.edit(name = 'BTC Price: $' + str(response_BTC))
        await channel_members.edit(name = 'Members: ' + members)
        print("Date/Time: " + get_Date_Time() + " => " + "Updated voice channel statuses")

@tasks.loop(minutes=1)
async def crypto_prices_channel_loop():
        channel = client.get_channel(801685694488510484)
        embed1 = contruct_embed_prices1(
            response_BTC = await get_crypto('bitcoin','price'),
            response_ETH = await get_crypto('ethereum','price'),
            response_XRP = await get_crypto('ripple','price'),
            response_ALGO = await get_crypto('algorand','price'),
            response_LINK = await get_crypto('chainlink','price'),
            response_COS = await get_crypto('cosmos','price'),
            response_SOL = await get_crypto('solana','price'),
            response_GRT = await get_crypto('the-graph','price'),
            response_BTC_1hrchng = await get_crypto('bitcoin','1hr'),
            response_ETH_1hrchng = await get_crypto('ethereum','1hr'),
            response_XRP_1hrchng = await get_crypto('ripple','1hr'),
            response_LINK_1hrchng = await get_crypto('chainlink','1hr'),
            response_ALGO_1hrchng = await get_crypto('algorand','1hr'),
            response_COS_1hrchng = await get_crypto('cosmos','1hr'),
            response_GRT_1hrchng = await get_crypto('the-graph','1hr'),
            response_SOL_1hrchng = await get_crypto('solana','1hr'),
            response_BTC_24hrchng = await get_crypto('bitcoin','24hr'),
            response_ETH_24hrchng = await get_crypto('ethereum','24hr'),
            response_XRP_24hrchng = await get_crypto('ripple','24hr'),
            response_LINK_24hrchng = await get_crypto('chainlink','24hr'),
            response_ALGO_24hrchng = await get_crypto('algorand','24hr'),
            response_COS_24hrchng = await get_crypto('cosmos','24hr'),
            response_SOL_24hrchng = await get_crypto('solana','24hr'),
            response_GRT_24hrchng = await get_crypto('the-graph','24hr'))
        embed2 = contruct_embed_prices2(
            response_REN = await get_crypto('republic-protocol','price'),
            response_LTC = await get_crypto('litecoin','price'),
            response_MATIC = await get_crypto('matic-network','price'),
            response_ADA = await get_crypto('cardano','price'),
            response_AXS = await get_crypto('axie-infinity','price'),
            response_BAT = await get_crypto('basic-attention-token','price'),
            response_DOT = await get_crypto('polkadot','price'),
            response_SHIB = await get_crypto('shiba-inu','price'),
            response_REN_1hrchng = await get_crypto('republic-protocol','1hr'),
            response_LTC_1hrchng = await get_crypto('litecoin','1hr'),
            response_MATIC_1hrchng = await get_crypto('matic-network','1hr'),
            response_ADA_1hrchng = await get_crypto('cardano','1hr'),
            response_AXS_1hrchng = await get_crypto('axie-infinity','1hr'),
            response_BAT_1hrchng = await get_crypto('basic-attention-token','1hr'),
            response_DOT_1hrchng = await get_crypto('polkadot','1hr'),
            response_SHIB_1hrchng = await get_crypto('shiba-inu','1hr'),
            response_REN_24hrchng = await get_crypto('republic-protocol','24hr'),
            response_LTC_24hrchng = await get_crypto('litecoin','24hr'),
            response_MATIC_24hrchng = await get_crypto('matic-network','24hr'),
            response_ADA_24hrchng = await get_crypto('cardano','24hr'),
            response_AXS_24hrchng = await get_crypto('axie-infinity','24hr'),
            response_BAT_24hrchng = await get_crypto('basic-attention-token','24hr'),
            response_DOT_24hrchng = await get_crypto('polkadot','24hr'),
            response_SHIB_24hrchng = await get_crypto('shiba-inu','24hr'))
        await channel.purge(limit=6)
        await channel.send(embed=embed2)
        await channel.send(embed=embed1)
        print("Date/Time: " + get_Date_Time() + " => " + "Updated crypto prices in channel embed")

@tasks.loop(minutes=5)
async def stock_prices_channel_loop():
    channel_Stock_Prices = client.get_channel(803880169722085386)
    tsla_Stock_Price = await get_stock_price('tsla')
    spy_Stock_Price = await get_stock_price('spy')
    amd_Stock_Price = await get_stock_price('amd')
    gme_Stock_Price = await get_stock_price('gme')
    amc_Stock_Price = await get_stock_price('amc')
    clne_Stock_Price = await get_stock_price('clne')
    embed = contruct_embed_stockprices(tsla_Stock_Price,spy_Stock_Price,amd_Stock_Price,gme_Stock_Price,amc_Stock_Price,clne_Stock_Price)
    await channel_Stock_Prices.purge(limit=1)
    await channel_Stock_Prices.send(embed=embed)
    print("Date/Time: " + get_Date_Time() + " => " + "Updated stock prices in channel embed")

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def test(ctx, *, arg):
    await ctx.send(response.text)

@client.command()
async def articleanalysis(ctx, *, arg):
    embed = await ArticleAnalysis(arg)
    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, x=0):
    await ctx.channel.purge(limit=x+1)

@client.command()
async def stock(ctx, *, arg):
    p = await get_stock_price(arg.upper())
    await ctx.send(arg.upper()+" is at: $" + str(p))

@client.command()
async def crypto(ctx, *, arg, arg1):
    p = await get_crypto(arg,arg1)
    await ctx.send(arg.upper()+" is at: $" + str(p))



client.run('Nzg2MTU5OTgxNDY4MTg4Njg0.X9CWiQ.BIkjogztGosRxJ3COozCQTsGp5c')
