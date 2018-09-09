import matplotlib.pyplot as plt
def draw(x, y):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)
    ax.set_xlabel('Number of Reducers')
    ax.set_ylabel('Time in Seconds')
    ax.set_title('Training Time as a function of # of Reducers')
    plt.show()

X = [1, 2, 5, 8, 10]
Y = [95, 62, 38, 32, 28]
draw(X, Y)
