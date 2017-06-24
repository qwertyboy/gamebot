import discord
import asyncio
from cmds import incrementStats, editPlayer, dumpStats
from config import Config

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

# create a client
client = discord.Client()
# get the config information
config = Config()
for group in config.groups:
    print(group.name)
    print('\t' + str(group.cmds))
    print('\t' + str(group.roles))
    print('\t' + str(group.users))


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
    # check if we should process messages for this channel
    msgChannel = message.channel.id
    if msgChannel == config.listenID or config.listenID == 'NONE':

        # check if this is a command for this bot
        if message.content.startswith(config.cmdPrefix):
            # get the arguments in the message
            args = message.content.split()
            # get the command after the command prefix
            command = args[0][1:].upper()
            # remove the command from the args
            del(args[0])
            print('\n[INFO] Command: %s' % command)
            print('[INFO] Arguments: %s' % args)

            # get invoking member
            msgAuthor = message.author
            # check permission for command
            permission = config.checkPermission(msgAuthor, command)

            if permission:
                # main command for adding win and lose information
                # syntax: !choochoo win [winner] lose [loser1 loser2]
                if command == 'CHOOCHOO':
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
                        status = incrementStats(message.channel, config.statsFileName, winner, losers)
                        await client.send_message(message.channel, status)

                    await client.send_message(message.channel, '<:trains:324019973607653378>')

                elif command == 'ADDPLAYER':
                    # check for valid number of arguments
                    if len(args) < 1:
                        print('[ERROR] Invalid argument list')
                        await client.send_message(message.channel, 'Error: Invalid number of arguments')
                    else:
                        # get name to add to database
                        playerName = args[0].capitalize()
                        status = editPlayer(message.channel, config.statsFileName, playerName, editType='ADD')
                        await client.send_message(message.channel, status)

                elif command == 'REMOVEPLAYER':
                    # check for valid number of arguments
                    if len(args) < 1:
                        print('[ERROR] Invalid argument list')
                        await client.send_message(message.channel, 'Error: Invalid number of arguments')
                    else:
                        # get name to remove from database
                        playerName = args[0].capitalize()
                        status = editPlayer(message.channel, config.statsFileName, playerName, editType='REMOVE')
                        await client.send_message(message.channel, status)

                elif command == 'SETPLAYER':
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
                            status = editPlayer(message.channel, config.statsFileName, playerName, editType='EDIT', wins=winCount, losses=lossCount)
                            await client.send_message(message.channel, status)

                elif command == 'STATS':
                    if len(args) > 0:
                        sortType = args[0].upper()
                        statsMsg = dumpStats(message.channel, config.statsFileName, sortType=sortType)
                        await client.send_message(message.channel, statsMsg)
                    else:
                        statsMsg = dumpStats(message.channel, config.statsFileName)
                        await client.send_message(message.channel, statsMsg)

                elif command == 'TRAINSHELP':
                    # send the help message
                    await client.send_message(message.channel, helpMsg)

            # failed permission check
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

client.run(config.botToken)
# https://discordapp.com/oauth2/authorize?client_id=bot_id&scope=bot&permissions=0
