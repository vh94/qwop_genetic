from itertools import combinations
from random import sample, random
#from selenium.webdriver.common.action_chains import ActionChains

keys = ['q','w','o','p']
combs = [''.join(i) for n in range(1,5) for i in combinations(keys,n)]


def create_Genome(n_genes):
    
    genome = [None]*n_genes

    for gene in range(n_genes):

        action = ''.join(sample(('up','down'),1))
        keypress = ''.join(sample(combs,1))
        duration = round(random(),5)

        genome[gene] =  [action,keypress,duration]
   
    return genome


