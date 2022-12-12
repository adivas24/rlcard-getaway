''' An example of evluating the trained models in RLCard
'''
import os
import argparse

import rlcard
from rlcard.agents import (
    DQNAgent,
    RandomAgent,
)
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
)
dqn = 'experiments/dqn-result-linear-rewards_4player/model.pth'
nfsp = 'experiments/nfsp-result-linear-rewards_4player/model.pth'
cfr = 'experiments/cfr-result-linear-rewards_4player/model.pth'
dmc = 'experiments/dmc-result-linear-rewards_4player/model.pth'
ran = "random"
model_dic = {0: cfr, 1: ran, 2: ran , 3: ran}
def load_model(model_path, env=None, position=None, device=None):
    if os.path.isfile(model_path):  # Torch model
        import torch
        agent = torch.load(model_path, map_location=device)
        agent.set_device(device)
    elif os.path.isdir(model_path):  # CFR model
        from rlcard.agents import CFRAgent
        agent = CFRAgent(env, model_path)
        agent.load()
    elif model_path == 'random':  # Random model
        from rlcard.agents import RandomAgent
        agent = RandomAgent(num_actions=env.num_actions)
    else:  # A model in the model zoo
        from rlcard import models
        agent = models.load(model_path).agents[position]

    return agent

def evaluate(seed):

    # Check whether gpu is available
    device = get_device()

    # Seed numpy, torch, random
    set_seed(seed)

    # Make the environment with seed
    env = rlcard.make('getaway', config={'seed': seed})

    # Load models
    # models = ['random', 'random', 'experiments/getaway_dqn_try_2/model.pth', 'experiments/getaway_dqn_try_2/model.pth']
    # models = ['random', 'experiments/getaway_dqn_try_2/model.pth', 'random', 'experiments/getaway_dqn_try_2/model.pth']
    models = list(model_dic.values())
    #models = ['random','random','experiments/dqn-result-linear-rewards_4player/model.pth','experiments/dqn-result-linear-rewards_4player/model.pth']
    # models = ['experiments/uno_dqn/model.pth','random','random','random']
    agents = []
    for position, model_path in enumerate(models):
        agents.append(load_model(model_path, env, position, device))
    env.set_agents(agents)

    # Evaluate
    rewards = tournament(env, 1000)
    # for position, reward in enumerate(rewards):
    #     print(position, args.models[position], reward)
    return rewards

if __name__ == '__main__':
    # from operator import add
    cum_rewards = [0,0,0,0]
    # map(add, list1,list2)
    counter = int(input("Counter:\n"))
    intermediate_rewards = []
    from tqdm import tqdm
    for seed in tqdm(range(counter)):
        rewards = evaluate(seed*seed*562353647788 % 458441)
        print(cum_rewards,rewards)
        cum_rewards = [cum_rewards[i]+rewards[i] for i in range(len(cum_rewards))]
        intermediate_rewards.append([r/(seed+1) for r in cum_rewards])
    print([r/counter for r in cum_rewards])
    # print(intermediate_rewards)
    import numpy as np
    vector = np.transpose(np.array(intermediate_rewards))
    import matplotlib.pyplot as plt
    plt.plot(vector[0], 'r')
    plt.plot(vector[1], 'b')
    plt.plot(vector[2], 'g')
    plt.plot(vector[3], 'y')
    l = []
    for type in model_dic.values():
        if type != "random":
            l.append(type.split("/")[1].split("-")[0].upper() + " agent")
        else:
            l.append("Random agent")
    plt.legend(l)
    # plt.legend(["NFSP Agent","Random Agent"])
    #plt.title("DQN : Linear Rewards")
    plt.xlabel("Runs")
    plt.ylabel("Rewards")
    plt.show()
