import sys

from selenium.webdriver.common.actions import action_builder
sys.path.append('./src/')
import pytesseract
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from MethodChainFactroy import MethodChainFactory, GeneChain
from CreateGenome import create_Genome
# Spawn Firefox WebDriver 
driver = webdriver.Firefox()

# access QWOP url:
driver.get("http://www.foddy.net/Athletics.html")

# target game canvas
game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')

## Gameplay logic ##
# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()

# Spacebar or r to restart
ActionChains(driver)\
    .key_up('q')\
    .key_up('w')\
    .key_up('o')\
    .key_up('p')\
    .send_keys('r')\
    .perform()


## create a genome

genome = create_Genome(30)

# perform the genome
GeneChain(genome,ActionChains(driver)).perform()




## OCR of score ##

# capture image:
game_canvas.screenshot('./data/img/foo.png') # write to data/img

# IMPROVE: not read and write image but access from ram, ie:
# snap = game_canvas.screenshot_as_png 

# Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator='''

# clean the image 
img = Image.open('./data/img/foo.png')
roi = (240, 20, 295, 55) # (l,t,r,b) COULD BUG if double digit score might never happen and cant test, because qwop too hard ...
img_cropped = img.crop(roi)
img_bw = ImageOps.grayscale(img_cropped)
img_in = ImageOps.invert(img_bw)

# extract & store score as float
score = pytesseract.image_to_string(img_in,config=tess_conf)
score = float(score.replace('\n',''))
print("score is:",score)
# save cropped image for qc
img_in.save('QWOP/data/img/foo_cropped_in.png')









# Close the browser window when done
driver.quit()
