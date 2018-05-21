import matplotlib.pyplot as plt
import numpy as np
from board import HOUSES, INIT_STONES

def plot_simulation_results(agent_1, agent_2, prefix):
    fig = plt.figure()
    agent_tags = (agent_1.tag, agent_2.tag)
    y_pos = np.arange(len(agent_tags))
    performance = [agent_1.wins / agent_1.games_played,
                    agent_2.wins / agent_2.games_played]
    fig, ax = plt.subplots()
    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(agent_tags)
    ax.set_xlabel('Win ratio')
    ax.set_xlim(left=0.0, right=1.0)
    ax.set_title('Win ratios after {} games'.format(agent_1.games_played))
    fig.savefig('{}_win_ratio.pdf'.format(prefix), bbox_inches='tight')

def plot_scores(agent_1, agent_2, prefix):
    total_stones = 2* HOUSES * INIT_STONES
    # Wins
    fig = plt.figure()
    plt.boxplot([agent_1.win_scores, agent_2.win_scores])
    plt.title('Win score distribution after {} games'.format(agent_1.games_played))
    plt.xticks([1, 2], [agent_1.tag, agent_2.tag])
    plt.ylim(ymin=int(total_stones/2), ymax=total_stones)
    fig.savefig('{}_win_scores.pdf'.format(prefix), bbox_inches='tight')
    # Losses
    fig = plt.figure()
    plt.boxplot([agent_1.lose_scores, agent_2.lose_scores])
    plt.title('Loss score distribution after {} games'.format(agent_1.games_played))
    plt.xticks([1, 2], [agent_1.tag, agent_2.tag])
    plt.ylim(ymin=0, ymax=int(total_stones/2))
    fig.savefig('{}_loss_scores.pdf'.format(prefix), bbox_inches='tight')

def plot_exploration(total_data, strategy, parameter, min, max, step, opp_strategy):
    total_stones = 2* HOUSES * INIT_STONES
    tags = np.arange(min, max+step, step)
    means = np.mean(total_data, axis=1)
    ticks = np.arange(len(means))+1
    fig = plt.figure()
    plt.title('Score distributions for exploring parameter {} using {}'.format(parameter, strategy))
    plt.boxplot(total_data)
    plt.plot(ticks, means)
    plt.xticks(ticks, tags)
    plt.ylim(ymin=0, ymax=total_stones)
    fig.savefig('../results/expl_{}_param_{}_VS_{}.pdf'.format(strategy, parameter, opp_strategy), bbox_inches='tight')