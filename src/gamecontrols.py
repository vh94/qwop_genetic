# This file contains game control fucntions:



def restart_game(driver):

    ActionChains(driver)\
        .key_up('q')\
        .key_up('w')\
        .key_up('o')\
        .key_up('p')\
        .send_keys('r')\
        .perform()
    
    pass

