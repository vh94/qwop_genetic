# This file contains game control fucntions:
import pytesseract
from PIL import Image, ImageOps
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime
import csv
from statistics import mean, median
from config import *
############## Functions ##################

def restart_game(driver):
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


def GeneChain(genome,driver):
    '''
    Input: genome:listof elem [action,argument]
            - 'action': list of instructions as character
            - 'argument' : list of arguments (one per instruction)
    Output: chained function constructor arg object of type selenium.ActionChains
    '''
    chain = ActionChains(driver)
    for gene in genome:
        fun = getattr(type(chain),gene[0])
        # note: key_down and key_up only accept single keys as input
        if gene[0] != 'pause':
            for key in gene[1]:
                chain = fun(chain,key)
        else:
            chain = fun(chain,gene[1])

    return chain


def read_score(Individual_ID,trial,game_canvas,Pop_ID):
    '''
    Reads the score (distance in M) of an Individual run using tesseract OCR.
    Saves image to data/img/directory for inspection.
    returns the score as a float.
    '''
    #global game_canvas
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



def Trials(Population, Pop_ID, Gen_ID,driver,game_canvas,n_trials,game_duration,N_generations,write=False):
    # Iterate over Population:
    #global N_generations
    
    for i,Genome in enumerate(Population):
        
        if not i: print('\n\n'); fitness = [0] # edge case for printing--:
        print(f'\x1B[2A Gen: {Gen_ID}/{N_generations - 1}; Fitness: max {max(fitness):.2f}, avg {mean(fitness):.2f} \x1B[B\n',end='\r')
        # concatenate ID of individual 
        Individual_ID = f'{Pop_ID}_{Gen_ID}_{i}'
        score = [] # list to store meters 
        # run n number of trials!
        for trial in range(n_trials):
            restart_game(driver)
            # Perform the steps , ie gene expression -> pheno 
            GeneChain(Genome,driver).perform()
            # Pause to limit trial duration
            sleep(game_duration)
            # read the score from game canvas and append to score list
            s = read_score(Individual_ID,trial,game_canvas,Pop_ID)
            print(f'\x1B[A N: {i}/{len(Population)-1}; trial {trial}/{n_trials-1};  score {s:.1f}   \n',end='\r')
            score.append(s)
            # next trial -->

        # append maximal reached score to fitness list
        if not i: fitness = [] 
        fitness.append(max(score))

        # parse data to write to logging csv column
        data = [datetime.now().strftime('%m-%d-%H-%M-%S'),
                game_duration,
                Individual_ID]\
                + [ round(f(score),5) for f in [min,mean,median,max]]
        
        if write:
            # write to csv file
            with open(f'./data/fitness_{Pop_ID}.csv','a',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)

        #print(data) # print to stdout

    return fitness

