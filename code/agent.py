import sys
import numpy as np

class Agent:
    def __init__(self, strategies, probabilities=None):
        if probabilities:
            assert len(strategies) == len(probabilities)
            assert sum(probabilities) == 1
        
        self.strategies = strategies
        self.probabilities = probabilities


    def play(self, trials=100):
        # pick a strategy with its respective probability
        strategy_indices = np.random.choice(np.arange(len(self.strategies)), size=trials, p=self.probabilities)
        return np.array(self.strategies)[strategy_indices]
        

if __name__ == '__main__':
    temp = Agent([[1,2,3]])
    # counts = {}
    for x in temp.play():
        print(x)

