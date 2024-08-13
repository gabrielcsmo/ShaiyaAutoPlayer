from Bot import Bot
import keyboard as kb
from time import sleep
from random import randint
from time import time
from ImageProcessing import ImgProcessor
from Skill import Skill
from Constants import Constants

class FighterBot(Bot):

    MIN_ATTACKS = 3
    MAX_ATTACKS = 5

    SPELLS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    AA_KEY = ['0']
    FW_KEY = ['w']
    BW_KEY = ['s']
    RIGHT_KEY = ['d']
    LEFT_KEY = ['a']
    MOVE_RIGHT = ['e']
    MOVE_LEFT = ['q']
    JUMP_KEY = ['Space']
    REST_KEY = 'c'
    REBUFF_KEY = 'r'

    NUM_BUFFS = 5

    JUMP_PROBABILITY = -1 # in %
    REST_TIME = 15 # in seconds
    REBUFF = 50 # in number of mobs killed
    POINTS_THRESHOLD = 45 # in %    

    def __init__(self, resolution=(1920, 1080), skills_csv=""):
        Bot.__init__(self)
        self.name = "Fighter Bot"
        
        print("Creating {}".format(self.name))
        
        self.skills = []
        self.buffs = []

        self.read_skills(skills_csv)
        #exit(0)
        self.killed_mobs = 0
        self.total_killed = 0
        self.resolution = resolution
        self.screen_hdl = ImgProcessor(resolution)
        self.hp = 100
        self.mp = 100
        self.sp = 100
        self.pot_type = 0
        self.pots = ['x', 'z']
        print("Successfully created {}".format(self.name))

    def read_skills(self, csv):
        """
            paramenter: csv that describes the skills parameters for
            the bot. Header: 'skill,description,cooldown,key,expires,type'

            It will populate skills and buffs lists.
        """
        with open(csv, 'r') as f:
            lines = f.readlines()
            for l in lines:
                tokens = l.strip().split(',')
                try:
                    skill = Skill(tokens[0],
                                  tokens[1],
                                  int(tokens[2]),
                                  tokens[3],
                                  int(tokens[4]),
                                  tokens[5])
                    if skill.sk_type == Constants.BUFF_T:
                        self.buffs.append(skill)
                    else:
                        self.skills.append(skill)
                except Exception as e:
                    #print(f"Failed to read skill from csv: {e}")
                    pass
        print(f"- Read a total of {len(self.skills)} skills and {len(self.buffs)} buffs.")
    
    def pot(self):
        if self.hp < FighterBot.POINTS_THRESHOLD:
            kb.press_and_release(self.pots[self.pot_type % 2])
            print("HP {}% - poting".format(self.hp))
            self.pot_type += 1
            sleep(0.5)
        if self.sp < FighterBot.POINTS_THRESHOLD:
            print("SP {}% or MP {}% - poting".format(self.sp, self.mp))
            kb.press_and_release("z")
            sleep(0.5)

    def rand_sleep(self):
        delay = randint(Constants.MIN_SPELL_DELAY,
                        Constants.MAX_SPELL_DELAY) / Constants.RESOLUTION
        sleep(delay)

    def rebuff(self):
        for buff in self.buffs:
            if buff.expired():
                buff.use()

    """
    Should write an heuristic for selecting next monster
    At this moment just auto the closest one
    """
    def select_next_monster(self):
        kb.press_and_release(Constants.NEXT_MOB_KEY)
        self.rand_sleep()

    """
    Should write an heuristic for using more spells.
    At this moment it is just MagicArrow.
    """
    def attack(self):
        auto_attack = self.skills[0]

        for sk in self.skills:
            if sk.name == 'AA':
                auto_attack = sk
            break
    
        auto_attack.use()

        """
        num_attacks = randint(FighterBot.MIN_ATTACKS, FighterBot.MAX_ATTACKS)
        #print("Attacking {} times".format(num_attacks))
        print("[{0:.2f}] Monster {1}.".format(self.current_time, self.killed_mobs))
        for i in xrange(num_attacks):
            # jump with a givenprobability
            #if randint(0, 100) < FighterBot.JUMP_PROBABILITY:
            #    kb.press_and_release(FighterBot.J1UMP_KEY)

            if i == 0:
                kb.press_and_release(FighterBot.SPELLS[0])
            elif i == 1:
                kb.press_and_release(FighterBot.SPELLS[1])
            elif i == 2:
                kb.press_and_release(FighterBot.SPELLS[2])
            else:
                kb.press_and_release(FighterBot.SPELLS[3])
            
            delay = randint(FighterBot.MIN_SPELL_DELAY, FighterBot.MAX_SPELL_DELAY) / 100.0
            #print("Wait {} until next attack".format(delay))
            sleep(delay)
        self.killed_mobs += 1
        """

    def rest(self):
        # make sure you finish killing last monster but do not select another one
        self.attack()

        # sit then press forward to get up
        kb.press_and_release(FighterBot.REST_KEY)
        sleep(FighterBot.REST_TIME)
        kb.press_and_release(FighterBot.FW_KEY)

    def update_status(self):
        self.screen_hdl.get_resources_status()
        self.screen_hdl.display_frame()
        self.hp = self.screen_hdl.get_res("HP", "1")
        self.mp = self.screen_hdl.get_res("MP", "1")
        self.sp = self.screen_hdl.get_res("SP", "1")

    def main_loop(self):
        print(f"Waiting {Constants.STOP_KEY} key to start. Stop it using the same key")
        kb.wait(Constants.STOP_KEY)
        sleep(1)
        while True:
            self.rand_sleep()

            if kb.is_pressed(Constants.STOP_KEY):
                print("Successfully stopped.")
                break
            self.update_status()

            self.rebuff()
            
            self.select_next_monster()

            self.attack()
        exit(0)
    
        """
        self.start_time = time()
        self.current_time = 0
        print(self.start_time)
        pots = ['z', 'x']
        sleep(2)

        self.killed_mobs = 0
        while True:
            self.current_time = time() - self.start_time
            # exit key
            if kb.is_pressed(FighterBot.STOP_KEY):
                print("Killed ~ {} mobs".format(self.total_killed + self.killed_mobs))
                break

            if self.current_time > 800:
                self.rebuff()
                self.current_time = 0

            # get HP, SP, MP
            self.update_status()

            # pot if necessary
            self.pot()

            self.select_next_monster()
            self.attack()
        """