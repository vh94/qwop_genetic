import sys
sys.path.append('./src/')
from selenium.webdriver.common.actions import action_builder
import pytesseract
from time import sleep
from statistics import mean, median
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from MethodChainFactroy import *
from CreateGenome import create_Genome, create_population


# Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator=''' 

# Spawn Firefox WebDriver 
driver = webdriver.Firefox()

# access QWOP url:
driver.get("http://www.foddy.net/Athletics.html")
sleep(30)
# target game canvas
game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')

# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()

### Inizialization done !


## Gameplay logic ##
Population_id = 'A'
Generation_id = '1'
N = 10 # number of Individuals / population size
n_genes = 30 # number of Genes / genome size
n_trials = 10 # number of game trial per Individual
game_duration = 15 # time in seconds per game 


Population = create_population(N,n_genes)
scores = []
for i,Individual in enumerate(Population):

    Individual_ID = f'{Population_id}_{Generation_id}_{i}'
    key_presses = GeneChain(Individual,ActionChains(driver))
    score = []
    # run!
    for trial in range(n_trials):
        key_presses.perform()
        sleep(game_duration)
        score.append(read_score(Individual_ID,trial,game_canvas))
        restart_game(driver)
    scores[i] = [ f(score) for f in [min,mean,median,max] ]


# Close the browser window when done
driver.quit()
