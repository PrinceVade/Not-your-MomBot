# Hunter Graves
# 13/10/2020
# momBot.py

# This program is a bot for Discord that does some random tasks (requested by my discord-ians)
# It responds to the user posting, unless producing an update message.
# Update messages print to a generated channel (#general) within a category ("Future Overlords")

import discord
from discord.ext import commands,tasks

import random
from datetime import datetime
import epicPrint

# The token and description of the bot.
TOKEN = ''
description = '''I am not your Mom-Bot. I will, however, perform tasks such as one would.
Please refer to your system administrator for additional functionality.
You are all pieces of fecal matter.'''

# defining the bot's command prefix as well as adding the description.
bot = commands.Bot(command_prefix='!', description=description)
RAID_CHARS = {"a" : "\u03B1","b" : "\u03B2","c" : "\u03C2","e" : "\u03B5","f" : "\u03DD","g" : "\u03D1","i" : "\u03CA","l" : "\u0399","m" : "\u03FB","n" : "\u03B7","o" : "\u03B8","p" : "\u03C1","s" : "\u03E9","u" : "\u03BC","w" : "\u03C9","z" : "\u03DF","T" : "\u0372"}

# ----------Commands----------
# print the contents of the file "changelog.txt."
@bot.command(name="changelog",
    description="Prints the most recent completed changelog file")
async def changelog(ctx):
    
    with open ("changelog.txt", "r") as file:
        log = file.readlines()
    
    await ctx.send("```" + "".join(log) + "```")

# ALL HAIL THE MAGIC CONCH
@bot.command(name = 'magicconch',
    description = 'The all-knowing magic conch',
    aliases = ["conch", "theconch", "mc"],
    pass_ctx = True)
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
@bot.command(description='Rolls a dice in NdN format. For those times when nobody wants to make a decision.',
    aliases =['r'])
async def roll(ctx, dice: str):
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

@bot.command(description="I can't believe you've done this.",
    aliases = ['f'])
async def fuck(ctx):
    await ctx.send(raidGenerateMessage("I can't believe you've done this."))

# the lynch command prints a funny statement and counts the number of people lynched.
@bot.group(aliases = ['Lynch', 'hang', 'l'],
                pass_ctx = True,
                invoke_without_command = True)
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
            
            with open("lynch.txt", "r") as file:
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
            
            with open("lynch.txt", "w") as newF:
                  newF.write(count  + "\n" + "".join(names) + " ".join(modArgs) + "\n")
            
            await ctx.send((" ".join(modArgs) + random.choice(responses)))
            await ctx.send((count + " people have been hanged from the gallows."))

@lynch.command(name = 'memorial')
async def memorial(ctx):
      with open ("lynch.txt", "r") as file:
            file.readline()
            names = file.readlines()

      await ctx.send("A moment of silence, for all those that are the die.")
      await ctx.send("```" + "".join(names) + "```")

# this command manages roles that people could want/remove whenever they please
@bot.command(description='Add/Remove roles made for notification purposes.')
async def role(ctx, todo: str, request: str):
    # search the current guild's roles for something that matches what was requested.
    roleToDo = discord.utils.find(lambda x: x.name == request, ctx.guild.roles)
    member = ctx.message.author
    memberHasRoles = list(map(lambda x: x.name, member.roles))
    
    # logging statement for the window
    print('role: ' + todo + ' ' + 'requested for ' + request + '\n by ' + member.name + '\n Role List: [\n' + '\n,'.join(memberHasRoles))
    
    # if that role exists in this guild
    try:
        print('role: role exists as: ' + request)
    
        # add the role if its not already there
        if (todo.lower() == 'add'):
            await member.add_roles(roleToDo)
            await ctx.send('Successfully added ' + request + ' to your roles!')
        # remove it if it ain't
        elif (todo.lower() == 'remove'):
            await member.remove_roles(roleToDo)
            await ctx.send('Successfully removed ' + request + ' from your roles!')
    except Exception as e:
        await ctx.send('Something went wrong. Please contact the admin:\n`' + str(e) + '`')

# this command runs on a loop, and double checks the time/day of the week. The minute doesnt really matter
@tasks.loop(hours=1)
async def epic():
    if (datetime.now().weekday() == 3) and (datetime.now().hour == 11):
        thisWeek = epicPrint.scrape()
        
        for g in thisWeek:
            embed = discord.Embed(title=g[1]
                , url=g[2]
                , description=g[3]
                , color=0x8e43b6)
            embed.set_image(url=g[0])
        
        
            channel = bot.get_channel(733722340193599598)
            await channel.send('*** THIS WEEK ***', embed=embed)

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