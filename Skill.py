import keyboard as kb
from time import sleep, time
from random import randint
from Constants import Constants

class Skill():
    def __init__(self, name = '', description = '', cooldown = 0,
                 key = '', expires = 0, sk_type = 'U') -> None:
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.key = key
        self.expires = expires
        self.sk_type = sk_type
        self._time = 0

    def use(self):
        self._time = time()
        kb.press_and_release(self.key)
        print(f"\t* used {self.description} on '{self.key}'")
        delay = randint(Constants.MIN_SPELL_DELAY,
                        Constants.MAX_SPELL_DELAY) / Constants.RESOLUTION
        sleep(delay)

    def expired(self):
        if time() - self._time > self.expires:
            return True
        return False

