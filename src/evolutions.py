
# This script contains functions realted to the evolutionary aspect; ie .
# creation of genomes, populations, evaluation, recombination, mutation, selection

from itertools import combinations
import scipy.stats as stats
import numpy as np
from random import sample, random, uniform, seed




def create_genome(n_genes):
    '''
    param: n_genes: integer number of genes 

    out: genome: list of genes with [key, duration] pairs
    '''

    keys = ['q','w','o','p'] # possible keys
    combs = [''.join(i) for n in range(1,5) for i in combinations(keys,n)]
    
    genome = [None] * n_genes

    for gene in range(n_genes):
        
        keys = ''.join(sample(combs,1)) 
        duration = round(random()*2,5)
        
        genome[gene] = [keys, duration]

    return genome


def create_population(N,n_genes):
    '''
    param: N: integer numper of individuals
    
    param: n_genes: integer number of genes 
    out: Population (Genepool)
    '''
    return [create_genome(n_genes) for _ in range(N)] 


### Parent selection 
## Rank based:

def select_top_N(population,fitness,N):
    # rank fitness list
    rank = stats.rankdata(fitness)
    # zip , sort based on rank and return 0 index
    pop_ranked = [ _[0] for _ in  sorted(list(zip(population,rank)),key = lambda x: -x[1])]
    fit_ranked = [ _[0] for _ in  sorted(list(zip(fitness,rank)),key = lambda x: -x[1])]
    return fit_ranked[:N], pop_ranked[:N] 

# I use Leventhein here as an distance metric since it incorporates 
# the order of the actions; set based dinstances ie Jaccard/manhattan/humming
# don't


def levenshtein_distance(genome1, genome2, concat = True):

    # pull actions
    keys1 = [_[0] for _ in genome1]
    keys2 = [_[0] for _ in genome2]
    
    if concat:
        keys1 = ''.join(keys1)
        keys2 = ''.join(keys2)


    l1, l2 = len(keys1)+1, len(keys2)+1
    
    # Create a 2D matrix to store the distances
    dist = [[0] * (l2) for _ in range(l1)]

    #  dist matrix first row / colum = strings / lists
    for i in range(l1):
        dist[i][0] = i
    for j in range(l2):
        dist[0][j] = j
    
    # penalties
    for i in range(1, l1):
        for j in range(1, l2):
            if keys1[i - 1] == keys2[j - 1]:
                cost = 0
            else:
                cost = 1
            dist[i][j] = min(
                dist[i - 1][j] + 1,  # Del
                dist[i][j - 1] + 1,  # Ins
                dist[i - 1][j - 1] + cost,  # Sub
            )

    return dist[l1-1][l2-1]

def min_distances(Genomes, concat = True):

    # get similarty scores lievenstein distace between them

    distsMat = np.empty((len(Genomes),len(Genomes)))
    distsMat[np.tril_indices_from(distsMat)] = np.inf

    for i,genome in enumerate(Genomes):
        distsMat[i,i:] = [levenshtein_distance(genome,g2, concat) for g2 in Genomes[i:]]
        
    
    return np.argmin(distsMat,axis=1)


### Recombination

def meiose(genome):
    size = len(genome)
    indices = range(size)
    sel = sorted(sample(indices,int(size/2)//1))
    return [genome[i] for i in sel]


# Note sample fucntion reshuffles,
# thus i should say for gene in genome....
def recombine_genomes(genome1,genome2,shuffle=False):

    if shuffle:
        return sample(genome1+genome2,len(genome1))
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
    return recombine_genomes(genome,mutated)



def mutate_genome_pauses(genome, time = .1):
   
    for gene in genome: 
        
        gene[1] = max(0,gene[1] + round(uniform(-time,time),5)) 

    return genome

def σ(scores):
    '''
    param: scores: vector of float score values of trial
    return: sigma scaled fitness
    '''
    scaled = np.maximum(scores - (np.mean(scores) - 2 * np.std(scores)),0)
    return scaled.tolist()


