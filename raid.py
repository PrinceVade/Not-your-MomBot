# Hunter Graves
# 09/11/2020
# raid.py

# 

import random
import discord
from discord.ext import commands

#
def nextBoss(cBoss, guild):
    

#
def readInfo(header):
    
#
def leaderboard(cboss, raw):

#
def rawLeaderboard(cBoss):
    contents = open("raid/bosses/" + cBoss + ".boss", "r").readlines()[3:]
    return {i.split(":")[0]: i.split(":")[1] for i in contents}
    
#
def giveEXP(cBoss, boardDict, channel):
    # gather the information on the boss
    bossContents = open("raid/bosses/" + cboss + ".boss", "r").readlines()
    bossHP = bossContents[1].strip()
    bossXP = bossContents[2].strip()
    
    for p in boardDict.keys():
        pDamage = boardDict[p]
    
        with open("users/" + str(p) + ".user", "w+") as pFile:
            pContents = pFile.readlines()
            pXP = pContents[2]
            
            xpPerc = bossXP / pDamage
            xpACT = round(xpPerc * pXP)
            
            pXP += xpACT

# defeats the current boss, prints defeat text and the leaderboard, distributes xp
# and loads the next boss
def killBoss(cBoss, guild):
    # first, grab the appropriate channel from guild
    cat = ([c for c in guild.categories if c.name == "Future Overlords"])[0]
    channel = ([t for t in cat.text_channels if t.name == "General"])[0]
    
    # grab the kill message and leaderboard text
    killText = readInfo("kill")
    rawBoardText = rawLeaderboard(cBoss)
    board = leaderboard(cBoss, raw)
    
    # print them both out
    await channel.send(content=killText)
    await channel.send(content="Leaders of the Fight!\n" + board)
    
    # distribute the experience points
    giveEXP(cBoss, rawBoardText, channel)
    
    # load up the next boss
    nextBoss(cBoss, guild)

# decrements the current bosses health per the user's level
def damageBoss(user, bHP, cBoss):
    
    # these are placeholders in case the file doesn't exist
    name = user.name
    level = 1
    xp = 0
    total = 0
    
    # attempt to open the user file, set a boolean
    userExists = True
    try:
        uFile = open("raid/users/" + str(user.id) + ".user")
    except IOError:
        # file didn't exist (or other issues)
        userExists = False

    # get the user's file and add the new damage done
    with open("raid/users/" + str(user.id) + ".user", "w+") as file:
        # get these so that we can add them back to the file later
        if userExists:
            name = file.readline().strip()
            level = int(file.readline().strip())
            xp = file.readline().strip()
            total = int(file.readline().strip())
        
        # damage the boss, increment the level
        if (level >= bHP):
                total += bHP
                bHP = 0
        else:
            bHP -= level
            total += level
        
        # write all the data back to the user file
        file.write("\n".join([name, str(level), str(xp), str(total)]))
    
    # get the boss's file and add/increment to the leaderboard
    with open("raid/bosses/" + cBoss + ".boss", "w+") as bFile:
        # grab the boss's information just in case we need to call their insurance provider
        bossName = bFile.readline().strip()
        bossHP = bFile.readline().strip()
        bossXP = bFile.readline().strip()
        
        # a complicated list of lines -> dictionary transition
        # bFile.readlines() -> list of lines ... ["test1:t1", "test2:t2", "test3:t3",...]
        # i -> "test1:t1"
        # i.split(":") -> ["test1", "t1"]
        userDict = {i.split(":")[0]: i.split(":")[1] for i in bFile.readlines()}
        
        if (userDict):
            userDict[str(user.name)] += level
        else:
            userDict[str(user.name)] = level
        
        # recompile the dictionary into a list and write it back to the file
        bossUsers = [":".join([k,str(v)]) for (k,v) in list(userDict.items())]
        bFile.writelines("\n".join([bossName, bossHP, bossXP] + bossUsers))
    
    # only return the new HP since this does all the file handling
    return bHP
    
# returns True if the msg is valid for user to react to.
# parameters:
#   Message: 'msg' the Message that the user reacted to
#   int: 'user' the user ID who reacted to msg
#   dict: 'chars' the dictionary of characters to replace (keys) with what to replace them with (values)
def checkMessage(msg, user, chars):
    print("\nhelper.raid.checkMessage: start")
    
    # determine if the msg content contains the correct character(s)
    charsInMsg = [c for c in chars.values() if (c in msg.content)]
    if not (charsInMsg) : return False
    
    print("helper.raid.checkMessage: found chars = " + str(charsInMsg))
    
    # open the file named by the message id
    with open("raid/msgs/" + str(msg.id) + ".msg", "w+") as file:
        lines = file.readlines()
        
        # check the content for the user's id
        # return if it's there, add it if it isn't.
        if (str(user) in lines) : return False
        else : file.write(str(user))
    
    print("helper.raid.checkMessage: this msg is valid.")
    return True

# has a 5% chance to replace one of RAID_CHARS.keys with respective RAID_CHARS.values
# returns the original string 95% of the time
# parameters:
#   String: 'message' the string to replace characters (5% chance)
def generateMessage(message):
    print("\nhelper.raidGenerateMessage: start")
    newMessage = message
    
    # store and print this to the console for debug
    randNum = random.randint(1,100)
    print("helper.raidGenerateMessage: randNum = " + str(randNum))
    
    # check for a 5% chance to change the message.
    if (randNum in [1, 14, 47, 69, 91]):
        
        # create a sublist of RAID_CHARS.keys that are in the message and check if it's empty
        # if it is, return.
        options = [c for c in RAID_CHARS.keys() if (c in newMessage)]
        if not options: return message
        
        # get a random character from possible characters
        randChar = random.choice(options)
        
        # throw a debug message and replace the character(s)
        print("helper.raidGenerateMessage: randChar = " + randChar)
        newMessage = newMessage.replace(randChar, RAID_CHARS[randChar])
    
    return newMessage