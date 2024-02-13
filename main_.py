import sys ; sys.path.insert(0, 'src')
import argparse
import src
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from src import evolutions, gamecontrols, config
from config import *
from gamecontrols import *
from evolutions import *

def main(driver,game_canvas, args):

    Popsize = args.pop
    N_genes = args.genes
    N_generations = args.gen
    Pop_id = args.id
    n_trials = args.trials
    top_N = args.top
    seed_nr = args.seed
    

    # Initial Random population
    seed(seed_nr)
    Population = create_population(Popsize,N_genes)

    
    for Generation in range(N_generations):

        # run Trials Parents: μ
        fitness_μ = Trials(
            Population,
            Pop_ID = Pop_id,
            Gen_ID = Generation,
            driver= driver,
            game_canvas= game_canvas,
            n_trials = n_trials,
            N_generations= N_generations,
            write = True)

        ###  Selection Top N Genomes based rank.
        TopN = select_top_N(Population, fitness_μ, top_N)
        
        # New Pop = mutation of timings of top genomes .. 
        Population = [mutate_genome_pauses(genome) for genome in TopN]

        ### + Recombination ...
        # get similarty scores lievenstein distace between top genomes
        min_indices = min_distances(TopN)
        # recombine_genomes:
        for i,j in enumerate(min_indices):

            Population += [ recombine_genomes(TopN[i],TopN[j]) ]
            Population += [ mutate_genome(TopN[i],0.5) ] 




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="QWOP evoultionary algo params:")

    parser.add_argument('--pop', type=int, default=60, help='Population size')
    parser.add_argument('--genes', type=int, default=20, help='Number of genes')
    parser.add_argument('--gen', type=int, default=10, help='Number of generations')
    parser.add_argument('--id', type=str, default='A', help='Population ID')
    parser.add_argument('--trials', type=int, default=2, help='Number of trials')
    parser.add_argument('--top', type=int, default=10, help='Top N')
    parser.add_argument('--seed', type=int, default=1994, help='Seed number')

    args = parser.parse_args()
    # , , , , , , , top_N = args[1:]

    # Spawn Firefox WebDriver 
    driver = webdriver.Firefox()
    # access QWOP url:
    driver.get("http://www.foddy.net/Athletics.html"); sleep(3)
    # target game canvas
    game_canvas = driver.find_element(By.CSS_SELECTOR,'#window1')
    # right click to initialize game:
    ActionChains(driver).click(game_canvas).perform()
    # execute main function:    
    main(driver, game_canvas, args)
    # Close the browser window when done
    driver.quit()


