# Genetic Algorithm to play QWOP - python Implemetation

## Goal:

Train an evoultionary Algortihm to play the browser based online Game 🏃 'QWOP' (Foddy).


## to know

When the computer goes into power save and turns off the screen, the OCR doesnt capture the screen. Therefore disable screen 'Screen blank' in the OS options. 

## Dependencies:

#### System Dependencies

 - mozilla-firefox (or chrome based browser)
 - tesseract OCR engine

#### Python Dependencies

All 🐍 - dependencies are listed in the conda environment file: 'environment.yml'

## Files

The src directory contains following files:

    - main_.py : contains the taining loop. Provide arguments such as inital Pupulation ID and -size, Genome size,
    - gamecontrols.py : contains functions providing browser setup, screencapture, and translation of Genomes to selenium key instructions
    - evoultions.py : contains functions providing the creation, selection, mutation and recombination of Genomes


After specification of the parameters in the main- script, a random inital population is created and the trials begin.

A single trial for one run of one individual consists of following steps:

    - reset game ( release all pressed keys and send the 'r' key to reset the game )
    - translate the genetic information of the individual to selenium instructions and send them to the browser
    - sleep step which limits the duration of a trial run.
    - capture the image form the game canvas, read the meters run and deterine if the player fell.
    - calculate the score for the run from those values and append them to a vector for the current Individuum

From the vector of scores of runs of a individuum, the average, median, minumum and maximum score is calcualted and captured in a csv,
together with the Pupulation, Generation and Indiduums information.

The maximum score of the Individum is then appended to a fitness vector to compare the performace of the individuums.





