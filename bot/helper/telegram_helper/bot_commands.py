from bot import CMD_SUFFIX

class _BotCommands:
    def __init__(self):
        self.StartCommand = f'start{CMD_SUFFIX}'
        self.CloneCommand = f'clone{CMD_SUFFIX}'
        self.CountCommand = f'count{CMD_SUFFIX}'
        self.DeleteCommand = f'del{CMD_SUFFIX}'
        self.CancelMirror = f'cancel{CMD_SUFFIX}'
        self.CancelAllCommand = f'cancelall{CMD_SUFFIX}'
        self.ListCommand = f'list{CMD_SUFFIX}'
        self.StatusCommand = f'status{CMD_SUFFIX}'
        self.UsersCommand = f'users{CMD_SUFFIX}'
        self.AuthorizeCommand = f'authorize{CMD_SUFFIX}'
        self.UnAuthorizeCommand = f'unauthorize{CMD_SUFFIX}'
        self.PingCommand = f'ping{CMD_SUFFIX}'
        self.StatsCommand = f'stats{CMD_SUFFIX}'
        self.HelpCommand = f'help{CMD_SUFFIX}'
        
BotCommands = _BotCommands()
