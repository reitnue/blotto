from agent import Agent
import blotto_utils as bu

def play_game(agent_a, agent_b, weight_a, weight_b, trials=100):
    a_wins = 0
    a_strats = agent_a.play(trials=trials)

    if type(agent_b) == list:
        b_strats = agent_b
    else:
        b_strats = agent_b.play(trials=trials)

    for a, b in zip(a_strats, b_strats):
        a_wins += bu.battle(a, b, weight_a, weight_b, split=False, seed=(bu.l1_norm(a, b)))

    return a_wins
    
if __name__ == '__main__':
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    temp1 = Agent([(11, 9,10,10,10,10,10,10,10,10)], [1])
    temp2 = Agent([(11, 10,10,10,10,10,10,10,10,10)], [1])

    print(play_game(temp1, temp2, weights, weights, trials=10))