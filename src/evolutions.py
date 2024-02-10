
# This script contains functions realted to the evolutionary aspect; ie .
# creation of genomes, populations, evaluation, recombination, mutation, selection

from itertools import combinations
# from os import sendfile
import scipy.stats as stats
from random import sample, random
#from selenium.webdriver.common.action_chains import ActionChains

keys = ['q','w','o','p'] # possible keys
# combs = chords / single keys
combs = [''.join(i) for n in range(1,5) for i in combinations(keys,n)]


def create_genome(n_genes):
    
    genome = [None]*n_genes

    for gene in range(n_genes):

        action = ''.join(sample(('key_up','key_down','pause'),1))
        
        if action == 'pause':
            argument = round(random(),5) # pause length [0,1] sec
        else:
        	argument = ''.join(sample(combs,1)) # select keycomb
		
        genome[gene] = [action,argument]
   
    return genome

def create_population(N,n_genes):
    return [create_genome(n_genes) for i in range(N)] 



def select_top_N(population,fitness,N):
    # rank fitness list
    rank = stats.rankdata(fitness)
    # zip , sort based on rank and return 0 index
    pop_ranked = [ _[0] for _ in  sorted(list(zip(population,rank)),key = lambda x: x[1])]
    return pop_ranked[:N] 

# I use Leventhein here as an distance metric since it incorporates 
# the order of the actions; set based dinstances ie Jaccard/manhattan/humming
# don't


def levenshtein_distance(genome1, genome2):
    # pull actions
    actions1 = [_[0] for _ in genome1]
    actions2 = [_[0] for _ in genome2]

    l1, l2 = len(actions1)+1, len(actions2)+1
    
    # Create a 2D matrix to store the distances
    dist = [[0] * (l2) for _ in range(l1)]

    #  dist matrix first row / colum = strings
    for i in range(l1):
        dist[i][0] = i
    for j in range(l2):
        dist[0][j] = j
    
    # penalties
    for i in range(1, l1):
        for j in range(1, l2):
            if actions1[i - 1] == actions2[j - 1]:
                cost = 0
            else:
                cost = 1
            dist[i][j] = min(
                dist[i - 1][j] + 1,  # Del
                dist[i][j - 1] + 1,  # Ins
                dist[i - 1][j - 1] + cost,  # Sub
            )

    return dist[l1-1][l2-1]




def meiose(genome):
    size = len(genome)
    indices = range(size)
    sel = sorted(sample(indices,int(size/2)//1))
    return [genome[i] for i in sel]


# Note sample fucntion reshuffles,
# thus i should say for gene in genome....
def recombine_genomes(genome1,genome2,n_genes,shuffle=False):

    if shuffle:
        return sample(genome1+genome2,n_genes)
    else:
        gamet1 = meiose(genome1)
        gamet2 = meiose(genome2)
        zygote = []
        for x in zip(gamet1,gamet2):
            for i in x:
                zygote.append(i)
        return zygote


def mutate_genome(genome,prob):
    # todo add modes: transposons, args only, duplications,
    # deletions 
    size = len(genome)
    mutated = create_genome(int((size*prob) // 1))
    return recombine_genomes(genome,mutated,size)







