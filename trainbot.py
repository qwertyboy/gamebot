import os
import discord
import asyncio
import csv
from collections import namedtuple

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

# function to check permissions for a command
def checkPermission(user, roleList):
    # check command permissions
    for role in user.roles:
        if role.id in roleList:
            return 1
    return 0

# function to search a list of lists for a name
def getIndex(name, searchList):
    for i in range(0, len(searchList)):
        if name == searchList[i][0]:
            return i
    return -1


# function to round a number to a specific multiple
def roundMultiple(num, multiple):
    if num % multiple:
        return num + (multiple - (num % multiple))
    return num


# function to read database
def readDB(fileName):
    # open file and get rows
    with open(fileName, newline='') as stats:
        reader = csv.reader(stats, delimiter=',', quotechar='"')
        # get column headers
        headers = next(reader)
        # get rows
        rows = list(reader)
        print('[INFO] Database read successful')

    Data = namedtuple('Data', ['headers', 'rows'])
    r = Data(headers, rows)
    return r


# function to wrte the database
def writeDB(fileName, headers, rows):
    try:
        # write the new data to the database file
        with open(fileName, 'w', newline='') as stats:
            writer = csv.writer(stats, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
            print('[INFO] Database write successful')
        return 1
    except PermissionError:
        print('[ERROR] Unable to open database file for writing')
        return 0


# function to update the database
async def incrementStats(msgChannel, winner, losers):
    # read the database
    data = readDB(STATS_FILE)
    rows = data.rows

    # check if the winner is actually in the database
    winnerFound = 1
    if getIndex(winner, rows) < 0:
        winnerFound = 0
        print('[ERROR] Winner \"%s\" not found in database' % winner)
        await client.send_message(msgChannel, 'Error: \"%s\" not found in '
                                  'database. Check your spelling or use '
                                  '!addplayer first.' % winner)

    # check if losers are in database
    losersFound = 1
    for loser in losers:
        # get loser index
        loserIndex = getIndex(loser, rows)

        # check against winner to see if the name was duplicated
        if loser == winner:
            losersFound = 0
            print('[ERROR] Winner duplicated in losers field')
            await client.send_message(msgChannel, 'Error: \"%s\" already specified'
                                                   ' as winner.' % loser)
        # check if loser was not found in database
        elif loserIndex < 0:
            losersFound = 0
            print('[ERROR] Loser \"%s\" not found in database' % loser)
            await client.send_message(msgChannel, 'Error: \"%s\" not found '
                                      'in database. Check your spelling or use '
                                      '!addplayer first.' % loser)

    # check for duplicate losers
    if len(losers) != len(set(losers)):
        losersFound = 0
        print('[ERROR] Duplicate losers found')
        await client.send_message(msgChannel, 'Error: Name duplicated in losers list')

    # update stats if we found the winner and all losers
    if winnerFound and losersFound:
        # get index, get win count, increment and update
        winnerIndex = getIndex(winner, rows)
        winnerVal = int(rows[winnerIndex][1])
        rows[winnerIndex][1] = str(winnerVal + 1)

        # same as winner for each loser
        for loser in losers:
            loserIndex = getIndex(loser, rows)
            loserVal = int(rows[loserIndex][2])
            rows[loserIndex][2] = str(loserVal + 1)

        # write the new data to the database file
        if writeDB(STATS_FILE, data.headers, rows):
            await client.send_message(msgChannel, 'Database updated successfully!')
        else:
            print('[INFO] Database not updated')
            await client.send_message(msgChannel, 'Error: Unable to open database for writing')
    else:
        print('[INFO] Database not updated')
        await client.send_message(msgChannel, 'Database not updated')


# function to add a player to the database
async def editPlayer(msgChannel, player, editType='ADD', wins='0', losses='0'):
    # open up the database
    data = readDB(STATS_FILE)
    rows = data.rows
    playerIndex = getIndex(player, rows)

    # check if player is already in database
    if editType == 'ADD':
        if playerIndex > -1:
            print('[ERROR] \"%s\" already in database' % player)
            await client.send_message(msgChannel, 'Error: \"%s\" is already in the '
                                                  'database' % player)
            print('[INFO] Database not updated')
            await client.send_message(msgChannel, 'Database not updated')
        else:
            # add player to list and resort
            rows.append([player, wins, losses])
            rows.sort(key=lambda name: name[0].capitalize())

            # write the new data to the database file
            if writeDB(STATS_FILE, data.headers, rows):
                print('[INFO] \"%s\" added to database' % player)
                await client.send_message(msgChannel, 'Database updated successfully!')
            else:
                print('[INFO] Database not updated')
                await client.send_message(msgChannel, 'Error: Unable to open database for writing')
    elif editType == 'EDIT':
        if playerIndex < 0:
            print('[ERROR] \"%s\" not found in database' % player)
            await client.send_message(msgChannel, 'Error: \"%s\" not found '
                                      'in database. Check your spelling or use '
                                      '!addplayer first.' % player)
            print('[INFO] Database not updated')
            await client.send_message(msgChannel, 'Database not updated')
        else:
            rows[playerIndex] = [rows[playerIndex][0], wins, losses]

            # write the new data to the database file
            if writeDB(STATS_FILE, data.headers, rows):
                print('[INFO] %s\'s data changed' % player)
                await client.send_message(msgChannel, 'Database updated successfully!')
            else:
                print('[INFO] Database not updated')
                await client.send_message(msgChannel, 'Error: Unable to open database for writing')


# function to remove a player
async def removePlayer(msgChannel, player):
    data = readDB(STATS_FILE)
    rows = data.rows

    # check if player is in database
    playerIndex = getIndex(player, rows)
    if playerIndex < 0:
        print('[ERROR] \"%s\" not found in database' % player)
        await client.send_message(msgChannel, 'Error: \"%s\" was not found in '
                                              'the database' % player)
        print('[INFO] Database not updated')
        await client.send_message(msgChannel, 'Database not updated')
    else:
        # delete player from list
        del(rows[playerIndex])
        # write the new data to the database
        if writeDB(STATS_FILE, data.headers, rows):
            print('[INFO] \"%s\" removed from database' % player)
            await client.send_message(msgChannel, 'Database updated successfully!')
        else:
            print('[INFO] Database not updated')
            await client.send_message(msgChannel, 'Error: Unable to open database for writing')


# function to display the stats
async def dumpStats(msgChannel, sortType='NAME', player='ALL'):
    # read database
    data = readDB(STATS_FILE)
    rows = data.rows

    print('[INFO] Sort type is %s' % sortType)
    if sortType == 'WINRATE':
        # sort data by win rate
        try:
            rows.sort(key=lambda rate: int(rate[1]) / (int(rate[1]) + int(rate[2])), reverse=True)
        except ZeroDivisionError:
            print('[ERROR] Tried to divide by zero because of blank player data')
            await client.send_message(msgChannel, 'Error while sorting list. Make '
                                                  'sure all players have at least '
                                                  'one win or loss.')
    elif sortType == 'WINS':
        # sort by number of wins and reverse so max is first
        rows.sort(key=lambda wins: int(wins[1]), reverse=True)
    elif sortType == 'LOSSES':
        # sort by number of losses and reverse so max is first
        rows.sort(key=lambda losses: int(losses[2]), reverse=True)

    if player == 'ALL':
        # get max player length
        maxPlayerLen = 0
        for player in rows:
            if len(player[0]) > maxPlayerLen:
                maxPlayerLen = len(player[0])

        # construct a string with all the player info
        playerString = ''
        # adjust start spacing if player length is odd or even to align with pipe
        startSpace = 4 if maxPlayerLen % 2 else 3
        for player in rows:
            playerName = player[0].rjust(maxPlayerLen + startSpace)
            winCount = player[1].rjust(7)
            loseCount = player[2].rjust(9)
            # calculate win rate
            if int(winCount) == 0:
                winRate = '0'
            elif int(loseCount) == 0:
                winRate = ' 100'
            else:
                winRate = str((int(winCount) / (int(winCount) + int(loseCount))) * 100)

            # truncate win rate and create string with player info
            winRate = winRate[0:4].rjust(9)
            playerString += playerName + winCount + loseCount + winRate + ' %\n'

        # calculate padding for name field and create header final strings
        namePaddingLen = roundMultiple((maxPlayerLen + 2), 2)
        header = ' |' + 'Name'.center(namePaddingLen) + '| Wins | Losses | Win Rate |\n'
        divider = ('-' * len(header)) + '\n'
        sendString = '```md\n' + header + divider + playerString + '```'
        await client.send_message(msgChannel, sendString)


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

                    await incrementStats(message.channel, winner, losers)
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
                    await editPlayer(message.channel, playerName)
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
                    await removePlayer(message.channel, playerName)
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
                        await editPlayer(message.channel, playerName, editType='EDIT', wins=winCount, losses=lossCount)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'stats':
            # check permissions
            if checkPermission(msgAuthor, CMD_ROLES) or checkPermission(msgAuthor, STAT_ROLES):
                if len(args) > 0:
                    sortType = args[0].upper()
                    await dumpStats(message.channel, sortType=sortType)
                else:
                    await dumpStats(message.channel)
            else:
                print('[ERROR] %s does not have permission to use this command' % msgAuthor.name)
                await client.send_message(message.channel, 'Error: You do not have permission to use that command')

        elif command == 'trainshelp':
            # send the help message
            await client.send_message(message.channel, helpMsg)

client.run('bot token')
# https://discordapp.com/oauth2/authorize?client_id=bot_id&scope=bot&permissions=0
