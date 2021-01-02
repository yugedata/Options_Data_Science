# code to be added to mine.py to display live paper/real trading
#
#

import matplotlib.pyplot as plt
import numpy as np

X = np.linspace(0, 2, 1000)
Y = X**2 + np.random.random(X.shape)
go = True

plt.ion()
graph = plt.plot(X, Y)[0]

while go:
    Y = X**2 + np.random.random(X.shape)
    graph.set_ydata(Y)
    plt.draw()
    plt.pause(3)


