def MethodChainFactory(genome):
    '''
    Input: genome:listof elem [action,argument]
            - 'action': list of instructions as character
            - 'argument' : list of arguments (one per instruction)
    Output: chained function constructor arg object of type selenium.ActionChains
    '''
    def MethodChain(object):

        for gene in genome:
            fun = getattr(type(object),gene[0])

            object = fun(object,gene[1])
        return object

    return MethodChain


def GeneChain(genome,actions):
    '''
    Input: genome:listof elem [action,argument]
            - 'action': list of instructions as character
            - 'argument' : list of arguments (one per instruction)
    Output: chained function constructor arg object of type selenium.ActionChains
    '''
    for gene in genome:
        fun = getattr(type(actions),gene[0])
        # note: key_down and key_up only accept single keys as input
        if gene[0] != 'pause':
            for key in gene[1]:
                actions = fun(actions,key)
        else:
            actions = fun(actions,gene[1])

    return actions
