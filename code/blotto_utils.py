import sys
import random

MAGNITUDES = [1,1,1,1,1,2,2,2,3,3,4,5]

# from the POV of player 1
# if symmetric payoffs then ut1 == ut2

def battle(col1, col2, ut1, ut2, split=False, seed=0):
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
#                 print(rand_num)
                if rand_num > 0.5:
                    sum2 += ut2[index]
                else:
                    sum1 += ut1[index]
    if sum1 > sum2:
        return 1
    elif sum1 < sum2:
        return 0
    else:
        return 0.5


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


def mutate_noise(strat, noises, magnitude=0, seed=0):
    random.seed(seed)
    while True:
        noise = random.choice(noises)
        mag = random.choice(MAGNITUDES)
        # print(mag)
        new_strat = [x+(y*mag) for x, y in zip(strat, noise)]
        if all(map((lambda x: x >= 0), new_strat)):
            return new_strat

def l1_norm(a, b):
    return sum(map(abs, [x-y for x, y in zip(a, b)]))
    