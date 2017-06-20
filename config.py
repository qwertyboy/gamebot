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

configText = ''';------------------------------------------------------------------------------;
; This is the config file for trainbot. Various parameters need to be          ;
; configured here in order for the bot to work. Read the description for each  ;
; parameter to find our what it does and the required information. Lines       ;
; starting with ; are viewed as comments and will not be parsed.               ;
;------------------------------------------------------------------------------;

;------------------------------------------------------------------------------;
; OWNER_ID is the ID of the bot's owner. They will have full access to all     ;
; commands. If this is not you, be careful who you grant it to                 ;
;------------------------------------------------------------------------------;
OWNER_ID = your_id_here

;------------------------------------------------------------------------------;
; BOT_TOKEN is the token to be used to login as a bot account. This is         ;
; available when creating a Bot User on the Developer site here:               ;
; https://discordapp.com/developers/applications/me                            ;
;------------------------------------------------------------------------------;
BOT_TOKEN = bot_token_here

;------------------------------------------------------------------------------;
; CMD_PREFIX is the character used to determine what will trigger the bot.     ;
; Example:                                                                     ;
;   CMD_PREFIX = !                                                             ;
;   !addplayer                                                                 ;
;------------------------------------------------------------------------------;
CMD_PREFIX = !

;------------------------------------------------------------------------------;
; STATS_FILE is the name of the file used for storing the stats.               ;
;------------------------------------------------------------------------------;
STATS_FILE = stats

;------------------------------------------------------------------------------;
; DEFAULT_CMDS and DEFAULT_ROLE control what commands are available by         ;
; default. The commands listed after DEFAULT_CMDS are grated to user with      ;
; DEFAULT_ROLE or @everyone if no role is provided. DEFAULT_ROLE expects the   ;
; ID of the role. Commands should be seperated by a space.                     ;
;------------------------------------------------------------------------------;
DEFAULT_CMDS = stats help
DEFAULT_ROLE = 131586834642894849

;------------------------------------------------------------------------------;
; ADMIN_CMDS and ADMIN_ROLE function the same as DEFAULT_CMDS and DEFAULT_ROLE ;
; but are used for setting permissions for commands that should only be used   ;
; by trusted users or roles. It is a good idea to restrict the addplayer,      ;
; removeplayer, and setplayer commands to this.                                ;
;------------------------------------------------------------------------------;
ADMIN_CMDS = addplayer removeplayer setplayer
ADMIN_ROLE = 319626374241320973

;------------------------------------------------------------------------------;
; UPDATE_DB_ROLE functions the same as DEFAULT_ROLE and ADMIN_ROLE but is      ;
; provided to allow the choochoo command to be used by roles without access to ;
; admin commands. Set this to the same as ADMIN_ROLE if you want the same      ;
; restriction on it.                                                           ;
;------------------------------------------------------------------------------;
UPDATE_DB_ROLE = 319626374241320973
'''
