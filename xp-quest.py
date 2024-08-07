import pyautogui
import pydirectinput as pdi
import keyboard as kb
from time import sleep

STOP_KEY = 'Ctrl'

print("Waiting {} key to start. Stop using the same key".format(STOP_KEY))
kb.wait(STOP_KEY)

def left_click():
    pdi.click()
    sleep(0.2)
    pdi.mouseUp()

def right_click():
    pdi.rightClick(duration=1)
    sleep(0.2)
    pdi.mouseUp(button='secondary')

def take_quests():
    # 1
    pdi.moveTo(350, 450, duration = 0.1)
    right_click()
    sleep(0.5)
    
    pdi.moveTo(1440, 940, duration = 0.1)
    left_click()
    sleep(0.5)
    
    # 2
    pdi.moveTo(400, 450, duration = 0.1)
    right_click()
    sleep(0.5)
    
    pdi.moveTo(1440, 940, duration = 0.1)
    left_click()
    sleep(0.5)
    
    # 3
    pdi.moveTo(440, 450, duration = 0.1)
    right_click()
    sleep(0.5)
    
    pdi.moveTo(1440, 940, duration = 0.1)
    left_click()
    sleep(0.5)
    
    # 4
    pdi.moveTo(480, 450, duration = 0.1)
    right_click()
    sleep(0.5)
    
    pdi.moveTo(1440, 940, duration = 0.1)
    left_click()
    sleep(0.5)


def quest_finish_accept():
    pdi.moveTo(1440, 940, duration = 0.1)
    sleep(0.2)
    left_click()

def loop():
    while(True):
        sleep(1)

        if kb.is_pressed(STOP_KEY):
            break

        take_quests()

loop()