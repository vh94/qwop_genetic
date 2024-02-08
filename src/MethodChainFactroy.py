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


def restart_game(driver):

    ActionChains(driver)\
        .key_up('q')\
        .key_up('w')\
        .key_up('o')\
        .key_up('p')\
        .send_keys('r')\
        .perform()
    
    pass


def read_score(Individual_ID,trial,game_canvas):
    ## OCR of score ##
    # capture image:
    game_canvas.screenshot(f'./data/img/{Individual_ID}_{trial}.png') # write to data/img

    # IMPROVE: not read and write image but access from ram, ie:
    # snap = game_canvas.screenshot_as_png 

    # clean the image 
    img = Image.open(f'./data/img/{Individual_ID}_{trial}.png')
    roi = (240, 20, 295, 55) # (l,t,r,b) COULD BUG if double digit, cant test because qwop too hard ...
    img_cropped = img.crop(roi)
    img_bw = ImageOps.grayscale(img_cropped)
    img_in = ImageOps.invert(img_bw)

    # extract & store score as float
    score = pytesseract.image_to_string(img_in,config=tess_conf)
    score = float(score.replace('\n',''))
    # print("score is:",score)
    # save cropped image for qc
    img_in.save(f'./data/img/{Individual_ID}_{trial}_cropped.png')

    return score

