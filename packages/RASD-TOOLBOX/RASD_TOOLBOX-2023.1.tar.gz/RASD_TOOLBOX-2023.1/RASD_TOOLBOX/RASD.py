import numpy as np
import pandas as pd
import json
import time
from datetime import datetime
from scipy.stats.distributions import norm
from scipy.stats.distributions import gumbel_r
from scipy.stats.distributions import gumbel_l
from scipy.stats.distributions import lognorm
from scipy.stats.distributions import uniform
from scipy.stats.distributions import triang

def PROGRESS_BAR(REP, TOTAL, PREFIX = 'Progress:', SUFFIX = 'Complete', DECIMALS = 1, LENGTH = 50, FILL = '█', PRINT_END = "\r"):
    """
    This function create terminal progress bar.
    
    Input:
    REP        | Current iteration (required)                     | Integer
    TOTAL      | Total iterations (required)                      | Integer
    PREFIX     | Prefix string                                    | String
    SUFFIX     | Suffix string                                    | String
    DECIMALS   | Positive number of decimals in percent complete  | Integer
    LENGTH     | Character length of bar                          | Integer
    FILL       | Bar fill character                               | String
    PRINT_END  | End character (e.g. "\r", "\r\n")                | String
    
    Output:
    N/A
    """
    
    # Progress bar
    PERCENT = ("{0:." + str(DECIMALS) + "f}").format(100 * (REP / float(TOTAL)))
    FILLED_LENGTH = int(LENGTH * REP // TOTAL)
    BAR = FILL * FILLED_LENGTH + '-' * (LENGTH - FILLED_LENGTH)
    print(f'\r{PREFIX} |{BAR}| {PERCENT}% {SUFFIX}', end = PRINT_END)
    
    # Print new line on complete
    if REP == TOTAL: 
        print()
    
    return

def SAMPLING(**kwargs):
    """ 
    This algorithm generates a set of random numbers according to a type distribution.

    See documentation in wmpjrufg.github.io/RASDPY/
    """
    if len(kwargs) != 4:
        raise ValueError("this fuction require four inputs!")

    # Creating variables
    N_POP = kwargs['N_POP']
    D = kwargs['D']
    MODEL = kwargs['MODEL']
    VARS = kwargs['VARS']
    RANDOM_SAMPLING = np.zeros((N_POP, D))
    
    # Monte Carlo sampling
    if MODEL.upper() == 'MCS':
        for I in range(D):
            # Type of distribution, mean and standard deviation
            TYPE = VARS[I][0].upper()
            MEAN = VARS[I][1]
            STD = VARS[I][2]
            # Normal or Gaussian
            if TYPE == 'GAUSSIAN' or TYPE == 'NORMAL':
                RANDOM_SAMPLING[:, I] = norm.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = None)
            # Gumbel right or Gumbel maximum
            elif TYPE == 'GUMBEL MAX':
                RANDOM_SAMPLING[:, I] = gumbel_r.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = None)
            # Gumbel left or Gumbel minimum
            elif TYPE == 'GUMBEL MIN':
                RANDOM_SAMPLING[:, I] = gumbel_l.rvs(loc = MEAN, scale = STD, size = N_POP, random_state = None)
            # Lognormal
            elif TYPE == 'LOGNORMAL':
                RANDOM_SAMPLING[:, I] = lognorm.rvs(s = STD, loc = MEAN, scale = np.exp(MEAN), size = N_POP)
            # Uniform
            elif TYPE == 'UNIFORM':
                RANDOM_SAMPLING[:, I] = uniform.rvs(loc = MEAN, scale=STD, size = N_POP, random_state = None)
            # Triangular
            elif TYPE == 'TRIANGULAR':
                LOC = VARS[I][1]
                SCALE = VARS[I][2]
                C = VARS[I][3]
                #loc is the start, scale is the base width, c is the mode percentage
                RANDOM_SAMPLING[:, I] = triang.rvs(loc = LOC, scale = SCALE, c = (C-LOC) / (SCALE-LOC), size = N_POP, random_state = None)

    return RANDOM_SAMPLING

def EVALUATION_MODEL(SAMPLE, OF_FUNCTION, NULL_DIC):
    R, S, G = OF_FUNCTION(SAMPLE, NULL_DIC)
    return R, S, G

