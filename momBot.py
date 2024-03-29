# Hunter Graves
# 13/10/2020
# momBot.py

# This program is a bot for Discord that does some random tasks (requested by my discord-ians)
# It responds to the user posting, unless producing an update message.
# Update messages print to a generated channel (#general) within a category ("Future Overlords")

import discord
from discord.ext import commands,tasks

import random
import epicScrape
from datetime import datetime
from pathlib import Path

# The token and description of the bot.
TOKEN = ''
description = '''I am not your Mom-Bot. I will, however, perform tasks such as one would.
Use the ? to prefix all requests.
Please refer to your system administrator for additional functionality.
You are all pieces of fecal matter.'''

# defining the bot's command prefix as well as adding the description.
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=('?', 'Janet? '), description=description)
RAID_CHARS = {"a" : "\u03B1","b" : "\u03B2","c" : "\u03C2","e" : "\u03B5","f" : "\u03DD","g" : "\u03D1","i" : "\u03CA","l" : "\u0399","m" : "\u03FB","n" : "\u03B7","o" : "\u03B8","p" : "\u03C1","s" : "\u03E9","u" : "\u03BC","w" : "\u03C9","z" : "\u03DF","T" : "\u0372"}

# ----------Commands----------
# print the contents of the file "changelog.txt."
@bot.command(   name = 'changelog'
                ,brief = ' Prints the changelog.'
                ,description = 'Prints the most recently completed changelog file. May not include "beta" updates/fixes.')
async def changelog(ctx):
    changelogPath = Path(__file__).with_name('changelog.txt')

    with changelogPath.open('r') as file:
        log = file.readlines()
    
    await ctx.send("```" + "".join(log) + "```")

# ALL HAIL THE MAGIC CONCH
@bot.command(   name = 'magicconch'
                ,brief = ' The all-knowing magic conch.'
                ,description = 'The magic conch: a fortune telling and all-knowing device that has elevated past the original reference.'
                ,aliases = ["conch", "theconch", "mc"]
                ,pass_ctx = True)
async def conch(ctx):
    responses = [
    "Yes",
    "No",
    "Try asking again",
    "Maybe someday",
    "Absolutely",
    "No (sassy)"]

    # add a commma and mention the author here, prepend later
    outMessage = ", " + ctx.message.author.mention

    # decided what repsonse to prepend
    if "what" in ctx.message.content:
        outMessage = "Nothing" + outMessage
    elif "another beer" in ctx.message.content:
        outMessage = "Only if you have a set of balls" + outMessage
    else:
        outMessage = random.choice(responses) + outMessage

    # printing the output
    await ctx.send((outMessage))

# accepts XdY fromat as input.
# outputs X random numbers, all between 1 and Y.
# both X and Y have a limit of 100
@bot.command(   name = 'roll'
                ,brief = ' Rolls a dice in NdN format.'
                ,description='Rolls a dice in NdN format. For those times when nobody wants to make a decision.'
                ,aliases =['r'])
async def roll(ctx, dice: str = commands.parameter(description='String of XdY format. Rolls a Y-sided dice X number of times. 100 Max for both values.')):
    """Rolls a dice in NdN format."""
    print("command.roll: Start")
    try:
        print("command.roll: inside try block")
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        print("command.roll: exception called")
        await ctx.send('Format has to be in NdN!')
        return

    print("command.roll: outside try")
    # Limit this shit so moron's don't rule the server
    if (rolls > 100 or limit > 100):
        await ctx.send('The limit is 100 for either parameter.')
        print("command.roll: limits exceeded.\n")
    else:
        print("command.roll: within limits. Result inbound.\n")
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

@bot.command(   name = 'fuck'
                ,brief = " I can't believe you've done this."
                ,description = 'Generates a funny maymay phrase.'
                ,aliases = ['f'])
async def fuck(ctx):
    await ctx.send("I can't believe you've done this.")

# the lynch command prints a funny statement and counts the number of people lynched.
@bot.group(     name = 'lynch'
                ,brief = ' Hang criminals from the gallows.'
                ,description = 'Lynch literally anyone or anything with a funny, predetermined phrase.'
                ,aliases = ['Lynch', 'hang', 'l']
                ,pass_ctx = True
                ,invoke_without_command = True)
async def lynch(ctx, *args):

      if ctx.invoked_subcommand is None:
            responses = [
            "'s neck snaps as the rope draws tight.",
            " falls as the floor opens beneath them, with a loud crack sounding through the air.",
            "'s rope isn't long enough after they drop, and they stop squriming after some minutes.",
            " jerks and swings as the rope draws tight.",
			" drops and breaks their neck with a crack.",
			" slips before the floor opens, writhing about as they suffocate.",
			" discovers that their kink is asphyxiation and blood rushes to their weiner as they perish with an erection.",
			"'s executioner calls an audible and allows the town to stone them to death. Savegery.",
			" swings from the gallows.",
			" jerks as the rope snaps their neck, and all falls silent except the creaking wood.",
			"'s luck has run out, and Will Turner doesn't show up to save them."]
            
            lynchPath = Path(__file__).with_name('lynch.txt')
            with lynchPath.open("r") as file:
                  count = str(int(file.readline()) + 1)
                  names = file.readlines()

            modArgs = []
            menCount = 0
            if len(ctx.message.mentions) > 0:
                  for a in args:
                        if '<' not in a:
                              modArgs += a
                        else:
                              if ctx.message.mentions[menCount].nick is None:
                                    modArgs += [ctx.message.mentions[menCount].name]
                              else:
                                    modArgs += [ctx.message.mentions[menCount].nick]
                              menCount += 1
            else:
                  modArgs = args
            
            with lynchPath.open("w") as newF:
                  newF.write(count  + "\n" + "".join(names) + " ".join(modArgs) + "\n")
            
            await ctx.send(("".join(modArgs) + random.choice(responses)))
            await ctx.send((count + " people have been hanged from the gallows."))

