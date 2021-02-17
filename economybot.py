import os
import discord
from discord.ext import commands
import random
import aiosqlite
import asyncio


token = os.getenv('SECRET')



bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

#db = sqlite3.connect("BankAccounts.db")
#cur = db.cursor()
START_BALANCE = 1000
START_WALLET = 1000



@bot.event
async def on_ready():
    print(f'we are ready to go. logged in as bot')

@bot.command()
async def balance(ctx):
    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()

    if result_userID is None:
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute('insert into Accounts(user_name, user_id, balance, wallet) values(?,?,?,?)', (USER_NAME, USER_ID, START_BALANCE, START_WALLET))
            await db.commit()
        await ctx.send('We gave you 2000c. you now have 1kc in your bank and other half in wallet')
    else:   
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
            #SQL.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
            result_userbal = await cur.fetchone()
            await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
            result_userwallet = await cur.fetchone()
        emb = discord.Embed(title='Bank')
        emb.add_field(name='Wallet: ', value=f'{result_userbal[0]}$', inline=False)
        emb.add_field(name='Bank: ', value=f'{result_userwallet[0]}$', inline=False)
        await ctx.send(embed=emb)

@bot.command()
async def beg(ctx):

    USER_ID = ctx.message.author.id
    USER_NAME = str(ctx.message.author)
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select user_id from Accounts where user_id="{USER_ID}"')
        result_userID =await cur.fetchone()

    if result_userID is None:
        await ctx.send(f'{ctx.message.author.mention} please create an account using balance command')
    else:
        #db.commit()
        random_amount = random.randint(0,100)
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET balance = balance + {random_amount} where user_id={USER_ID}')
            await db.commit()
        await ctx.send(f'Daddy gave you {random_amount}')

@bot.command()
async def deposite(ctx, amount:int):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('🖕Please create an account using balance command before you deposite')  
    elif result_userID:      
        wallet_balance = int(result_userID[0])
    if amount > wallet_balance:
        await ctx.send('You do not have enough money to do that')
    elif str(amount) <= str(wallet_balance):
        async with aiosqlite.connect("BankAccounts.db") as db:     
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET wallet = wallet + {int(amount)} where user_id={USER_ID}')
            await db.commit()
            await cur.execute(f'UPDATE Accounts SET balance = balance - {int(amount)} where user_id={USER_ID}')
            await db.commit()
        await ctx.send(f'Successfully transfered {amount} to your bank')    
    else:
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead")    

@bot.command()
async def withdraw(ctx, amount:int):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute('create table if not exists Accounts("Num" integer primary key autoincrement,"user_name" text, "user_id" integer not null, "balance" integer,"wallet" integer)')
        await cur.execute(f'select wallet from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('🖕Please create an account using balance command before you deposite')
    elif result_userID:
        bank_balance = int(result_userID[0])
    if amount > bank_balance:
        await ctx.send('You do not have enough money to do that')
    elif str(amount) <= str(bank_balance):
        async with aiosqlite.connect("BankAccounts.db") as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE Accounts SET wallet = wallet - {int(amount)} where user_id={USER_ID}')
            await db.commit()
            await cur.execute(f'UPDATE Accounts SET balance = balance + {int(amount)} where user_id={USER_ID}')
            await db.commit() 
        await ctx.send(f'Successfully withdrawn {amount}')
    else:
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead")                     


@deposite.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(f"{ctx.message.author.mention} That's why yo mama dead")

@bot.command()
async def search(ctx):
    USER_ID = ctx.message.author.id
    async with aiosqlite.connect("BankAccounts.db") as db:
        cur = await db.cursor()
        await cur.execute(f'select balance from Accounts where user_id="{USER_ID}"')
        result_userID = await cur.fetchone()
    if result_userID is None:
        await ctx.send('Mofo Create an account first using balance command')    
    else:
        options = ['Socks', 'Hell', 'Toilet', 'Dog', 'Lawn', 'Couch', 'Sex house']
        option1 = random.choice(options)
        options.remove(option1)
        option2 = random.choice(options)
        options.remove(option2)
        option3 = random.choice(options)

        embed1 = discord.Embed(title='Disclaimer',description='What do you want to search', color=0xfcba03)
        embed1.add_field(name='search', value=f"``{option1}``,``{option2}``, ``{option3}`` ")
        await ctx.send(embed=embed1)

        def msg_check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel

        try:
            response = await bot.wait_for('message', check=msg_check, timeout=10.0)
            if str(response) == option1.lower() or option2.lower() or option3.lower():
                random_money = random.randint(0,2000)
                async with aiosqlite.connect("BankAccounts.db") as db:
                    cur = await db.cursor()
                    await cur.execute(f'UPDATE Accounts SET balance = balance + {random_money} where user_id={USER_ID}')
                    await db.commit()
                await ctx.send(f'``You searched {response.content} and found {random_money}$ ``')
            else:
                await ctx.send('Bruh')    
        except asyncio.TimeoutError:
            await ctx.send('Dumbass you ran out of time')

bot.run(token)
