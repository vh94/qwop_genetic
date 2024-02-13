
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

###: Simulation Params :###
Popsize = 60
N_genes = 20
N_generations = 10
Pop_id = 'A'
n_trials = 2
game_duration = 1.5
top_N = 10
seed_nr = 1994

# Setup tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
tess_conf = '--psm 7 -c page_separator=''' 