def MCS_LHS_ALGORITHM(SETUP, OF_FUNCTION):
    """
    This function creates the samples and evaluates the limit state functions.
    
    See documentation in wmpjrufg.github.io/RASDPY/                     | 
    """
    # Initial setup
    INIT = time.time()
    # AQUI FAZER O KWARGS
    N_POP = SETUP['N_POP']
    N_G = SETUP['N_G']
    D = SETUP['D']
    MODEL = SETUP['MODEL']
    VARS = SETUP['VARS']
    NULL_DIC = SETUP['NULL_DIC']
    STEP = SETUP['STEP SAMPLE']
    RESULTS_R = np.zeros((N_POP, N_G))
    RESULTS_S = np.zeros((N_POP, N_G))
    RESULTS_G = np.zeros((N_POP, N_G))
    RESULTS_I = np.zeros((N_POP, N_G))  
    MODEL_NAME = 'MCS_LHS'
    # BETA_DF = RASD_CL.PROBABILITY_OF_FAILURE() - Vamos mudar esse calc aqui para uma derivada numérica vou pensar em como fazer
    
    # Creating samples   
    DATASET_X = SAMPLING(N_POP = N_POP, D = D, MODEL = MODEL, VARS = VARS)    
    
    # Evaluates Limit State functions with all samples
    for I in range(N_POP):
        SAMPLE = DATASET_X[I, :]
        # Model evaluation
        R, S, G = EVALUATION_MODEL(SAMPLE, OF_FUNCTION, NULL_DIC)
        for J in range(N_G):
            # Capacity
            RESULTS_R[I, J] = R[J]
            # Demand
            RESULTS_S[I, J] = S[J]
            # Limit State function
            RESULTS_G[I, J] = G[J]
            # Failure check (ideal condition Demand - Capacity <= 0)
            if G[J] <= 0: 
                K = 0
            elif G[J] > 0: 
                K = 1
            RESULTS_I[I, J] = int(K) 
        
        # Progress bar update
        time.sleep(0.01)
        PROGRESS_BAR(I + 1, N_POP)

    # Storage all results
    AUX = np.hstack((DATASET_X, RESULTS_R, RESULTS_S, RESULTS_G, RESULTS_I))
    RESULTS_RASD = pd.DataFrame(AUX)          
    
    # Rename columns in dataframe 
    COLUMNS_NAMES = []
    P_F = []
    N_F = []
    # BETA_F = []
    for L in range(D):
        COLUMNS_NAMES.append('X_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('R_' + str(L))  
    for L in range(N_G):
        COLUMNS_NAMES.append('S_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('G_' + str(L))
    for L in range(N_G):
        COLUMNS_NAMES.append('I_' + str(L))
    RESULTS_RASD.columns = COLUMNS_NAMES
    
    # Resume data
    VALUES = list(np.arange(1, N_POP, STEP, dtype = int))
    if VALUES[-1] != N_POP:
        VALUES.append(N_POP)
    VALUES = [int(X) for X in VALUES]
    for I in VALUES:
        LINES = RESULTS_RASD[:I]
        # Failure probability
        for L in range(N_G):
            INDEX = 'I_' + str(L)
            N_FAILURE = int(LINES[INDEX].sum())
            N_F.append(N_FAILURE)
            P_FVALUE = N_FAILURE / I
            P_F.append(P_FVALUE)

    # Resume process (Time and outputs)
    END = time.time()
    print(' Process Time: %.2f' % (END - INIT), 'Seconds', '\n', 'Seconds per sample: %.4f' % ((END - INIT) / N_POP))
    RESUME_DATA = {'Count the number of points G > 0': N_F, 'x': VALUES, 'probability of faliure': P_F}  
    NAME = MODEL_NAME + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S'))
    with open(NAME + '.json', 'w') as FILE:
        json.dump(RESUME_DATA, FILE)  
        print(' Save json file!')
    RESULTS_RASD.to_csv(NAME + '.txt', sep = '\t', index = False)
    print(' Save txt file!')

    """
    BETA_DF = pd.read_csv('RASD_TOOLBOX/beta_df.txt', delimiter = ";",  names = ['PF' ,'BETA'])
    BETA_APROX = round(P_FVALUE,5)
    BETA_VALUE_INDEX = (BETA_DF['PF'].sub(P_FVALUE).abs().idxmin())
    BETA_VALUE = BETA_DF['BETA'][BETA_VALUE_INDEX]   
    BETA_F.append(BETA_VALUE)
    """
    """
    # Save results
    RESULTS_REP = {'TOTAL RESULTS': RESULTS_RASD, 'NUMBER OF FAILURES': N_F, 'PROBABILITY OF FAILURE': P_F, 'BETA INDEX': BETA_F}
    RESULTS.append(RESULTS_REP)
    NAME = 'RASD_' + MODEL + '_REP_' + str(J) + '_SAMPLES_' + str(N_POP) + '_' + str(datetime.now().strftime('%Y%m%d %H%M%S')) + '.txt'
    HEADER_NAMES =  ';'.join(COLUMNS_NAMES)
    np.savetxt(NAME, RESULTS_RASD, fmt = '%1.5f', delimiter = ';' , header = HEADER_NAMES)
    """
    return RESULTS_RASD