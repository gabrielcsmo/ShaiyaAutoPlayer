from Bot import Bot
import keyboard as kb
from time import sleep
from random import randint, choice

class MageBot(Bot):

    MIN_ATTACKS = 2
    MAX_ATTACKS = 3

    #SPELLS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    SPELLS = {'arrow' : '1'}

    AA_KEY = ['~']
    FW_KEY = ['w']
    BW_KEY = ['s']
    RIGHT_KEY = ['d']
    LEFT_KEY = ['a']
    MOVE_RIGHT = ['e']
    MOVE_LEFT = ['q']
    JUMP_KEY = ['Space']
    REST_KEY = 'c'
    REBUFF_KEY = 'r'
    STOP_KEY = 'Ctrl'

    NUM_BUFFS = 4
    MIN_SPELL_DELAY = 35 # /100 to get number of seconds
    MAX_SPELL_DELAY = 49 # /100 to get number of seconds

    JUMP_PROBABILITY = 50 # in %`1`
    REST_TIME = 15 # in seconds
    REST_THRESHOLD = 1000 # in number of mobs killed

    def __init__(self):
        Bot.__init__(self)
        self.name = "mage_bot"
        self.killed_mobs = 0
        self.total_killed = 0
        print("Created {}".format(self.name))

    def rebuff(self):
        for i in range(MageBot.NUM_BUFFS):
            sleep(2)
            kb.press(MageBot.REBUFF_KEY)
            sleep(self.get_random_delay())
            kb.release(MageBot.REBUFF_KEY)

    def get_random_delay(self):
        return randint(MageBot.MIN_SPELL_DELAY, MageBot.MAX_SPELL_DELAY) / 100.0

    def press(self, k):
        kb.press(k)
        sleep(self.get_random_delay())
        kb.release(k)
        sleep(self.get_random_delay())
    
    def press_list(self, kl):
        for k in kl:
            kb.press(k)
        sleep(self.get_random_delay())
        
        for k in kl:
            kb.release(k)

        sleep(self.get_random_delay())

    """
    Should write an heuristic for selecting next monster
    At this moment just auto the closest one
    """
    def select_next_monster(self):
        self.press("F1")
        
        #move = choice(['q', 'e', 'w', 's'])
        #self.press(move)
        
        self.press(MageBot.AA_KEY)

    def magic_arrow(self):
        self.press_list([MageBot.JUMP_KEY, MageBot.SPELLS['arrow']])
        #self.press(MageBot.SPELLS['arrow'])
    """
    Should write an heuristic for using more spells.
    At this moment it is just MagicArrow.
    """
    def attack(self):
        num_attacks = randint(MageBot.MIN_ATTACKS, MageBot.MAX_ATTACKS)
        #print("Attacking {} times".format(num_attacks))

        for i in range(num_attacks):
            # jump with a givenprobabilityw
            if randint(0, 100) < MageBot.JUMP_PROBABILITY:
                kb.press_and_release(MageBot.JUMP_KEY)

            self.magic_arrow()

            delay = self.get_random_delay()
            #print("Wait {} until next attack".format(delay))
            #sleep(delay)
        self.killed_mobs += 1

    def rest(self):
        # make sure you finish killing last monster but do not select another one
        self.attack()

        # sit then press forward to get up
        kb.press_and_release(MageBot.REST_KEY)
        sleep(MageBot.REST_TIME)
        kb.press_and_release(MageBot.FW_KEY)

    def main_loop(self):
        print("Waiting {} key to start. Stop using the same key".format(MageBot.STOP_KEY))
        kb.wait(MageBot.STOP_KEY)

        for i in range(2):
            print("Starting in {} sec...".format(2 - i))
            sleep(1)

        #self.rebuff()

        self.killed_mobs = 0
        while True:
            # exit key
            if kb.is_pressed(MageBot.STOP_KEY):
                print("Killed ~ {} mobs".format(self.total_killed + self.killed_mobs))
                break

            self.select_next_monster()
            self.attack()

            if self.killed_mobs == MageBot.REST_THRESHOLD:
                self.rest()
                self.total_killed += self.killed_mobs
                self.killed_mobs = 0