@lynch.command( name = 'memorial'
                ,brief = ' Shows the memorial of the fallen.'
                ,description = 'Displays the number and the plaintext names of those who were lynched across time.')
async def memorial(ctx):
    lynchPath = Path(__file__).with_name('lynch.txt')
    with lynchPath.open("r") as file:
        file.readline()
        names = file.readlines()

    await ctx.send("A moment of silence, for all those that are the die.")
    await ctx.send("```" + "".join(names) + "```")

# this command manages roles that people could want/remove whenever they please
@bot.command(   name = 'role'
                ,brief = ' Adds or Removes a role from the user.'
                ,description = 'Add/Remove roles made for notification purposes. Does not work for all roles.')
async def role(ctx, action: str = commands.parameter(description='The action to perform. "Add" or "Remove" are the only accepted values.'), roleRequested: str = commands.parameter(description='Case sensitive name of role to perform the action on.')):
    # search the current guild's roles for something that matches what was roleRequested.
    roletodo = discord.utils.find(lambda x: x.name == roleRequested, ctx.guild.roles)
    member = ctx.message.author
    memberHasRoles = list(map(lambda x: x.name, member.roles))
    
    # logging statement for the window
    print('role: ' + action + ' ' + 'roleRequested for ' + roleRequested + '\n by ' + member.name + '\n Role List: [\n' + '\n,'.join(memberHasRoles))
    
    try:
        print('role: role exists as: ' + roleRequested)
    
        # add the role if its not already there
        if (action.lower() == 'add'):
            await member.add_roles(roletodo)
            await ctx.send('Successfully added ' + roleRequested + ' to your roles!')
        # remove it if it ain't
        elif (action.lower() == 'remove'):
            await member.remove_roles(roletodo)
            await ctx.send('Successfully removed ' + roleRequested + ' from your roles!')
    except Exception as e:
        await ctx.send('Something went wrong. Please contact the admin:\n`' + str(e) + '`')

@bot.command(   name = 'reEpic'
                ,brief = ' Runs the Epic Tasks.'
                ,description='A command to re-print an epic message. Simulates a message based on the given day. Sends the message in the channel the command was called in.')
async def reEpic(ctx, day: str = commands.parameter(default='Thursday', description='The day to emulate.')):       
    await printEpic((day in ['Thursday', 'Thurs', 'Th', '5']), ctx)

# epic() loops every hour, until Thursday, 11a (EST)
# prints games retrieved from epicgames.com that are free
# output goes to all guilds the bot is on, in the first channel
# or role with 'epic' in the name.
@tasks.loop(hours=1)
async def epic():
    isThursday = (datetime.now().weekday() == 3)
    
    if (isThursday or (datetime.now().weekday() == 1)) and (datetime.now().hour == 16):
        await printEpic(isThursday)

async def printEpic(isThursday, ctx=''):
    thisWeek = epicScrape.scrape()
    
    #loop through guilds the bot is apart of, find the proper channel/role to drop into.
    for g in bot.guilds:
        channel = [c for c in g.channels if 'epic' in c.name.lower()][0]
        role = [r for r in g.roles if 'epic' in r.name.lower()][0]

        if (ctx):
            channel = ctx.channel
        
        try:
            #this is set for Thursday, 11a
            if isThursday:

                adjustedTime = str(int(datetime.fromisoformat(thisWeek[0]['endDate'][:-1] + '+00:00').timestamp()))
                await channel.send('***FREE NOW - <t:' + adjustedTime + ':f> ***\n' + role.mention)
                for t in thisWeek:
                    embed = discord.Embed(title=t['title']
                        , url=t['url']
                        , description=t['desc']
                        , color=0x2E8b57)
                    embed.set_image(url=t['image'])

                    await channel.send(embed=embed)
                    print('epic.loop: Thursday: sent msg to ' + g.name + ' channel: ' + channel.name)
            else:
                await channel.send('Don\'t forget to grab the above game(s) while they last!\n' + role.mention)
                print('epic.loop: !Thursday: sent reminder to '  + g.name + ' channel: ' + channel.name)
        except Exception:
            print('Error during epic loop. Exception: ' + repr(Exception) + '\nData from scrape: \n' + ''.join(thisWeek))

# ----------Events----------

@bot.event
async def on_ready():
    # print out some debug stuff
    print("event.on_ready: bot is all ready to go.")
    
    # go ahead and start the epic task loop
    epic.start()

@bot.event
async def on_guild_join(guild):
    print("on_guild_join: start")
    
    #Check to see if the Future Overlords category exists
    if ("Future Overlords" not in [c.name for c in guild.categories]):
        print("on_guild_join: Future Overlords does not exist.")
    
        #Create the category
        cat = await guild.create_category("Future Overlords")
    else:
        print("on_guild_join: Future Overlords does exist.")
    
        #it already exists, just declare 'cat' as the category channel
        cat = ([c for c in guild.categories if c.name == "Future Overlords"])[0]

    # check to make sure general isn't already in there.
    #  if it isn't, go ahead and make it
    print("on_guild_join: check for general category.\n")
    if ("general" not in [t.name for t in cat.text_channels]):
    
        print("on_guild_join: general does not exist within Future Overlords.\n")
        channel = await guild.create_text_channel("general", category=cat)

# ----------End----------

bot.run(TOKEN)