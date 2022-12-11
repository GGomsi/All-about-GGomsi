import discord
import asyncio
import random
import csv
import operator
import pandas as pd
df1 = pd.read_csv('mmrlist1.csv')
df1.head()

from discord.utils import get

client = discord.Client()



@client.event
async def on_ready():
    print(client.user.name)
    print('성공적으로 봇이 시작되었습니다')
    game = discord.Game('헤으응') # ~~ 하는중
    await client.change_presence(status=discord.Status.online, activity=game)
    


# 대기열
@client.event
async def on_message(message):
       
    if message.content.startswith("!호스트"):
        await message.channel.purge(limit=1)        
        tank = 0
        deal = 0
        heal = 0
        tank_list = []
        deal_list = []
        heal_list = []
        all_list = []
        await message.channel.send (f"`!참가 포지션`을 입력하세요")
        waitembed = discord.Embed(
            title = "매칭 대기중",
            description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}",
            color=0x4000FF
        ) 
        wait = await message.channel.send(embed=waitembed)
                        
        while tank < 2 or deal < 6 or heal < 2:
            def join(m):
                return m.content in ['!참가 탱커','!참가 딜러', '!참가 힐러', '!취소'] and m.channel == message.channel
            coin = await client.wait_for("message", check=join)
            
            if coin.content == "!참가 탱커":
                await message.channel.purge(limit=1)                
                
                if tank == 2:
                    await message.channel.send (f"탱커는 더이상 참가 할 수 없습니다.")
                    await message.channel.purge(limit=1)
                
                else:
                    try: 
                        if all_list.index(coin.author.id) <= 9:
                            await message.channel.send (f"이미 참가 하셨습니다.")
                    except ValueError:
                        tank += 1
                        tank_list.append(coin.author.name)
                        all_list.append(coin.author.id)                       
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))
                    
                     
            elif coin.content == "!참가 딜러":
                await message.channel.purge(limit=1)
                
                if deal == 6:    
                    await message.channel.send (f"딜러는 더이상 참가 할 수 없습니다.")
                    await message.channel.purge(limit=1)
                
                else:
                    try: 
                        if all_list.index(coin.author.id) <= 9:
                            await message.channel.send (f"이미 참가 하셨습니다.")       
                    except ValueError:
                        deal +=1
                        deal_list.append(coin.author.name) #id or name 결정
                        all_list.append(coin.author.id)
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))

            elif coin.content == "!참가 힐러":
                await message.channel.purge(limit=1)
                
                if heal == 2:
                    await message.channel.send (f"힐러는 더이상 참가 할 수 없습니다.")
                    await message.channel.purge(limit=1)
                
                else:
                    try: 
                        if all_list.index(coin.author.id) <= 9:
                            await message.channel.send (f"이미 참가 하셨습니다.")        
                    except ValueError:
                        heal +=1
                        heal_list.append(coin.author.name)
                        all_list.append(coin.author.id)
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))
            
            
            
            elif coin.content == "!취소":
                await message.channel.purge(limit=1)
                
                try:
                    if tank_list.index(coin.author.name) <= 1:
                        tank -= 1
                        tank_list.remove(coin.author.name)
                        all_list.remove(coin.author.id)
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))
                
                except ValueError:
                    pass
                
                try:    
                    if deal_list.index(coin.author.name) <= 5:
                        deal -= 1
                        deal_list.remove(coin.author.name)
                        all_list.remove(coin.author.id)
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))
                
                except ValueError:
                    pass
                
                try:    
                    if heal_list.index(coin.author.name) <= 1:
                        heal -= 1
                        heal_list.remove(coin.author.name)
                        all_list.remove(coin.author.id)
                        await wait.edit(embed=discord.Embed(title = "매칭 대기중", description ='🛡'f"{tank_list}\n⚔{deal_list}\n🍃{heal_list}", color=0x4000FF))                                       
                
                except ValueError:
                    pass
            

                
                
                
                    

            
        
                            
# 매칭
                
        if tank > 1 and deal > 5 and heal > 1:         
            
            Tanker = random.sample(tank_list,2)
            Dealer = random.sample(deal_list,6)
            Healer = random.sample(heal_list,2)
            RedTeam = [Tanker[0]] + Dealer[:3] + [Healer[0]]
            BlueTeam = [Tanker[1]] + Dealer[3:6] + [Healer[1]]

            matchingembed = discord.Embed(title="🔴매칭이 잡혔습니다🔴", description = "이긴 사람 중 아무나 한명이 `!승리`를 입력해주세요.\n 게임을 원하지 않는다면 ❌를 눌러주세요", color=0x4000FF)
            matchingembed.add_field(name= "RED TEAM", value= '🛡'f"{Tanker[0]}\n⚔{Dealer[0]}\n⚔{Dealer[1]}\n⚔{Dealer[2]}\n🍃{Healer[0]}", inline=True)
            matchingembed.add_field(name= "BLUE TEAM", value= '🛡'f"{Tanker[1]}\n⚔{Dealer[3]}\n⚔{Dealer[4]}\n⚔{Dealer[5]}\n🍃{Healer[1]}", inline=True)
            OX = await message.channel.send(embed=matchingembed)
            for ox in ['✅','❌']:
                await OX.add_reaction(ox)

            def confirm(reaction, user):
                return str(reaction) in ['✅','❌'] and user.id in all_list and reaction.message.id == OX.id
