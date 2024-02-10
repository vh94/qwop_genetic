import sys
sys.path.append('./src/')
from datetime import datetime
import csv
from statistics import mean, median
import numpy as np
############### OWN MODULES 
from gamecontrols import * # sets up browser etc
from evolutions import *
### Inizialization done !

############################# Gameplay logic ##################################
Population_id = 'A'
Generation_id = '1'
N = 5 # number of Individuals / population size
n_genes = 25 # number of Genes / genome size
n_trials = 2 # number of game trial per Individual
game_duration = 3 # time in seconds per game 


Population = create_population(N,n_genes)
fitness = []
# perform the runs:
# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()


for i,Genome in enumerate(Population):
    
    # concatenate ID of individual 
    Individual_ID = f'{Population_id}_{Generation_id}_{i}'
    score = [] # list to store meters 
    # run!
    for trial in range(n_trials):
        restart_game()
        # Perform the steps , ie gene expression -> pheno 
        GeneChain(Genome).perform()
        # Pause to limit trial duration
        sleep(game_duration)
        # read the score from game canvas and append to score list
        score.append(read_score(Individual_ID,trial))
        # next trial
     
    # append maximal reached score to fitness list
    fitness.append(max(score))
    # parse data to write to logging csv column
    data = [datetime.now().strftime('%m-%d-%H-%M-%S'),
            game_duration,
            Individual_ID]\
            + [ f(score) for f in [min,mean,median,max]]
    
    # write to csv file
    with open('./data/fitness.csv','a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

    print(data) # print to stdout


### Selection
# rank based on fitness
# get the ten highest ranked Individuals 

TopTen = select_top_N(Population,fitness,10)

### Recombination
# get similarty scores lievenstein distace between them
# and store in matrix

distsMat = np.empty((len(TopTen),len(TopTen)))


for i,genome in enumerate(TopTen):
    distsMat[i,i:] = [levenshtein_distance(genome,g2) for g2 in TopTen[i:]]
    
distsMat
np.tril(distsMat)+1

# recombine_genomes



### Mutation


### Migration new Individuals

## next gen:

# top ten old gen + Offspring + Top 10 old gen mutated + Offspring mutated + rest : new Individuals

# Close the browser window when done
driver.quit()
