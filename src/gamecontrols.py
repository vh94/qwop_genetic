# This file contains game control fucntions:
import pytesseract
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, clock
from datetime import datetime
import csv
from statistics import mean, median

## # Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator=''' 
# Spawn Firefox WebDriver 
driver = webdriver.Firefox()
# access QWOP url:
driver.get("http://www.foddy.net/Athletics.html"); sleep(3)
# target game canvas
game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')


############## Functions ##################

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
    chain = ActionChains(driver)

    down = getattr(type(chain),"key_down")
    up = getattr(type(chain),"key_up")
    pause = getattr(type(chain),"pause")
    
    for gene in genome:
        # note: key_down and key_up only accept single keys as input
        for key in gene[0]: chain = down(chain,key)
        # pause
        chain = pause(chain,gene[1])
        # key up 
        for key in gene[0]: chain = up(chain,key)
    return chain


def read_score(Individual_ID,trial,Pop_ID):
    '''
    Reads the score (distance in M) of an Individual run using tesseract OCR.
    Saves image to data/img/directory for inspection.
    returns the score as a float.
    '''
    #game_canvas.screenshot(f'./data/img/{Individual_ID}_{trial}.png') # write to data/img

    game_canvas.screenshot(f'./data/img/{Pop_ID}tmp.png') # write to data/img

    # IMPROVE: not read and write image but access from ram, ie:
    # snap = game_canvas.screenshot_as_png 

    # Preprocess the image crop:  (l,t,r,b) 
    #img = Image.open(f'./data/img/{Individual_ID}_{trial}.png')
    img = Image.open(f'./data/img/{Pop_ID}tmp.png')
    img_bw = ImageOps.grayscale(img)
    img_in = ImageOps.invert(img_bw)

    # save cropped image for qc
    #img_in.save(f'./data/img/{Individual_ID}_{trial}_cropped.png')
    try:
        # extract & store score as float
        score = pytesseract.image_to_string(img_in.crop((230, 20, 420, 55)),config=tess_conf)
        score = float(score.replace(' metres\n',''))
        if score <= 0.4: score = 0 # don't just stand there
    except:
        print("score couldn't be read, setting 0")
        score = 0
    
    try:
        participant = pytesseract.image_to_string(img_in.crop((200, 110, 430, 140)),config=tess_conf)
        if participant == 'PARTICIPANT\n':
            score = 0 # harsh penalty for falling
            #score -= 1.0
    except:
        print("could not determine if fell down")

    return score



def Trials(Population, Pop_ID, Gen_ID,  n_trials, N_generations, write=True):
    # Iterate over Population:
    avg_genome_size = mean([len(genome) for genome in Population])
    Score = [] # score for pop

    for i,Genome in enumerate(Population):
        
        score = [] # score for individual
        times = [] # store game durations

        if not i: print('\n\n'); Score = [0] # edge case for printing-- score = 0 for max / mean:
        print(f'\x1B[2A Gen: {Gen_ID}/{N_generations - 1}; Score: max {max(Score):.2f}, avg {mean(Score):.2f}; NGenes Ø:{avg_genome_size} \x1B[B\n',end='\r')
        # concatenate ID of individual 
        Individual_ID = f'{Pop_ID}_{Gen_ID}_{i}'
        
        # run n number of trials!
        for trial in range(n_trials):
            restart_game()

            t0 = clock()
            # Perform the steps , ie gene expression -> pheno 
            GeneChain(Genome).perform()
            # Pause 
            sleep(1.5)
            dt = clock() - t0
            # read the score from game canvas and append to score list
            s = read_score(Individual_ID,trial,Pop_ID)
            print(f'\x1B[A N: {i}/{len(Population)-1}; trial {trial}/{n_trials-1};  score {s:.1f}   \n',end='\r')
            score.append(s)
            times.append(dt)
            # next trial -->

        # append maximal reached score to Score list
        if not i: Score = [] 
        Score.append(max(score))
        
        # parse data to write to logging csv column
        data = [datetime.now().strftime('%m-%d-%H-%M-%S'),
                Individual_ID, mean(times)]\
                + [ round(f(score),5) for f in [min,mean,median,max]]
        
        if write:
            # write to csv file
            with open(f'./data/fitness_{Pop_ID}.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)


    return Score


