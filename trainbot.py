import discord
import asyncio
from cmds import incrementStats, editPlayer, dumpStats

# file name for the database
CMD_PREFIX = '!'
STATS_FILE = 'stats.csv'

              # Reichspräsident     # Reichsprotektor
CMD_ROLES = ['319225958492012545', '319626374241320973']
               # Members
STAT_ROLES = ['131586834642894849']

choochooUsage = '!choochoo win [winner] lose [loser1 loser2 etc]'
addplayerUsage = '!addplayer [player]'
removeplayerUsage = '!removeplayer [player]'
setplayerUsage = '!setplayer name [name] wins [win_count] losses [loss_count]'
statsUsage = '!stats <winrate | wins | losses>'
helpMsg = ('```diff\n'
           'These are the available commands. Arguments displayed in [square brackets]\n'
           'are required. Arguments displayed in <angle brackets> are optional.\n'
           '----------------------------------------------------------------------------\n'
           + choochooUsage + '\n'
           + addplayerUsage + '\n'
           + removeplayerUsage + '\n'
           + setplayerUsage + '\n'
           + statsUsage + '\n'
           '```')

client = discord.Client()

# desc: function to check permissions for a command
# args: member - the member to check permissions for. must be of type Member
#       roleList - a list of approved roles
# retn: 1 if member has an allowed role, 0 otherwise
def checkPermission(member, roleList):
    # check command permissions
    for role in member.roles:
        if role.id in roleList:
            return 1
    return 0


@client.event
async def on_ready():
    print('Logged in as \"%s\" with ID %s' % (client.user.name, client.user.id))
    print('Connected servers:')
    for server in client.servers:
        print('\t%s (%s)' % (server.name, server.id))

        #print('\tRoles:')
        #for role in server.role_hierarchy:
        #    print('\t\t%s (%s)' % (role.name, role.id))

        #print('\tMembers:')
        #for member in server.members:
        #    print('\t\t%s (%s)' % (member.name, member.id))
    print('---------------------------------------------')

@client.event
async def on_message(message):
    # check if this is a command for this bot
    if message.content.startswith(CMD_PREFIX):
        # get the arguments in the message
        args = message.content.split()
        # get the command after the command prefix
        command = args[0][1:]
        # remove the command from the args
        del(args[0])
        print('\n[INFO] Command: %s' % command)
        print('[INFO] Arguments: %s' % args)

        # get invoking member
        msgAuthor = message.author

        # main command for adding win and lose information
        # syntax: !choochoo win [winner] lose [loser1 loser2]
        if command == 'choochoo':
            # check command permissions
            if checkPermission(msgAuthor, CMD_ROLES):
                # check if the number of arguments is valid
                if len(args) < 4:
                    print('[ERROR] Invalid argument list')
                    await client.send_message(message.channel, 'Error: Invalid number of arguments')
                    winnerFound = 0
                    losersFound = 0
                else:
                    # convert all arguments to UPPERCASE
                    for i in range(0, len(args)):
                        args[i] = args[i].upper()

                    # get winner
                    try:
                        winIndex = args.index('WIN')
                        winner = args[winIndex + 1]
                        winnerFound = 1
                    except ValueError:
                        print('[ERROR] No winner specified')
                        await client.send_message(message.channel, 'Error: No winner specified')
                        winnerFound = 0

                    # get losers
                    try:
                        loseIndex = args.index('LOSE')
                        if loseIndex > winIndex:
                            # losers were stated after the winner
                            losers = args[loseIndex + 1 :]
                        else:
                            # losers were stated before the winner
                            losers = args[loseIndex + 1 : winIndex]
                        losersFound = 1
                    except ValueError:
                        print('[ERROR] No losers specified')
                        await client.send_message(message.channel, 'Error: No losers specified')
                        losersFound = 0

                # if we got a winner and losers then update stats
                if winnerFound and losersFound:
                    # change case to capitalized
                    winner = winner.capitalize()
                    for i in range(0, len(losers)):
                        losers[i] = losers[i].capitalize()

                    print('[INFO] Winner: %s' % winner)
                    print('[INFO] Losers: %s' % losers)

                    # try updating the stats
                    status = incrementStats(message.channel, STATS_FILE, winner, losers)
                    await client.send_message(message.channel, status)

                await client.send_message(message.channel, '<:trains:324019973607653378>')
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'addplayer':
            # check command permissions
            if checkPermission(msgAuthor, CMD_ROLES):
                # check for valid number of arguments
                if len(args) < 1:
                    print('[ERROR] Invalid argument list')
                    await client.send_message(message.channel, 'Error: Invalid number of arguments')
                else:
                    # get name to add to database
                    playerName = args[0].capitalize()
                    status = editPlayer(message.channel, STATS_FILE, playerName, editType='ADD')
                    await client.send_message(message.channel, status)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'removeplayer':
            # check command permissions
            if checkPermission(msgAuthor, CMD_ROLES):
                # check for valid number of arguments
                if len(args) < 1:
                    print('[ERROR] Invalid argument list')
                    await client.send_message(message.channel, 'Error: Invalid number of arguments')
                else:
                    # get name to remove from database
                    playerName = args[0].capitalize()
                    status = editPlayer(message.channel, STATS_FILE, playerName, editType='REMOVE')
                    await client.send_message(message.channel, status)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'setplayer':
            # check command permissions
            if checkPermission(msgAuthor, CMD_ROLES):
                if len(args) < 6:
                    print('[ERROR] Invalid argument list')
                    await client.send_message(message.channel, 'Error: Invalid number of arguments')
                else:
                    # convert all arguments to UPPERCASE
                    for i in range(0, len(args)):
                        args[i] = args[i].upper()

                    #get player name
                    try:
                        playerIndex = args.index('NAME')
                        playerName = args[playerIndex + 1]
                        playerName = playerName.capitalize()
                        playerFound = 1
                    except ValueError:
                        print('[ERROR] No player specified')
                        await client.send_message(message.channel, 'Error: No player specified')
                        playerFound = 0

                    # get number of wins
                    try:
                        winIndex = args.index('WINS')
                        winCount = str(args[winIndex + 1])
                        winsFound = 1
                    except ValueError:
                        print('[ERROR] No win count specified')
                        await client.send_message(message.channel, 'Error: No win count specified')
                        winsFound = 0

                    # get number of losses
                    try:
                        loseIndex = args.index('LOSSES')
                        lossCount = str(args[loseIndex + 1])
                        lossFound = 1
                    except ValueError:
                        print('[ERROR] No loss count specified')
                        await client.send_message(message.channel, 'Error: No loss count specified')
                        lossFound = 0

                    if playerFound and winsFound and lossFound:
                        status = editPlayer(message.channel, STATS_FILE, playerName, editType='EDIT', wins=winCount, losses=lossCount)
                        await client.send_message(message.channel, status)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'stats':
            # check permissions
            if checkPermission(msgAuthor, CMD_ROLES) or checkPermission(msgAuthor, STAT_ROLES):
                if len(args) > 0:
                    sortType = args[0].upper()
                    statsMsg = dumpStats(message.channel, STATS_FILE, sortType=sortType)
                    await client.send_message(message.channel, statsMsg)
                else:
                    statsMsg = dumpStats(message.channel, STATS_FILE)
                    await client.send_message(message.channel, statsMsg)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'trainshelp':
            # send the help message
            await client.send_message(message.channel, helpMsg)

client.run('bot token')
# https://discordapp.com/oauth2/authorize?client_id=bot_id&scope=bot&permissions=0
