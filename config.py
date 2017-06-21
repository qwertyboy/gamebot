import os
from collections import namedtuple

# desc: function to create a config file
def readConfig():
    if not os.path.isfile('config.ini'):
        # if the file doesnt exist, create it with some default values
        print('[INFO] Config file missing, creating')
        with open('config.ini', 'w') as configFile:
            configFile.write(configText)

    # otherwise read the file
    ConfigTuple = namedtuple('ConfigTuple', ['OWNER_ID', 'BOT_TOKEN', 'CMD_PREFIX',
                                             'STATS_FILE', 'DEFAULT_CMDS', 'DEFAULT_ROLE',
                                             'ADMIN_CMDS', 'ADMIN_ROLE', 'UPDATE_DB_ROLE'])
    print('[INFO] Config file exists, parsing')
    with open('config.ini', 'r') as configFile:
        for line in configFile:
            # split up line and get parameter
            line = line.split('=')
            param = line[0].strip()

            if param == 'OWNER_ID':
                # get owner id
                ownerID = line[1].strip()
            elif param == 'BOT_TOKEN':
                # get bot token
                botToken = line[1].strip()
            elif param == 'CMD_PREFIX':
                # get command prefix
                cmdPrefix = line[1].strip()
            elif param == 'STATS_FILE':
                # get
                statsFile = line[1].strip() + '.csv'
                elif

configText = '''################################################################################
# This is the config file for trainbot. Various parameters need to be          #
# configured here in order for the bot to work. Read the description for each  #
# parameter to find our what it does and the required information. Lines       #
# starting with # are viewed as comments and will not be parsed.               #
################################################################################

[Owner]
################################################################################
# OWNER_ID is the ID of the bot's owner. They will have full access to all     #
# commands. If this is not you, be careful who you grant it to                 #
################################################################################
OWNER_ID = your_id_here

[Credentials]
################################################################################
# BOT_TOKEN is the token to be used to login as a bot account. This is         #
# available when creating a Bot User on the Developer site here:               #
# https://discordapp.com/developers/applications/me                            #
################################################################################
BOT_TOKEN = bot_token_here

[Chat]
################################################################################
# CMD_PREFIX is the character used to determine what will trigger the bot. If  #
# you only want the bot to listen and send messages in a specific text         #
# channel, uncomment LISTEN_CHANNEL and provide the chanel's ID.               #
################################################################################
CMD_PREFIX = !
# LISTEN_CHANNEL =

[Files]
################################################################################
# STATS_FILE is the name of the file used for storing the stats.               #
################################################################################
STATS_FILE = stats



################################################################################
#                                 PERMISSIONS                                  #
#                                                                              #
# Permissions can be configured in any way desired and are configured in       #
# groups. To create a permission group, copy the section below and change the  #
# name of the header contained in the [square brackets].                       #
#                                                                              #
# [Group Name]                                                                 #
# CMDS = command1 command1                                                     #
# ROLES = 112233445566778899 998877665544332211                                #
# USERS = 102030405060708090                                                   #
#                                                                              #
# The commands listed after CMDS are the commands available to the group. The  #
# role IDs listed after ROLES are the server roles that will be granted CMDS.  #
# If you want to override a role for a specific user, list their ID after      #
# USERS. There are a couple groups already created below as examples. You are  #
# free to modify them as needed but do not remove the Default group.           #
################################################################################

# Do not rename or delete this role. These permissions are assigned to anyone
# who doesn't get assigned to another group.
[Default]
CMDS = help
# ROLES =
# USERS =

[Members]
CMDS = stats help
ROLES = 131586834642894849
# USERS =

[Mods]
CMDS = choochoo addplayer stats help
ROLES = 319626374241320973
# USERS =
'''
