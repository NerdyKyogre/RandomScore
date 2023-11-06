'''
Algorithm to produce scores for machine learning factors based on randomly generated weights
Author: Amy Franchuk (github/NerdyKyogre)
Collaborators: Cam Franchuk
When: Nov 5 2023
'''
import random
import time

attempts = 0

def main():
    '''
    Main logic loop for random scoring
    Inputs: N/A
    Returns: N/A
    '''
    #constants for base weight and scoring values
    #edit these before running the script to change the values
    BASE_WEIGHTS = [30, 5, 5, 5, 20, 5, 15, 0, 15]
    BASE_SCORES = [
        [4.9922, 3, 2, 3, 5, 5, 3, 5, 5],
        [5, 4, 2, 5, 3, 3.1679, 2, 5, 5],
        [2.2066, 5, 4, 3, 5, 2.1374, 5, 3, 4.1379]
    ]
    BASE_VAL_ERROR = 10
    BASE_TOT_ERROR = 1
    
    #TODO: get these values from a config file or user input

    #initialize a dictionary to save the total scores for each option
    #using this instead of a list so we can get the key later
    totals = {}
    for i in range(len(BASE_SCORES)):
        totals[i] = 0
    #count randomizer attempts too
    global attempts

    #start timer
    print("Calculating... Please be patient, this may take a moment")
    startTime = time.time()

    #TODO: get length of this loop from input as well
    for i in range(1000):
        #roll some weights, then calculate
        totals[calculateWinner(BASE_SCORES, rollWeights(BASE_WEIGHTS, BASE_VAL_ERROR, BASE_TOT_ERROR))] += 1
    
    #stop timer and print results
    endTime = time.time()
    print("Finished!")
    #loop over totals for scores of any length of option set
    for i in range(len(totals)):
        print("Option " + str(i + 1) + " scored highest " + str(totals[i]) + " times.")
    print("The highest scoring option was option " + str((max(totals, key=totals.get)) + 1) + ".")
    print(str(attempts) + " sets of random weights were generated.")
    print("This calculation took " + "%.2f" % (endTime - startTime) + " seconds to run.")

    

def calculateWinner(options, weights):
    '''
    Calculates which scoring option has the highest score based on the provided weights
    Inputs: 
        - options: Base score options mapped to each factor, type 2D list
        - weights: List of weights for each score
    Returns: highest scoring option index, type int
    '''
    
    #initialize dictionary for score totals
    total = {}
    for i in range(len(options)):
        total[i] = 0

    #loop over factors of an arbitrary option set since they should all be the same length
    for i in range(len(options[0])):
        #now apply the weight to each scoring option and add the value to the total dictionary
        for j in range(len(total)):
            total[j] += options[j][i] * weights[i]

    return (max(total, key=total.get))

def rollWeights(baseVals, valError, totError):
    '''
    Randomizes weights of scoring within acceptable range
    Inputs: 
        - baseVals: starting weights for each score, type tuple
        - valError: percentage by which individual values can vary, type int
        - totError: percentage by which the total of the values can vary, type int
    Returns: Randomized score weights for each score option, type list
    '''
    #mark that we have attempted another weighting
    global attempts
    attempts += 1
    #create a list to return
    rolled = []
    #loop over each value in baseVals and randomize it within error range
    for value in baseVals:
        #append a random value based on the checked error
        rolled.append(random.uniform(max(value - valError, 0), value + valError))

    #calculate total and check that it is in acceptable range; if not, recurse
    total = sum(rolled)
    if (total < (100 - totError)) or (total > (100 + totError)):
        nextAttempt = rollWeights(baseVals, valError, totError)
        rolled = nextAttempt
    
    return rolled

main()