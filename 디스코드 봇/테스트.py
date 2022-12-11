from re import A
import discord
import asyncio
import random

from discord.utils import get


client = discord.Client()

id, mmr = [], []

try:
    f = open('mmrlist.txt', 'r')
except:
    f = open('mmrlist.txt', 'w')
    f.close()
    f = open('mmrlist.txt', 'r')
for line in f.readlines():
    data = line.split(",")
    id.append(data[0])
    mmr.append(int(data[1]))
f.close

@client.event
async def on_ready():

    print(client.user.name)
    print('성공적으로 봇이 시작되었습니다')
    game = discord.Game('헤으응') # ~~ 하는중
    await client.change_presence(status=discord.Status.online, activity=game)


       
@client.event
async def on_message(message):
    if message.content == "!해윙": # 내가 '해윙'이라고 말하면
        await message.channel.send (f"헤으응") # 봇이 '안녕하세요'라고 대답
    if message.content == "!꼼시":
        await message.channel.send (f"우리 주인님")
    if message.content == "!사용법": #입력할 메시지
        embed = discord.Embed(title="참가하는법", description="!참가 탱커\n!참가 딜러\n!참가 힐러", color=0x4000FF) #큰 제목과 작은 제목을 보여준다
        embed.add_field(name="랭킹 보는법", value="!랭킹", inline=False) #작은 제목과 작은제목의 설명
        embed.add_field(name="참가 취소", value="!취소", inline=False)
        embed.add_field(name="이겼을 시", value="!승리", inline=False)
        await message.channel.send(embed=embed)        
#테스트용
    if message.content == "!테스트":

        bot = ['1','2','3','4','5','6','7','8','9','10']
        GG = ['GGomsi'] #테스트용 추가
        tank_list = random.sample(bot,2)
        deal_list = random.sample(bot,6)
        heal_list = random.sample(bot,2)
        RedTeam = [tank_list[0]] + deal_list[:3] + [heal_list[0]] + GG
        BlueTeam = [tank_list[1]] + deal_list[3:6] + [heal_list[1]]
        matchingembed = discord.Embed(title="🔴매칭이 잡혔습니다🔴", description = "이긴 사람 중 아무나 한명이 `!승리`를 입력해주세요.\n 게임을 원하지 않는다면 ❌를 눌러주세요", color=0x4000FF)
        matchingembed.add_field(name= "RED TEAM", value= '🛡'f"{tank_list[0]}\n⚔{deal_list[0]}\n⚔{deal_list[1]}\n⚔{deal_list[2]}\n🍃{heal_list[0]}", inline=True)
        matchingembed.add_field(name= "BLUE TEAM", value= '🛡'f"{tank_list[1]}\n⚔{deal_list[3]}\n⚔{deal_list[4]}\n⚔{deal_list[5]}\n🍃{heal_list[1]}", inline=True)
        OX = await message.channel.send(embed=matchingembed)
        for ox in ['✅','❌']:
            await OX.add_reaction(ox)

        def confirm(reaction, user):
                return str(reaction) in ['✅','❌'] and user == message.author and reaction.message.id == OX.id
                
        reaction, user = await client.wait_for("reaction_add", check=confirm)
                                  
        if str(reaction) == '✅':            
            agree = 0
            agree += 1
            if agree == 1:
                await OX.clear_reactions()
                def join(m):
                    return m.content in ['!승리'] and m.channel == message.channel
                VIC = await client.wait_for("message", check=join)

                if VIC.content == "!승리":
                    for vic in ['✅','❌']:
                        await VIC.add_reaction(vic)
                            
                    def CONFIRM(reaction, user):
                        return str(reaction) in ['✅','❌'] and user == message.author and reaction.message.id == VIC.id
                                
                    reaction, user = await client.wait_for("reaction_add", check=CONFIRM)

                    if str(reaction) == '✅':
                        vagree = 0
                        vagree += 1
                        if vagree == 1:
                            ID = str(VIC.author.name) #name은 닉네임 id는 고유값
                            await VIC.clear_reactions() #이모지 제거

                            if ID in RedTeam:
                                try:

                                    for j in RedTeam:
                                        mmr[id.index(j)] += 50
                                    await message.channel.send("레드팀 "+str(50)+"점 획득!")
                                except:
                                    pass
                            
                            elif ID in BlueTeam:
                                try:

                                    for z in BlueTeam:
                                        mmr[id.index(z)] += 50
                                    await message.channel.send("블루팀 "+str(50)+"점 획득!")
                                except:
                                    pass


                            
                            
                            # elif not ID in id:
                                # id.append(ID)
                               # mmr.append(0)

                            
                            
                            f = open("mmrlist.txt", "w") #저장
                            for p in range(0,len(id),1):
                                f.write(str(id[p])+","+str(mmr[p])+"\n")
                            f.close()

        
        
        elif str(reaction) == '❌':
                await OX.delete()
                await message.channel.send (f"누군가로 인해 매칭이 취소 되었습니다.")                

    if message.content == "!점수":
        ID = str(message.author.name)
        if ID in id:
            await message.channel.send(str(mmr[id.index(ID)])+"점")
        
        elif not ID in id:
            await message.channel.send("없어")
            raise ValueError




# 승리                
                
            
        
                
       

 # 승리                   
    
        



client.run("OTc5NjkxNjM4NzY5MjAxMTYy.G5ONKI.uq6wNW_cad4Wvt5cKFS1y4SqeBV08zPD0nGHVs") # 토큰 적는곳