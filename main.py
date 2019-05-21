from MageBot import MageBot
from FighterBot import FighterBot
from ImageProcessing import ImgProcessor

if __name__ == '__main__':
    #bot = MageBot()
    #bot = FighterBot()
    #bot.main_loop()
    img_proc = ImgProcessor((1920,1080))
    img_proc.display_frame()
    #frame = img_proc.grab_frame()
    #print(len(frame[0][0]))
