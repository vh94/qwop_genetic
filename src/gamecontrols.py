# This file contains game control fucntions:

import pytesseract
from PIL import Image, ImageOps
from selenium.webdriver.common.action_chains import ActionChains


# Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator=''' 



def restart_game(driver):

    ActionChains(driver)\
        .key_up('q')\
        .key_up('w')\
        .key_up('o')\
        .key_up('p')\
        .send_keys('r')\
        .perform()
    
    pass

def read_score(Individual_ID,trial,game_canvas):
    ## OCR of score ##
    # capture image:
    game_canvas.screenshot(f'./data/img/{Individual_ID}_{trial}.png') # write to data/img

    # IMPROVE: not read and write image but access from ram, ie:
    # snap = game_canvas.screenshot_as_png 

    # clean the image 
    img = Image.open(f'./data/img/{Individual_ID}_{trial}.png')
    roi = (240, 20, 295, 55) # (l,t,r,b) COULD BUG if double digit, cant test because qwop too hard ...
    img_cropped = img.crop(roi)
    img_bw = ImageOps.grayscale(img_cropped)
    img_in = ImageOps.invert(img_bw)

    img_in.save(f'./data/img/{Individual_ID}_{trial}_cropped.png')
    # extract & store score as float
    try:
        score = pytesseract.image_to_string(img_in,config=tess_conf)
        score = float(score.replace('\n',''))
    except:
        score = 0
        print("score couldn't be read, setting 0")
    # print("score is:",score)
    # save cropped image for qc

    return score



