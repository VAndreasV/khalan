import matplotlib
matplotlib.use('agg')
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
    plt.close(fig)

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
    plt.close(fig)

def plot_exploration(total_data, strategy, parameter, min, max, step, opp_strategy):
    total_stones = 2* HOUSES * INIT_STONES
    #tags = np.arange(min, max+step, step)
    means = np.mean(total_data, axis=1)
    ticks = np.arange(len(means))+1
    fig = plt.figure()
    plt.title('Score distributions for exploring parameter {} using {}'.format(parameter, strategy))
    box_ax = fig.add_subplot(111)
    box_ax.boxplot(total_data)
    score_ln = box_ax.plot(ticks, means, color='yellow', label='mean score')
    box_ax.set_ylim(ymin=0, ymax=total_stones)
    box_ax.set_ylabel('Captured stones')

    win_ax = box_ax.twinx()
    win_ratios = [len(np.where(np.array(data) > (total_stones / 2))[0]) / len(data) for data in total_data]
    win_ln = win_ax.plot(ticks, win_ratios, color='green', label='win ratio')
    win_ax.set_ylim(0.0,1.1)
    win_ax.set_ylabel('Win ratio')

    box_ax.set_xlabel('Parameter value')

    tags = []
    for idx,_ in enumerate(ticks):
        if idx%4 == 0:
            tags.append('%.2f'%(min + step * idx))
        else:
            tags.append('')
    plt.xticks(ticks, tags)

    # Legend
    lns = score_ln + win_ln
    labs = [ln.get_label() for ln in lns]
    box_ax.legend(lns, labs, loc=0)

    fig.savefig('../results/expl_{}_param_{}_VS_{}.pdf'.format(strategy, parameter, opp_strategy), bbox_inches='tight')
    plt.close(fig)