import os
import configparser

class Config:
    def __init__(self):
        if not os.path.isfile('config.ini'):
            # if the file doesnt exist, create it with some default values
            print('[INFO] Config file missing, creating')
            with open('config.ini', 'w') as configFile:
                configFile.write(configText)

        # otherwise read the file
        print('[INFO] Config file exists, parsing')
        # open the file and read the sections
        config = configparser.ConfigParser()
        config.read('config.ini')

        # check if we have all required sections
        reqSections = {'Owner', 'Credentials', 'Chat', 'Files', 'Default'}
        sections = config.sections()
        diff = reqSections.difference(sections)
        if diff:
            # return 0 if differences were found
            raise RuntimeError('The config file is missing the following '
                               'sections: {}'.format(', '.join(['%s' % s for s
                               in diff])) + '. Replace them or delete the file '
                               'to force it to be recreated.')

        # get the config information
        self.ownerID = config.get('Owner', 'OWNER_ID', fallback='NONE')
        self.botToken = config.get('Credentials', 'BOT_TOKEN', fallback='NONE')
        self.cmdPrefix = config.get('Chat', 'CMD_PREFIX', fallback='NONE')
        self.listenID = config.get('Chat', 'LISTEN_CHANNEL', fallback='NONE')
        self.statsFileName = config.get('Files', 'STATS_FILE', fallback='stats') + '.csv'

        # get the default commands and create a default group
        self.groups = set()
        self.defaultGroup = PermissionGroup('Default', config['Default'])

        # loop through the rest of the groups
        permGroups = set(sections).difference(reqSections)
        for group in permGroups:
            # add an instance of the permissions class for each group defined
            self.groups.add(PermissionGroup(group, config[group]))


    # desc: function to check a user's permissions
    # args: user - a discord user or member object
    #       command - the commands to check permission for
    # retn: 1 if the user can use the command, 0 otherwise
    def checkPermission(self, user, command):
        # immediately grant owner permission
        if user.id == self.ownerID:
            return 1

        # check for user override
        for group in self.groups:
            if (user.id in group.users) and (command in group.cmds):
                return 1

        # check for role permissions. needs to be separate loop to avoid
        # returning before user override
        for group in self.groups:
            for role in user.roles:
                if (role.id in group.roles) and (command in group.cmds):
                    return 1

        # check default group
        if command in self.defaultGroup.cmds:
            return 1

        # else return 0 if not found anywhere
        return 0

# groupData is a configparser section
class PermissionGroup:
    def __init__(self, name, groupData):
        self.name = name
        self.cmds = set(groupData.get('CMDS', fallback='NONE').upper().split())
        self.roles = set(groupData.get('ROLES', fallback='NONE').split())
        self.users = set(groupData.get('USERS', fallback='NONE').split())


configText = '''################################################################################
# This is the config file for trainbot. Various parameters need to be          #
# configured here in order for the bot to work. Read the description for each  #
# parameter to find our what it does and the required information. Lines       #
# starting with # are viewed as comments and will not be parsed.               #
################################################################################


################################################################################
# OWNER_ID is the ID of the bot's owner. They will have full access to all     #
# commands. If this is not you, be careful who you grant it to                 #
################################################################################
[Owner]
OWNER_ID = your_id_here


################################################################################
# BOT_TOKEN is the token to be used to login as a bot account. This is         #
# available when creating a Bot User on the Developer site here:               #
# https://discordapp.com/developers/applications/me                            #
################################################################################
[Credentials]
BOT_TOKEN = bot_token_here


################################################################################
# CMD_PREFIX is the character used to determine what will trigger the bot. If  #
# you only want the bot to listen and send messages in a specific text         #
# channel, uncomment LISTEN_CHANNEL and provide the chanel's ID.               #
################################################################################
[Chat]
CMD_PREFIX = !
# LISTEN_CHANNEL =


################################################################################
# STATS_FILE is the name of the file postfix used for storing the stats.       #
################################################################################
[Files]
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
