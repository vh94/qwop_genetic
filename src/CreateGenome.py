from itertools import combinations
from random import sample, random
#from selenium.webdriver.common.action_chains import ActionChains

keys = ['q','w','o','p'] # possible keys
# combs = chords / single keys
combs = [''.join(i) for n in range(1,5) for i in combinations(keys,n)]


def create_Genome(n_genes):
    
    genome = [None]*n_genes

    for gene in range(n_genes):

        action = ''.join(sample(('key_up','key_down','pause'),1))
        
        if action == 'pause':
            argument = round(random(),5)
        else:
        	argument = ''.join(sample(combs,1))
		
        genome[gene] = [action,argument]
   
    return genome

def create_population(N,n_genes):
    return [create_Genome(n_genes) for i in range(N)] 


     

