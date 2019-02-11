import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def plot_costs(cost_list):
    plt.plot(cost_list)
    plt.title('Change in Cost of Solution Over Time')
    plt.ylabel('Cost of solution')
    plt.xlabel('Solution number')
    plt.show()
