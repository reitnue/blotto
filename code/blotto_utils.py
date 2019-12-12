import sys
import random
import scipy.optimize
import numpy as np
import os
import pickle
import gzip
import re
gz_re = re.compile(r'.gz$')
import math
import random
import datetime


MAGNITUDES = [1,1,1,1,1,2,2,2,3,3,4,5]
WEIGHTS = [1,2,3,4,5,6,7,8,9,10]
# from the POV of player 1
# if symmetric payoffs then ut1 == ut2

def battle(col1, col2, ut1=WEIGHTS, ut2=WEIGHTS, split=False, seed=0):
    random.seed(seed)
    assert len(col1) == len(col2) and len(ut1) == len(ut2) and len(col1) == len(ut1)
    sum1, sum2 = 0, 0
    for index in range(len(col1)):
        if col1[index] > col2[index]:
            sum1 += ut1[index]
        elif col1[index] < col2[index]:
            sum2 += ut2[index]
        else: # ==
            if split:
                sum1 += ut1[index] / 2
                sum2 += ut2[index] / 2
            else:
                rand_num = random.random()
                if rand_num > 0.5:
                    sum2 += ut2[index]
                else:
                    sum1 += ut1[index]
    if sum1 > sum2:
        return 1
    elif sum1 < sum2:
        return -1
    else:
        return 0

# noise arrays
# return [-mag, mag, 0, \dots, 0]
def generate_noise_arrays(magnitude): # generates 90 arrays
    noise_arrays = []
    temp = [0 for _ in range(10)]
    for i in range(9):
        for j in range(i+1, 10):
            if i != j:
                temp[i], temp[j] = magnitude, -magnitude
                noise_arrays.append(temp[:])
                
                temp[i], temp[j] = -magnitude, magnitude
                noise_arrays.append(temp[:])
                
                temp[i], temp[j] = 0, 0
    return noise_arrays

def eval_strats(a_strats, b_strats, weights):
    a_results = [0 for x in a_strats]
    b_results = [0 for x in b_strats]

    for i in range(len(a_strats)):
        a = a_strats[i]
        for j in range(len(b_strats)):
            b = b_strats[j]
            a_result = battle(a, b, weights, weights, seed=(i+j))
            b_result = 1 - a_result

            a_results[i] += a_result
            b_results[j] += b_result
    
    return list(zip(a_strats, a_results)), list(zip(b_strats, b_results))

def cross(parents):
    n = len(parents)
    c = len(parents[0])
    child = [0 for _ in range(c)]
    for parent in parents:
        child = [child[i]+parent[i] for i in range(len(parent))]
        
    return [x/n for x in child]

def make_integer(strat, seed=0):
    random.seed(seed)
    base_strat = [int(x) for x in strat]
    additions = 100 - sum(base_strat)
    for _ in range(additions):
        index = random.randint(0, 9)
        base_strat[index] += 1
    return base_strat

def mutate_noise(strat, noises, mutations=1, seed=0):
    random.seed(seed)
    curr_strat = strat
    for _ in range(mutations):
        while True:
            noise = random.choice(noises)
            mag = np.random.binomial(10, 0.5, 1)[0] # random.choice(MAGNITUDES)
            # print(mag)
            new_strat = [x+(y*mag) for x, y in zip(curr_strat, noise)]
            if all(map((lambda x: x >= 0), new_strat)):
                curr_strat = new_strat
                break
    return curr_strat

def l1_norm(a, b):
    return sum(map(abs, [x-y for x, y in zip(a, b)]))

def l2_norm(a, b):
    return math.sqrt(sum([(x-y) ** 2 for x, y in zip(a, b)]))

def make_neg(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            mat[i][j] *= -1

def transpose(mat):
    new_mat = []
    for j in range(len(mat[0])):
        new_mat.append([])
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            new_mat[j].append(mat[i][j])
    return new_mat

def make_payoff(a_strats, b_strats):
    payoff = []
    for a_index in range(len(a_strats)):
        payoff.append([])
        for b_index in range(len(b_strats)):
            payoff[a_index].append(battle(a_strats[a_index], b_strats[b_index]))
            
    return payoff

def blotto_nash(strats_a, strats_b):
    payoff = make_payoff(strats_a, strats_b)
    # print(payoff)
    make_neg(payoff)
    # print(payoff)
    payoff = transpose(payoff)
    # print(payoff)
    bounds = (0.0, 1.0)

    rows = len(strats_a)
    cols = len(strats_b)

    # offense
    b_ub = [-1.0] * cols
    c = [1.0] * rows
    # print(payoff)
    result = scipy.optimize.linprog(c, payoff, b_ub, None, None, bounds)
    # print(result)
    value = 1.0 / result.fun # v from lecture
    x = [xi * value for xi in result.x]
    new_x = [float("%.6f" % abs(i)) for i in x]
    
    # defense
    b_ub = [1.0] * rows
    c = [-1.0] * cols

    pay_off = make_payoff(strats_a, strats_b)
    # print(pay_off)
    result = scipy.optimize.linprog(c, pay_off, b_ub, None, None, bounds)
    y = [-yi * value for yi in result.x]
    new_y = [float("%.6f" % abs(i)) for i in y]
    return new_x, new_y

def normalize_probabilities(probs):
    probs = np.array(probs)
    probs /= probs.sum()
    return probs

def save_pickle(file_name, to_save):
    func = open
    if gz_re.search(file_name):
        func = gzip.open
    with func(file_name, 'wb') as db:
        pickle.dump(to_save, db)

def load_pickle(file_name):
    func = open
    if gz_re.search(file_name):
        func = gzip.open
    with func(file_name, 'rb') as db:
        return pickle.load(db)

