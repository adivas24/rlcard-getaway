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
    env = rlcard.make('uno', config={'seed': seed})

    # Load models
    # models = ['random', 'random', 'experiments/getaway_dqn_try_2/model.pth', 'experiments/getaway_dqn_try_2/model.pth']
    # models = ['random', 'experiments/getaway_dqn_try_2/model.pth', 'random', 'experiments/getaway_dqn_try_2/model.pth']
    # models = ['experiments/nfsp-result-linear-rewards_4player/model.pth','random','random','random']
    models = ['experiments/uno_dqn/model.pth','random','random','random']
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
        rewards = evaluate(seed*seed*562353647789 % 458441)
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
    plt.legend(["NFSP Agent","Random Agent", "Random Agent", "Random Agent"])
    # plt.legend(["NFSP Agent","Random Agent"])
    plt.title("NFSP : Linear Rewards")
    plt.xlabel("Runs")
    plt.ylabel("Rewards")
    plt.show()
