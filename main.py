from MageBot import MageBot
from FighterBot import FighterBot
import sys

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: {} [mage|fighter]".format(sys.argv[0]))
        sys.exit(1)

    bot_type = sys.argv[1]
    if bot_type == "mage":
        bot = MageBot()
    elif bot_type == "fighter":
        bot = FighterBot()
    else:
        print("Choose between mage or fighter")
        sys.exit(1)

    bot.main_loop()
