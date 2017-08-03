class Help:
    ERROR_CMD_NOT_FOUND = 'Error: \"%s\" is not a valid command.'

    def __init__(self):
        seperator = '----------------------------------------------------------------------------\n'

        updatestatsUsage = '\t!updatestats game=[Game Name] winner=[Winner Name] losers=[Loser1,Loser2,etc...]'
        updatestatsHelp = ('```md\n'
                       'The \'updatestats\' command is used for updating the '
                       'database when a game is completed. It requires a game, '
                       'a winner, and at least one loser. The losers must be '
                       'seperated with ONLY a comma.The syntax is as follows:\n'
                       + seperator + updatestatsUsage + '```')

        addplayerUsage = '\t!addplayer game=[Game Name] name=[Player Name]'
        addplayerHelp = ('```md\n'
                        'The \'addplayer\' command is used for adding a player '
                        'to the database. It requires the game and the name of '
                        'the player to add. The syntax is as follows:\n'
                        + seperator + addplayerUsage + '```')

        removeplayerUsage = '\t!removeplayer game=[Game Name] name=[Player Name]'
        removeplayerHelp = ('```md\n'
                           'The \'removeplayer\' command is used for removing a '
                           'player from the database. It requires the game and '
                           'the name of the player to remove. NOTE: This is '
                           'permanent and all data for the specified player will'
                           ' be lost. The syntax is as follows:\n'
                           + seperator + removeplayerUsage + '```')

        setplayerUsage = '\t!setplayer game=[Game Name] name=[Player Name] wins=[Win Count] losses=[Loss Count]'
        setplayerHelp = ('```md\n'
                        'The \'setplayer\' command is used for setting the wins '
                        'and loss counts of a specified player. It requires the '
                        'game, the name of the player, the number of wins, and '
                        'the number of losses. The syntax is as follows:\n'
                        + seperator + setplayerUsage + '```')

        statsUsage = '\t!stats game=[Game Name] sort=<Sort Type>'
        statsHelp = ('```md\n'
                    'The \'stats\' command is used for displaying the win and '
                    'loss statistics stored in the database. It requires the '
                    'game to display stats for. Optionally, a sorting type can '
                    'be specified. Accepted sorting orders are \'winrate\', '
                    '\'wins\', and \'losses\'. If no sorting order is specified,'
                    ' the default \'winrate\' order will be used. The syntax is '
                    'as follows:\n' + seperator + statsUsage + '```')

        helpUsage = '\t!gamehelp <Command>'
        helpHelp = ('```md\n'
                   'Displays the help message. A command can be given as an '
                   'argument to see more information on that command. The syntax'
                   ' is as follows:\n' + seperator + helpUsage + '```')

        addgameUsage = '\t!addgame [Game Name]'
        addgameHelp = ('```md\n'
                      'The \'addgame\' command is used to create a database for '
                      'a new game. The only required argument is the name of the'
                      ' game. The name must be one word and will be used for all'
                      ' other commands. The syntax is as follows:\n'
                      + seperator + addgameUsage + '```')

        self.helpMsg = ('```md\n'
                       'These are the available commands. Arguments displayed in '
                       '[square brackets] are required. Arguments displayed in '
                       '<angle brackets> are optional. To see more information about '
                       'a specific command, use \'!gamehelp <command>\'\n'
                       '----------------------------------------------------------------------------\n'
                       + updatestatsUsage + '\n'
                       + addplayerUsage + '\n'
                       + removeplayerUsage + '\n'
                       + setplayerUsage + '\n'
                       + statsUsage + '\n'
                       + addgameUsage + '\n'
                       + helpUsage +
                       '```')

        self.cmdHelp = {'UPDATESTATS': updatestatsHelp, 'ADDPLAYER': addplayerHelp,
                        'REMOVEPLAYER': removeplayerHelp, 'SETPLAYER': setplayerHelp,
                        'STATS': statsHelp, 'GAMEHELP': helpHelp, 'ADDGAME': addgameHelp}


    # desc: a function to display a help message
    # args: the command to show help for, defaults to listing them
    # retn: a string formatted with the help information
    def helpMessage(self, cmd='LIST'):
        if cmd == 'LIST':
            return self.helpMsg
        else:
            try:
                return self.cmdHelp[cmd]
            except KeyError:
                return ERROR_CMD_NOT_FOUND % cmd
