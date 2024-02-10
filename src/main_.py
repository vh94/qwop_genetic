import sys
sys.path.append('./src/')
import numpy as np
from evolutions import *
from gamecontrols import * # sets up browser etc
### Inizialization done !

####### Gameplay logic ##################

# right click to initialize game:
ActionChains(driver).click(game_canvas).perform()
Population = create_population(N = 20,n_genes = 25)
# run Trials
fitness = Trials(
    Population,
    Pop_ID = 'A',
    Gen_ID = '1',
    n_trials = 3,
    game_duration = 3,
    write = False
)

## Selection
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
