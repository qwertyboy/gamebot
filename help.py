class Help:
    def __init__(self):
        seperator = '----------------------------------------------------------------------------\n'

        choochooUsage = '\t!choochoo win [winner] lose [loser1 loser2 etc]'
        choochooHelp = ('```md\n'
                       'The \'choochoo\' command is used for updating the '
                       'database when a game is completed. It requires a winner '
                       'and at least one loser. The syntax is as follows:\n'
                       + seperator + choochooUsage + '```')

        addplayerUsage = '\t!addplayer [player]'
        addplayerHelp = ('```The \'addplayer\' command is used for adding a player '
                        'to the database. It requires the name of the player to '
                        'add. The syntax is as follows:\n' + addplayerUsage + '```')

        removeplayerUsage = '\t!removeplayer [player]'
        removeplayerHelp = ('```The \'removeplayer\' command is used for removing a '
                           'player from the database. It requires the name of '
                           'the player to remove. NOTE: This is permanent and '
                           'all data for the specified player will be lost. The '
                           'syntax is as follows:\n' + removeplayerUsage + '```')

        setplayerUsage = '\t!setplayer name [name] wins [win_count] losses [loss_count]'
        setplayerHelp = ('```The \'setplayer\' command is used for setting the wins '
                        'and loss counts of a specified player. It requires the '
                        'name of the player, the number of wins, and the number '
                        'of losses. The syntax is as follows:\n' + setplayerUsage + '```')

        statsUsage = '\t!stats <winrate | wins | losses>'
        statsHelp = ('```The \'stats\' command is used for displaying the win and '
                    'loss statistics stored in the database. It does not require '
                    'any arguments but you can optionally specify a sorting order. '
                    'Accepted sorting orders are \'winrate\', \'wins\', and '
                    '\'losses\'. If no sorting order is specified, the default '
                    '\'winrate\' order will be used. The syntax is as follows:\n'
                    + statsUsage + '```')

        self.helpMsg = ('```md\n'
                       'These are the available commands. Arguments displayed in '
                       '[square brackets] are required. Arguments displayed in '
                       '<angle brackets> are optional. To see more information about '
                       'a specific command, use \'!trainshelp <command>\'\n'
                       '----------------------------------------------------------------------------\n'
                       + choochooUsage + '\n'
                       + addplayerUsage + '\n'
                       + removeplayerUsage + '\n'
                       + setplayerUsage + '\n'
                       + statsUsage + '\n'
                       '```')

        self.cmdHelp = {'CHOOCHOO': choochooHelp, 'ADDPLAYER': addplayerHelp,
                        'REMOVEPLAYER': removeplayerHelp, 'SETPLAYER': setplayerHelp,
                        'STATS': statsHelp}
