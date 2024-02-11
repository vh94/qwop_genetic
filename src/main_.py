import sys
sys.path.append('./src/')
import numpy as np
from evolutions import *
from gamecontrols import * # sets up browser etc
### Inizialization done !

####### Gameplay logic ##################
# Initial Random population
seed(1234)
Population = create_population(N = 200,n_genes = 20)
# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()
 
for Generation in range(10):
    print(f'-----\nTraining Gen: {Generation}; N:{len(Population)} \n -----')
    # run Trials
    fitness = Trials(
        Population,
        Pop_ID = 'A',
        Gen_ID = Generation,
        n_trials = min(5,(1 + Generation)),
        game_duration = min(15, (1 + Generation)),
        write = True
)
    print(f'Fitness: \n -----\nHighest: {max(fitness)}\nAvg: {mean(fitness)}')
    ## Selection
    TopTen = select_top_N(Population,fitness,35 - (Generation*2))

    ### Recombination
    # get similarty scores lievenstein distace between them
    # and store in matrix

    distsMat = np.empty((len(TopTen),len(TopTen)))

    for i,genome in enumerate(TopTen):
        distsMat[i,i:] = [levenshtein_distance(genome,g2) for g2 in TopTen[i:]]
        
    distsMat[np.tril_indices_from(distsMat)] = np.inf
    # maybe add more min_indices
    min_indices = np.argmin(distsMat,axis=1)[:int((len(TopTen)/2)//1) ]

    # recombine_genomes

    Population = [mutate_genome_pauses(genome) for genome in TopTen]

    for i,j in enumerate(min_indices):

        Population += [ recombine_genomes(TopTen[i],TopTen[j]) ]
        Population += [ recombine_genomes(TopTen[i],TopTen[j]) ]
        Population += [ mutate_genome(TopTen[i],0.5) ] 
        Population += [ mutate_genome_pauses(TopTen[i]) ] 


# Close the browser window when done
driver.quit()
