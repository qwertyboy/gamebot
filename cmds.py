import discord
from collections import Counter
from db import readDB, writeDB
from help import Help

# get the help messages
help = Help()

INFO_DB_SUCCESS = 'Database updated successfully!'
ERROR_DB_ERROR = 'Error: Unable to open database for writing'

ERROR_PLAYER_NOT_FOUND = 'Error: \"%s\" not found in database. Check your spelling or use !addplayer first.'
ERROR_WIN_IN_LOSE = 'Error: \"%s\" already specified as winner.'
ERROR_DUP_LOSER = 'Error: \"%s\" duplicated in losers list'

ERROR_IN_DB = 'Error: \"%s\" is already in the database'

ERROR_SORT_ERROR = 'Error while sorting list. Make sure all players have at least one win or loss.\n'
ERROR_INVALID_SORT = 'Error: Invalid sorting type. Displaying stats as stored.\n'

ERROR_CMD_NOT_FOUND = 'Error: \"%s\" is not a valid command.'

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


# desc: function to find duplicate items in a list
# args: inputList - a list to search for duplicates
# retn: a list containing the duplicates
def findDuplicates(inputList):
    dupList = [k for k, v in Counter(inputList).items() if v > 1]
    return dupList


# desc: function to update the database
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       winner - a string containing the winner's name
#       losers - a list of strings containing the losers' names
# retn: a string indicating success or failure
def incrementStats(msgChannel, statsFile, winner, losers):
    # read the database
    data = readDB(statsFile)
    rows = data.rows

    # check if the winner is actually in the database
    if getIndex(winner, rows) < 0:
        print('[ERROR] Winner \"%s\" not found in database' % winner)
        return (ERROR_PLAYER_NOT_FOUND % winner)

    # check if losers are in database
    for loser in losers:
        # get loser index
        loserIndex = getIndex(loser, rows)

        # check against winner to see if the name was duplicated
        if loser == winner:
            print('[ERROR] Winner duplicated in losers field')
            return (ERROR_WIN_IN_LOSE % loser)
        # check if loser was not found in database
        if loserIndex < 0:
            print('[ERROR] Loser \"%s\" not found in database' % loser)
            return (ERROR_PLAYER_NOT_FOUND % loser)

    # check for duplicate losers
    dupList = findDuplicates(losers)
    if len(dupList) > 0:
        print('[ERROR] Duplicate losers found')
        return (ERROR_DUP_LOSER % dupList)

    # update stats if we found the winner and all losers
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
        return INFO_DB_SUCCESS
    else:
        print('[INFO] Database not updated')
        return ERROR_DB_ERROR


# desc: function to add a player to the database or edit an existing player
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       player - the name of the player to either add to the db or edit
#       editType - either 'ADD' or 'EDIT' or 'REMOVE' - sets type of change happening
#       wins - the number of wins to assign the player
#       losses - the number of losses to assign the player
# retn: a string indicating success or failure
def editPlayer(msgChannel, statsFile, player, editType, wins='0', losses='0'):
    # open up the database
    data = readDB(statsFile)
    rows = data.rows
    playerIndex = getIndex(player, rows)

    # check if player is already in database
    if editType == 'ADD':
        if playerIndex > -1:
            print('[ERROR] \"%s\" already in database' % player)
            print('[INFO] Database not updated')
            return (ERROR_IN_DB % player)
        else:
            # add player to list and resort
            rows.append([player, wins, losses])
            rows.sort(key=lambda name: name[0].capitalize())

            # write the new data to the database file
            if writeDB(statsFile, data.headers, rows):
                print('[INFO] \"%s\" added to database' % player)
                return INFO_DB_SUCCESS
            else:
                print('[INFO] Database not updated')
                return ERROR_DB_ERROR
    elif editType == 'EDIT':
        if playerIndex < 0:
            print('[ERROR] \"%s\" not found in database' % player)
            print('[INFO] Database not updated')
            return (ERROR_PLAYER_NOT_FOUND % player)
        else:
            rows[playerIndex] = [rows[playerIndex][0], wins, losses]

            # write the new data to the database file
            if writeDB(statsFile, data.headers, rows):
                print('[INFO] %s\'s data changed' % player)
                return INFO_DB_SUCCESS
            else:
                print('[INFO] Database not updated')
                return ERROR_DB_ERROR
    elif editType == 'REMOVE':
        if playerIndex < 0:
            print('[ERROR] \"%s\" not found in database' % player)
            print('[INFO] Database not updated')
            return (ERROR_PLAYER_NOT_FOUND % player)
        else:
            # delete player from list
            del(rows[playerIndex])
            # write the new data to the database
            if writeDB(statsFile, data.headers, rows):
                print('[INFO] \"%s\" removed from database' % player)
                return INFO_DB_SUCCESS
            else:
                print('[INFO] Database not updated')
                return ERROR_DB_ERROR


# desc: function to display the stats
# args: msgChannel - the channel the invoking message was sent from
#       statsFile - the name of the database file
#       sortType - the order in which the results should be sorted.
#                  options are 'WINRATE', 'WINS', 'LOSSES', or 'NAME'.
#                  will revert to 'NAME' if invalid
#       player - NOT IMPLEMENTED - the player to display stats for
# retn: a string formatted with the database stats
def dumpStats(msgChannel, statsFile, sortType='WINRATE', player='ALL'):
    # read database
    data = readDB(statsFile)
    rows = data.rows

    print('[INFO] Sort type is %s' % sortType)
    returnMsg = ''
    if sortType == 'WINRATE':
        # sort data by win rate
        try:
            rows.sort(key=lambda rate: float(rate[1]) / (float(rate[1]) + float(rate[2])), reverse=True)
        except ZeroDivisionError:
            print('[ERROR] Tried to divide by zero because of blank player data')
            returnMsg = ERROR_SORT_ERROR
    elif sortType == 'WINS':
        # sort by number of wins and reverse so max is first
        rows.sort(key=lambda wins: float(wins[1]), reverse=True)
    elif sortType == 'LOSSES':
        # sort by number of losses and reverse so max is first
        rows.sort(key=lambda losses: float(losses[2]), reverse=True)
    elif sortType == 'NAME':
        # database is stored sorted by name so dont do anything
        pass
    else:
        print('[ERROR] Invalid sorting type specified. Displaying stats as stored')
        returnMsg = ERROR_INVALID_SORT

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
            if float(winCount) <= 0:
                winRate = '0'
            elif float(loseCount) <= 0:
                winRate = ' 100'
            else:
                winRate = str((float(winCount) / (float(winCount) + float(loseCount))) * 100)

            # truncate win rate and create string with player info
            winRate = winRate[0:4].rjust(9)
            playerString += playerName + winCount + loseCount + winRate + ' %\n'

        # calculate padding for name field and create header final strings
        namePaddingLen = roundMultiple((maxPlayerLen + 2), 2)
        header = ' |' + 'Name'.center(namePaddingLen) + '| Wins | Losses | Win Rate |\n'
        divider = ('-' * len(header)) + '\n'
        sendString = '```md\n' + header + divider + playerString + '```'

        # return the constructed string
        if len(returnMsg) > 0:
            returnMsg = returnMsg + sendString
            return returnMsg
        return sendString


# desc: a function to display a help message
# args: the command to show help for, defaults to listing them
# retn: a string formatted with the help information
def helpMessage(cmd='LIST'):
    if cmd == 'LIST':
        return help.helpMsg
    else:
        try:
            return help.cmdHelp[cmd]
        except KeyError:
            return ERROR_CMD_NOT_FOUND % cmd