# reaction~Ox.id 는 이모지 반응을 해준 메세지의 고유아이디와 OX라는 메세지의 고유 아이디가 일치하는지에 대한거다.
# user = 아이디#3030  //  user.id = 아이디 고유값(숫자)   // 오류가 나면 print()로 확인해보기!          
            reaction, user = await client.wait_for("reaction_add", check=confirm)
                                       
            if str(reaction) == '✅':
                agree = 0
                agree += 1
                if agree == 10: 
                    await OX.clear_reactions()

 # 승리             
                     
                    def join(m):
                        return m.content in ['!승리'] and m.channel == message.channel
                    VIC = await client.wait_for("message", check=join)     
                    
                    if VIC.content == "!승리":
                        for vic in ['✅','❌']:
                            await VIC.add_reaction(vic)
                        
                        def CONFIRM(reaction, user):
                            return str(reaction) in ['✅','❌'] and user.id in all_list and reaction.message.id == VIC.id
                        
                        reaction, user = await client.wait_for("reaction_add", check=CONFIRM)

                        if str(reaction) == '✅':
                            vagree = 0
                            vagree += 1

                            if vagree > 5: 
                                ID = str(VIC.author.name) #name은 닉네임 id는 고유값
                                await VIC.clear_reactions() #이모지 제거
                                
                                if ID in RedTeam:
                                    try:                                       
                                        for j in RedTeam:
                                            df1.loc[df1['ID'] == j , 'MMR'] += 100    
                                        df1.to_csv('mmrlist1.csv', index=False) # csv로 저장   
                                        await message.channel.send("레드팀 "+str(100)+"점 획득!")
                                    
                                    except:
                                        pass
                                
                                elif ID in BlueTeam:
                                    try:      
                                        for z in BlueTeam:    
                                            df1.loc[df1['ID'] == z , 'MMR'] += 100
                                        df1.to_csv('mmrlist1.csv', index=False) 
                                        await message.channel.send("블루팀 "+str(100)+"점 획득!")                                      
                                    
                                    except:
                                        pass      


            elif str(reaction) == '❌':
                await OX.delete()
                await message.channel.send (f"누군가로 인해 매칭이 취소 되었습니다.")


            
            

# 사용법
    if message.content.startswith ("!사용법"): #입력할 메시지
        msgembed = discord.Embed(title="호스팅 하는법", description="!호스트", color=0x4000FF) #큰 제목과 작은 제목을 보여준다
        msgembed.add_field(name="참가하는법", value="!참가 탱커\n!참가 딜러\n!참가 힐러", inline=False)
        msgembed.add_field(name="랭킹 보는법", value="!랭킹", inline=False) #작은 제목과 작은제목의 설명
        msgembed.add_field(name="참가 취소", value="!취소", inline=False)
        msgembed.add_field(name="이겼을 시", value="!승리", inline=False)
        await message.channel.send(embed=msgembed)
        


# 청소
    if message.content.startswith ("!청소"):
        i = (message.author.guild_permissions.administrator)

        if i is True:
            amount = message.content[4:]
            await message.channel.purge(limit=1)
            await message.channel.purge(limit=int(amount))

        if i is False:
            await message.channel.purge(limit=1)
            await message.channel.send("{}, 당신은 명령어를 사용할 수 있는 권한이 없습니다".format(message.author.mention))

# 점수 확인

    if message.content == "!점수":
        ID = str(message.author.name)
        find_row = df1[df1['ID']==ID]
        await message.channel.send(find_row.to_string(index=False)+"점") #index값을 제거
    
    
# 랭킹
    if message.content == "!랭킹":
            MMR_list = df1.sort_values(by=['MMR'], ascending = False)
            embed = discord.Embed(title="랭킹", description=f"{MMR_list[1:11].to_string(index=False)}", color=0x4000FF) #큰 제목과 작은 제목을 보여준다
            await message.channel.send(embed=embed)
    
    
client.run("OTc5NjkxNjM4NzY5MjAxMTYy.G5ONKI.uq6wNW_cad4Wvt5cKFS1y4SqeBV08zPD0nGHVs") # 토큰 적는곳

자바,파이썬