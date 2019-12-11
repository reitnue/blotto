from agent import Agent
import blotto_utils as bu

def play_game(agent_a, agent_b, weight_a=bu.WEIGHTS, weight_b=bu.WEIGHTS, trials=100, percentage=True):
    a_wins = 0
    a_strats = agent_a.play(trials=trials)

    if type(agent_b) == list:
        b_strats = agent_b
    else:
        b_strats = agent_b.play(trials=trials)

    for a, b in zip(a_strats, b_strats):
        a_wins += bu.battle(a, b, weight_a, weight_b, split=False, seed=(bu.l1_norm(a, b)))

    return 0.5 + (a_wins/(2*trials))
    
def make_nash_agents(strats_a, strats_b):
    probs_a, probs_b = bu.blotto_nash(strats_a, strats_b)
    
    probs_a_norm = bu.normalize_probabilities(probs_a)
    probs_b_norm = bu.normalize_probabilities(probs_b)
    
    agent_a = Agent(strats_a, list(probs_a_norm))
    agent_b = Agent(strats_b, list(probs_b_norm))

    return agent_a, agent_b


if __name__ == '__main__':
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    temp1 = Agent([(11, 9,10,10,10,10,10,10,10,10)], [1])
    temp2 = Agent([(11, 10,10,10,10,10,10,10,10,10)], [1])

    print(play_game(temp1, temp2, weights, weights, trials=10))