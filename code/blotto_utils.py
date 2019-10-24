import sys
import random

# from the POV of player 1
# if symmetric payoffs then ut1 == ut2

def battle(col1, col2, ut1, ut2, split=False, seed=0):
    random.seed(0)
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

def eval_strats(test, train, weights):
    results = []
    for a in test:
        temp_result = 0
        for b in train:
            temp_result += battle(a, b, weights, weights)
                
        results.append((a, temp_result))

    return results

def cross(parents):
    n = len(parents)
    c = len(parents[0])
    child = [0 for _ in range(c)]
    for parent in parents:
        child = [child[i]+parent[i] for i in range(len(parent))]
        
    return [x/n for x in child]

def make_integer(strat):
    random.seed(0)
    base_strat = [int(x) for x in strat]
    additions = 100 - sum(base_strat)
    for _ in range(additions):
        index = random.randint(1, 10)
        base_strat[index] += 1
    return base_strat


def mutate_noise(strat, noise):
    new_strat = [x+y for x, y in zip(strat, noise)]
    if all(map((lambda x: x >= 0), new_strat)):
        return new_strat
    else:
        return strat

        