"""Commands: "!quote [n]"."""
import json
import random

from .command import Command
from .paths import QUOTES_FILE
from .utilities.permission import Permission


class outputQuote(Command):
    """Simple Class to output quotes stored in a json-file."""

    perm = Permission.User

    def __init__(self, bot):
        """Load command list."""
        self.responses = {}
        with open(QUOTES_FILE.format(bot.root)) as file:
            self.quotelist = json.load(file)

    def match(self, bot, user, msg):
        """Match if command starts with !quote."""
        cmd = msg.lower().strip()
        return cmd == "!quote" or cmd.startswith("!quote ")

    def run(self, bot, user, msg):
        """Say a quote."""
        self.responses = bot.responses["outputQuote"]
        cmd = msg.lower().strip()
        if cmd == "!quote":
            quote = random.choice(self.quotelist)
            bot.write(quote)
        elif cmd.startswith("!quote "):
            arg = cmd[len("!quote "):]
            try:
                arg = int(arg.strip()) - 1      # -1: So list for users goes from 1 to len + 1
                if arg >= 0 and arg < len(self.quotelist):
                    quote = self.quotelist[arg]
                    bot.write(quote)
                else:
                    var = {"<N_QUOTES>": len(self.quotelist)}
                    bot.write(bot.replace_vars(self.responses["not_found"]["msg"], var))
            except ValueError:
                bot.write(self.responses["wrong_input"]["msg"])