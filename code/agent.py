import sys
import numpy as np
import blotto_utils as bu

class Agent:
    def __init__(self, strategies, probabilities=None):
        if probabilities:
            assert len(strategies) == len(probabilities)
            # assert sum(probabilities) == 1
            probabilities = bu.normalize_probabilities(probabilities)
        
        self.strategies = strategies
        self.probabilities = probabilities


    def play(self, trials=100, seed=0):
        np.random.seed(seed)
        # pick a strategy with its respective probability
        strategy_indices = np.random.choice(np.arange(len(self.strategies)), size=trials, p=self.probabilities)
        return np.array(self.strategies)[strategy_indices]
        

if __name__ == '__main__':
    temp = Agent([1,2,3], [0.1, 0.1, 0.8])
    # counts = {}
    for x in temp.play():
        print(x)

