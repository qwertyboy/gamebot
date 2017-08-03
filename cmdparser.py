# desc: a class to parse the command received
# args: message - the received message
# retn: a named tuple containing the parsed data
class ParseMessage:
    def __init__(self, message):
        # get the arguments in the message
        self.args = message.content.upper().split()
        # get the command after the command prefix
        self.command = self.args.pop(0)[1:]

        # initialize the params with default values
        self.game = 'NONE'
        self.name = 'NONE'
        self.wins = 'NONE'
        self.sort = 'NONE'
        self.losses = 'NONE'
        self.winner = 'NONE'
        self.losers = 'NONE'
        self.nonKeyed = 'NONE'

        # iterate through each argument
        for arg in self.args:
            # split the argument into its parameters
            try:
                key, value = arg.split('=')
            except ValueError:
                key = 'NONE'
                value = arg

            # set the command params
            if key == 'GAME':
                self.game = value
            elif key == 'NAME':
                self.name = value
            elif key == 'WINS':
                self.wins = value
            elif key == 'SORT':
                self.sort = value
            elif key == 'LOSSES':
                self.losses = value
            elif key == 'WINNER':
                self.winner = value
            elif key == 'LOSERS':
                self.losers = value.split(',')
            elif key == 'NONE':
                self.nonKeyed = value
