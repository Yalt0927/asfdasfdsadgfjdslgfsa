
# 필수설치 모듈
#pip install discord
#pip install captcha
#pip install asyncio

import discord
from captcha.image import ImageCaptcha
import random
import time
import asyncio
import datetime

client = discord.Client()
token = 'ODY0MDg2ODA0MzQ0MjA5NDA4.YOwVjA.VEq55DMVhPuDN7Pj3lpUuMkLrNA'
gaming = 'Made By CHOCOBAR'
channel = '864414932870365204'

@client.event
async def on_ready():
    print("인증 봇이 정상적으로 실행되었습니다.")
    game = discord.Game(gaming)
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith("!인증"):    #명령어 !인증
        if not message.channel.id == int(channel):
            return
        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author. id) + ".png"
        Captcha_img.write(a, name)

        await message.channel.send(f"""{message.author.mention} 아래 숫자를 10초 내에 입력해주세요. """)
        await message.channel.send(file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check) # 제한시간 10초
        except:
            await message.channel.purge(limit=3)
            chrhkEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            chrhkEmbed.add_field(name='닉네임', value=message.author, inline=False)
            chrhkEmbed.add_field(name='이유', value='시간초과', inline=False)
            await message.channel.send(embed=chrhkEmbed)
            print(f'{message.author} 님이 시간초과로 인해 인증을 실패함.')
            return

        if msg.content == a:
            role = discord.utils.get(message.guild.roles, name="유저")
            await message.channel.purge(limit=4)
            tjdrhdEmbed = discord.Embed(title='인증성공', color=0x04FF00)
            tjdrhdEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tjdrhdEmbed.add_field(name='3초후 인증역할이 부여됩니다.', value='** **', inline=False)
            tjdrhdEmbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=tjdrhdEmbed)
            await asyncio.sleep(3)
            await message.author.add_roles(role)
        else:
            await message.channel.purge(limit=4)
            tlfvoEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            tlfvoEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tlfvoEmbed.add_field(name='이유', value='잘못된 숫자', inline=False)
            await message.channel.send(embed=tlfvoEmbed)
            print(f'{message.author} 님이 잘못된 숫자로 인해 인증을 실패함.')


@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    else:
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        h = datetime.datetime.now().hour
        min = datetime.datetime.now().minute
        bot_logs = '864412846237155329'
        embed = discord.Embed(title='메시지 수정됨', colour=discord.Colour.orange())
        embed.add_field(name='유저', value=f'<@{before.author.id}>({before.author})', inline=False)
        embed.set_footer(text=f"유저 ID:{before.author.id} • 메시지 ID: {before.id}")
        embed.add_field(name='수정 전', value=before.content + "\u200b", inline=True)
        embed.add_field(name='수정 후', value=after.content + "\u200b", inline=True)
        embed.add_field(name='날짜', value=f"{y}-{m}-{d} {h}:{min}", inline=False)
        await client.get_channel(int(bot_logs)).send(embed=embed)

@client.event
async def on_message_delete(message):
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    h = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    bot_logs = '864412846237155329'
    embed = discord.Embed(title='메시지 삭제됨', colour=discord.Colour.orange())
    embed.add_field(name='유저', value=f'<@{message.author.id}>({message.author})')
    embed.add_field(name='채널', value=f'<#{message.channel.id}>')
    embed.add_field(name='내용', value=message.content, inline=False)
    embed.add_field(name='날짜', value=f"{y}-{m}-{d} {h}:{min}", inline=False)
    embed.set_footer(text=f"유저 ID:{message.author.id} • 메시지 ID: {message.id}")
    await client.get_channel(int(bot_logs)).send(embed=embed)

@client.event
async def on_message(message):
    if message.content.startswith('!청소'):
        try:
            # 메시지 관리 권한 있을시 사용가능
            if message.author.guild_permissions.manage_messages:
                amount = message.content[4:]
                await message.delete()
                await message.channel.purge(limit=int(amount))
                message = await message.channel.send(embed=discord.Embed(title='🧹 메시지 ' + str(amount) + '개 삭제됨', colour=discord.Colour.green()))
                await asyncio.sleep(2)
                await message.delete()
            else:
                await message.channel.send('``명령어 사용권한이 없습니다.``')
        except:
            pass

@client.event
async def on_message(message):
    if message.content.startswith('!폭파'):
        if message.author.guild_permissions.ban_members:
            aposition = message.channel.position
            new = await message.channel.clone()
            await message.channel.delete()
            await new.edit(position=aposition)

            embed = discord.Embed(title='채널 폭파됨', colour=discord.Colour.red())
            embed.set_image(url='https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif')
            await new.send(embed=embed)
        else:
            await message.channel.send('``명령어 사용권한이 없습니다.``')

client.run(token)


