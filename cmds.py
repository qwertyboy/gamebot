import discord
import asyncio
from db import readDB, writeDB

# desc: function to search a list of lists for a name
# args: name - the name to search the lists for
#       searchList - a list of lists to search for a name
# retn: the index of the list containing the name or -1 if not found
def getIndex(name, searchList):
    for i in range(0, len(searchList)):
        if name in searchList[i]:
            return i
    return -1


# desc: function to round a number up to a specific increment. for example,
#       rounding 11 to the nearest multiple of 2 would result in 12
# args: num - the number to round up
#       multiple - the increment to round to
# retn: the rounded number
def roundMultiple(num, multiple):
    if num % multiple:
        return num + (multiple - (num % multiple))
    return num


# desc: function to update the database
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       winner - a string containing the winner's name
#       losers - a list of strings containing the losers' names
async def incrementStats(msgChannel, statsFile, winner, losers):
    # read the database
    data = readDB(statsFile)
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
        if writeDB(statsFile, data.headers, rows):
            await client.send_message(msgChannel, 'Database updated successfully!')
        else:
            print('[INFO] Database not updated')
            await client.send_message(msgChannel, 'Error: Unable to open database for writing')
    else:
        print('[INFO] Database not updated')
        await client.send_message(msgChannel, 'Database not updated')


# desc: function to add a player to the database or edit an existing player
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       player - the name of the player to either add to the db or edit
#       editType - either 'ADD' or 'EDIT' or 'REMOVE' - sets type of change happening
#       wins - the number of wins to assign the player
#       losses - the number of losses to assign the player
async def editPlayer(msgChannel, statsFile, player, editType, wins='0', losses='0'):
    # open up the database
    data = readDB(statsFile)
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
            if writeDB(statsFile, data.headers, rows):
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
            if writeDB(statsFile, data.headers, rows):
                print('[INFO] %s\'s data changed' % player)
                await client.send_message(msgChannel, 'Database updated successfully!')
            else:
                print('[INFO] Database not updated')
                await client.send_message(msgChannel, 'Error: Unable to open database for writing')
    elif editType == 'REMOVE':
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
            if writeDB(statsFile, data.headers, rows):
                print('[INFO] \"%s\" removed from database' % player)
                await client.send_message(msgChannel, 'Database updated successfully!')
            else:
                print('[INFO] Database not updated')
                await client.send_message(msgChannel, 'Error: Unable to open database for writing')


# desc: function to display the stats
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       sortType - the order in which the results should be sorted.
#                  options are 'WINRATE', 'WINS', 'LOSSES', or 'NAME'.
#                  will revert to 'NAME' if invalid
#       player - NOT IMPLEMENTED - the player to display stats for
async def dumpStats(msgChannel, statsFile, sortType='WINRATE', player='ALL'):
    # read database
    data = readDB(statsFile)
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
    elif sortType == 'NAME':
        # database is stored sorted by name so dont do anything
        pass
    else:
        print('[ERROR] Invalid sorting type specified. Displaying stats as stored')
        await client.send_message(msgChannel, 'Error: Invalid sorting type. Displaying stats as stored.')

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