import sys ; sys.path.insert(0, 'src')
import argparse
from selenium.webdriver.common.action_chains import ActionChains
from src.gamecontrols import *
from src.evolutions import *

def main(args):

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
        fitness = Trials(
            Population,
            Pop_ID = Pop_id,
            Gen_ID = Generation,
            n_trials = n_trials,
            N_generations= N_generations,
            write = True)

        ### rank based parent Selection Top N Genomes .
        fit_μ, μ = select_top_N(Population, fitness, top_N)
        ## offspring
        λ = []
        
        # New Pop = mutation of timings of top genomes .. 
        # Population = [mutate_genome_pauses(genome) for genome in TopN]

        ### + Recombination ...
        # get similarty scores lievenstein distace between top genomes
        min_indices = min_distances(μ)
        # recombine_genomes:
        for i,j in enumerate(min_indices):
            # λ offspring duplicates genome size:
            for _ in range(2): # 2 offspring
                λ += [ recombine_genomes(μ[i]+μ[i],μ[j]+μ[j])]
        
        # mutated offspring
        λ += [mutate_genome(genome, 0.3) for genome in λ]
            #Population += [ mutate_genome(TopN[i],0.5) ] 
        # evaluate offspring
        fit_λ = Trials(
            λ,
            Pop_ID="λ",
            Gen_ID=Generation,
            n_trials=n_trials,
            N_generations=N_generations)
        # next gen: best of parents vs offspring
        Population = select_top_N( μ+λ, fit_μ+fit_λ, top_N )[1]
        # + pauses tweak:
        Population += [mutate_genome_pauses(genome) for genome in Population]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="QWOP evoultionary algo params:")

    parser.add_argument('--pop', type=int, default=300, help='Population size')
    parser.add_argument('--genes', type=int, default=3, help='Number of genes')
    parser.add_argument('--gen', type=int, default=10, help='Number of generations')
    parser.add_argument('--id', type=str, default='A', help='Population ID')
    parser.add_argument('--trials', type=int, default=1, help='Number of trials')
    parser.add_argument('--top', type=int, default=15, help='Top N')
    parser.add_argument('--seed', type=int, default=121, help='Seed number')

    args = parser.parse_args()

    # right click to initialize game:
    ActionChains(driver).click(game_canvas).perform()
    # execute main function:    
    main(args)
    # Close the browser window when done
    driver.quit()

