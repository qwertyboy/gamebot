import discord
import asyncio
from cmds import incrementStats, editPlayer, dumpStats
from config import Config
from db import createDB
from cmdparser import ParseMessage
from help import Help
import random


# initialize help messages
help = Help()
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
    for server in client.guilds:
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
    if message.author.id == '241726136629854208':
        if 'lost' in message.content.lower() and 'game' in message.content.lower():
            await message.channel.send('fuck you')
    
    if message.author.id != client.user.id:
        if 'corn' in message.content.lower():
            if random.randrange(0, 2) == 1:
                await message.channel.send(u'\U0001F33D\U0001F33D\U0001F33D IT\'S RAINING CORN! \U0001F33D\U0001F33D\U0001F33D');
        if message.content == 'same':
            await message.channel.send('same')
    
    if random.randrange(0, 15) == 5:
        await message.add_reaction(u'\U0001F33D')
        
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
                if cmd.command == 'UPDATESTATS':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE' or cmd.winner == 'NONE' or cmd.losers == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await message.channel.send('Error: No game specified.')
                        # error message if winner not specified
                        if cmd.winner == 'NONE':
                            print('[ERROR] No winner specified')
                            await message.channel.send('Error: No winner specified.')
                        #error message if losers not specified
                        if cmd.losers == 'NONE':
                            print('[ERROR] No losers specified')
                            await message.channel.send('Error: No losers specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Winner: %s' % cmd.winner)
                        print('[INFO] Losers: %s' % cmd.losers)

                        # try updating the stats
                        status = incrementStats(message.channel, gameFileName, cmd.winner, cmd.losers)
                        await message.channel.send(status)
                        await message.channel.send('<:trains:324019973607653378>')

                # command for adding a player to a database
                # syntax: !addplayer game='game' name='name'
                elif cmd.command == 'ADDPLAYER':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE' or cmd.name == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await message.channel.send('Error: No game specified.')
                        # error message if player not specified
                        if cmd.name == 'NONE':
                            print('[ERROR] No player specified')
                            await message.channel.send('Error: No player specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Player: %s' % cmd.name)

                        # add the player
                        status = editPlayer(message.channel, gameFileName, cmd.name, editType='ADD')
                        await message.channel.send(status)

                # command for removing a player from a database
                # syntax: !removeplayer game='game' name='name'
                elif cmd.command == 'REMOVEPLAYER':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE' or cmd.name == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await message.channel.send('Error: No game specified.')
                        # error message if player not specified
                        if cmd.name == 'NONE':
                            print('[ERROR] No player specified')
                            await message.channel.send('Error: No player specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Player: %s' % cmd.name)

                        # remove the player
                        status = editPlayer(message.channel, gameFileName, cmd.name, editType='REMOVE')
                        await message.channel.send(status)

                # command for setting a players win and loss stats
                # syntax: !setplayer game='game' name='name' wins='wins' losses='losses'
                elif cmd.command == 'SETPLAYER':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE' or cmd.name == 'NONE' or cmd.wins == 'NONE' or cmd.losses == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await message.channel.send('Error: No game specified.')
                        # error message if player not specified
                        if cmd.name == 'NONE':
                            print('[ERROR] No player specified')
                            await message.channel.send('Error: No player specified.')
                        # error message if wins not specified
                        if cmd.wins == 'NONE':
                            print('[ERROR] No wins specified')
                            await message.channel.send('Error: No wins specified.')
                        # error message if losses not specified
                        if cmd.losses == 'NONE':
                            print('[ERROR] No losses specified')
                            await message.channel.send('Error: No losses specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Player: %s' % cmd.name)

                        # update the players stats
                        status = editPlayer(message.channel, gameFileName, cmd.name, editType='EDIT', wins=cmd.wins, losses=cmd.losses)
                        await message.channel.send(status)

                # command for displaying game stats
                # syntax: !stats game='game' (optional) sort='sort'
                elif cmd.command == 'STATS':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.game == 'NONE':
                        # error message if game not specified
                        if cmd.game == 'NONE':
                            print('[ERROR] No game specified')
                            await message.channel.send('Error: No game specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)
                        print('[INFO] Sorting Type: %s' % cmd.sort)

                        statsMsg = dumpStats(message.channel, gameFileName, sortType=cmd.sort)
                        await message.channel.send(statsMsg)

                elif cmd.command == 'GAMEHELP':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    if cmd.nonKeyed == 'NONE':
                        # return default help message
                        helpMsg = help.helpMessage('LIST')
                    else:
                        # return a help message for the specified command
                        helpMsg = help.helpMessage(cmd.nonKeyed)
                    # send message
                    await message.channel.send(helpMsg)

                # command for creating a new game database
                # syntax: !addgame game
                elif cmd.command == 'ADDGAME':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    # make sure the required arguments were provided
                    if cmd.nonKeyed == 'NONE':
                        print('[ERROR] No game specified')
                        await message.channel.send('Error: No game specified.')
                    else:
                        # print some info to terminal
                        print('[INFO] Game: %s' % cmd.game)

                        gameFileName = cmd.nonKeyed + '_' + config.statsFileName
                        if createDB(gameFileName):
                            print('[INFO] New database created')
                            await message.channel.send('New database created!')
                        else:
                            await message.channel.send('Error: Problem creating database')
                elif cmd.command == 'NATE':
                    # send a typing message because why not
                    await message.channel.trigger_typing()
                    
                    await message.channel.send('no u')

            # failed permission check or game check
            else:
                if not permission:
                    print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                    await message.channel.send('Error: You do not have permission to use that command')

client.run(config.botToken)
# https://discordapp.com/oauth2/authorize?client_id=bot_id&scope=bot&permissions=0
