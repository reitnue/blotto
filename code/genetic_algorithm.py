import sys
import blotto_utils as bu

def mutate_top(fittest, next_gen_list, noise, mutation_count=1):
    for i in range(14):
        for j in range(i+1, 15):
            next_gen_list.append(bu.mutate_noise(bu.make_integer(bu.cross([fittest[i][0], fittest[j][0]]), seed=(i+j+i*j)), noise, seed=(i+j)))

def mutate_half(fittest, next_gen_list, noise, mutation_count=1):
    for i in range(len(fittest)//2):
        next_gen_list.append(fittest[i][0])
        next_gen_list.append(bu.mutate_noise(fittest[i][0], noise, mutations=mutation_count, seed=i))

def evolve(a_strats, b_strats, generations, noise, mutate_func=mutate_top, **kwargs):
    for _ in range(generations):
        # fitness
        a_results, b_results = bu.eval_strats(a_strats, b_strats, bu.WEIGHTS)
        
        # selection
        a_fittest = sorted(a_results, key=(lambda x: (x[1], -(x[0][-1]))), reverse=True)
        b_fittest = sorted(b_results, key=(lambda x: (x[1], -(x[0][-1]))), reverse=True)

        # mutation and crossover
        a_next_gen = []
        b_next_gen = []
        
        # method 1: mutation among the top 14 of each
        # downsides - very simiar results
        mutate_func(a_fittest, a_next_gen, noise, mutation_count=kwargs.get('mutation_count', 1))
        mutate_func(b_fittest, b_next_gen, noise, mutation_count=kwargs.get('mutation_count', 1))
        
        a_strats = a_next_gen
        b_strats = b_next_gen
        
    return a_fittest, b_fittest, a_strats, b_strats

