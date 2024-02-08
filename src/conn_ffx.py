import sys
sys.path.append('./src/')
#from selenium.webdriver.common.actions import action_builder
#import pytesseract
from time import sleep
from statistics import mean, median
#from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from MethodChainFactroy import *
from gamecontrols import *
from CreateGenome import *




# Spawn Firefox WebDriver 
driver = webdriver.Firefox()

# access QWOP url:
driver.get("http://www.foddy.net/Athletics.html")
# target game canvas
game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')


### Inizialization done !


## Gameplay logic ##
Population_id = 'A'
Generation_id = '1'
N = 50 # number of Individuals / population size
n_genes = 25 # number of Genes / genome size
n_trials = 3 # number of game trial per Individual
game_duration = 3 # time in seconds per game 


Population = create_population(N,n_genes)
scores = []
# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()
for i,Individual in enumerate(Population):

    Individual_ID = f'{Population_id}_{Generation_id}_{i}'
    # key_presses = GeneChain(Individual,ActionChains(driver))
    score = []
    # run!
    for trial in range(n_trials):
        #key_presses.perform()
        GeneChain(Individual,ActionChains(driver)).perform()
        sleep(game_duration)

        score.append(read_score(Individual_ID,trial,game_canvas))
        restart_game(driver)
    scores.append([ f(score) for f in [min,mean,median,max] ])
    print(i,scores[i])

# Close the browser window when done
driver.quit()
