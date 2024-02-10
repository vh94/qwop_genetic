# This file contains game control fucntions:
import pytesseract
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator=''' 
# Spawn Firefox WebDriver 
driver = webdriver.Firefox()
# access QWOP url:
driver.get("http://www.foddy.net/Athletics.html")
# target game canvas
sleep(3)
game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')

### Functions
def restart_game():
    '''
    releases keypresses and restarts game
    '''
    ActionChains(driver)\
        .key_up('q')\
        .key_up('w')\
        .key_up('o')\
        .key_up('p')\
        .send_keys('r')\
        .perform()
    
    pass


def GeneChain(genome):
    '''
    Input: genome:listof elem [action,argument]
            - 'action': list of instructions as character
            - 'argument' : list of arguments (one per instruction)
    Output: chained function constructor arg object of type selenium.ActionChains
    '''
    for gene in genome:
        fun = getattr(type(ActionChains(driver)),gene[0])
        # note: key_down and key_up only accept single keys as input
        if gene[0] != 'pause':
            for key in gene[1]:
                actions = fun(actions,key)
        else:
            actions = fun(actions,gene[1])

    return actions


def read_score(Individual_ID,trial):
    '''
    Reads the score (distance in M) of an Individual run using tesseract OCR.
    Saves image to data/img/directory for inspection.
    returns the score as a float.
    '''
    #global game_canvas
    game_canvas.screenshot(f'./data/img/{Individual_ID}_{trial}.png') # write to data/img

    # IMPROVE: not read and write image but access from ram, ie:
    # snap = game_canvas.screenshot_as_png 

    # Preprocess the image 
    img = Image.open(f'./data/img/{Individual_ID}_{trial}.png')
    roi = (240, 20, 295, 55) # (l,t,r,b) COULD BUG if double digit, cant test because qwop too hard ...
    img_cropped = img.crop(roi)
    img_bw = ImageOps.grayscale(img_cropped)
    img_in = ImageOps.invert(img_bw)

    # save cropped image for qc
    img_in.save(f'./data/img/{Individual_ID}_{trial}_cropped.png')
    try:
        # extract & store score as float
        score = pytesseract.image_to_string(img_in,config=tess_conf)
        score = float(score.replace('\n',''))
    except:
        print("score couldn't be read, setting 0")
        score = 0

    return score



