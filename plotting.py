import matplotlib.pyplot as plt
import numpy as np

def plot_simulation_results(agent_1, agent_2):
    plt.rcdefaults()
    agent_tags = (agent_1.tag, agent_2.tag)
    y_pos = np.arange(len(agent_tags))
    performance = [agent_1.wins / agent_1.games_played,
                    agent_2.wins / agent_2.games_played]
    fig, ax = plt.subplots()
    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(agent_tags)
    ax.set_xlabel('Win ratio')
    ax.set_title('Win ratios after {} games'.format(agent_1.games_played))
    plt.show()
