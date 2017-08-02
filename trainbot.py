import discord
import asyncio
from cmds import incrementStats, editPlayer, dumpStats, helpMessage
from config import Config
from db import createDB
from cmdparser import ParseMessage

choochooUsage = '!choochoo win [winner] lose [loser1 loser2 etc]'
addplayerUsage = '!addplayer [player]'
removeplayerUsage = '!removeplayer [player]'
setplayerUsage = '!setplayer name [name] wins [win_count] losses [loss_count]'
statsUsage = '!stats <winrate | wins | losses>'


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
            # parse the command
            cmd = ParseMessage(message)
            gameFileName = cmd.game + '_' + config.statsFileName

            print('\n[INFO] Command: %s' % cmd.command)
            print('[INFO] Arguments: %s' % cmd.args)

            # get invoking member
            msgAuthor = message.author
            # check permission for command
            permission = config.checkPermission(msgAuthor, cmd.command)

            if permission:
                # main command for adding win and lose information
                # syntax: !updategame game='game' winner='winner' losers='losers'
                if cmd.command == 'UPDATEGAME':
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE' or cmd.winner == 'NONE' or cmd.losers == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await client.send_message(message.channel, 'Error: No game specified.')
                        # error message if winner not specified
                        if cmd.winner == 'NONE':
                            print('[ERROR] No winner specified')
                            await client.send_message(message.channel, 'Error: No winner specified.')
                        #error message if losers not specified
                        if cmd.losers == 'NONE':
                            print('[ERROR] No losers specified')
                            await client.send_message(message.channel, 'Error: No losers specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Winner: %s' % cmd.winner)
                        print('[INFO] Losers: %s' % cmd.losers)

                        # try updating the stats
                        status = incrementStats(message.channel, gameFileName, cmd.winner, cmd.losers)
                        await client.send_message(message.channel, status)
                        await client.send_message(message.channel, '<:trains:324019973607653378>')

                elif cmd.command == 'ADDPLAYER':
                    if gameFound:
                        # check for valid number of arguments
                        if len(args) < 1:
                            print('[ERROR] Invalid argument list')
                            await client.send_message(message.channel, 'Error: Invalid number of arguments')
                        else:
                            # get name to add to database
                            playerName = args[0].capitalize()
                            status = editPlayer(message.channel, gameFileName, playerName, editType='ADD')
                            await client.send_message(message.channel, status)
                    else:
                        await client.send_message(message.channel, 'Error: No game specified')

                elif cmd.command == 'REMOVEPLAYER':
                    if gameFound:
                        # check for valid number of arguments
                        if len(args) < 1:
                            print('[ERROR] Invalid argument list')
                            await client.send_message(message.channel, 'Error: Invalid number of arguments')
                        else:
                            # get name to remove from database
                            playerName = args[0].capitalize()
                            status = editPlayer(message.channel, gameFileName, playerName, editType='REMOVE')
                            await client.send_message(message.channel, status)
                    else:
                        await client.send_message(message.channel, 'Error: No game specified')

                elif cmd.command == 'SETPLAYER':
                    if gameFound:
                        if len(args) < 6:
                            print('[ERROR] Invalid argument list')
                            await client.send_message(message.channel, 'Error: Invalid number of arguments')
                        else:
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
                                status = editPlayer(message.channel, gameFileName, playerName, editType='EDIT', wins=winCount, losses=lossCount)
                                await client.send_message(message.channel, status)
                    else:
                        await client.send_message(message.channel, 'Error: No game specified')

                elif cmd.command == 'STATS':
                    if gameFound:
                        # we got a sort type other than default
                        if len(args) > 0:
                            sortType = args[0]
                            statsMsg = dumpStats(message.channel, gameFileName, sortType=sortType)
                            await client.send_message(message.channel, statsMsg)
                        else:
                            # default sorting type
                            statsMsg = dumpStats(message.channel, gameFileName)
                            await client.send_message(message.channel, statsMsg)
                    else:
                        await client.send_message(message.channel, 'Error: No game specified')

                elif cmd.command == 'TRAINSHELP':
                    # we got a command to get help for
                    if len(args) > 0:
                        helpCmd = args[0]
                        helpMsg = helpMessage(helpCmd)
                        await client.send_message(message.channel, helpMsg)
                    else:
                        # send the default help message
                        await client.send_message(message.channel, helpMessage())

                elif cmd.command == 'ADDGAME':
                    # add a new game database
                    if len(args) < 1:
                        print('[ERROR] Invalid argument list')
                        await client.send_message(message.channel, 'Error: Invalid number of arguments')
                    else:
                        gameFileName = args[0].lower() + '_' + config.statsFileName
                        if createDB(gameFileName):
                            print('[INFO] New database created')
                            await client.send_message(message.channel, 'New database created!')
                        else:
                            await client.send_message(message.channel, 'Error: Problem creating database')

            # failed permission check or game check
            else:
                if not permission:
                    print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                    await client.send_message(message.channel, 'Error: You do not have permission to use that command')

client.run(config.botToken)
# https://discordapp.com/oauth2/authorize?client_id=bot_id&scope=bot&permissions=0
