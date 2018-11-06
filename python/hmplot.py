import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# matplotlib.use('macosx')


class SINQHMViewOrig(object):
    shape = None

    def __init__(self, shape):
        self.shape = shape
        self.fig = plt.imshow(np.array(np.zeros(shape)), cmap=cm.hot, aspect='auto')
        plt.ion()
        plt.show()

    def plot(self, values):
        plt.clf()
        histogram = np.reshape(values, self.shape)
        plt.imshow(histogram, cmap=cm.hot, aspect='auto')
        plt.draw()
        plt.pause(0.001)


class SINQHMView(object):
    ani = None
    im = None

    def f(self, _x, _y):
        return np.sin(_x) + np.cos(_y)

    def _updatefig(self, *args):
        if self.connection is not None:
            counts = self.connection.get()
            print('counts: {}'.format(np.sum(counts)))
            self.im.set_array(np.reshape(counts, self.shape))
        else:
            self.x += np.pi / 15.
            self.y += np.pi / 20.
            self.im.set_array(self.f(self.x, self.y))
        return self.im,

    def __init__(self, connection=None, shape=None):
        self.fig = plt.figure()
        self.connection = connection
        self.shape = shape

    def live(self, interval):
        self.ani = animation.FuncAnimation(self.fig, self._updatefig, interval=1000 * interval, blit=True)
        if self.connection is not None:
            counts = self.connection.get()
            print('counts: {}'.format(np.sum(counts)))
            self.im = plt.imshow(np.reshape(counts, self.shape), animated=True, cmap=cm.hot, aspect='auto')
        else:
            self.x = np.linspace(0, 2 * np.pi, self.shape[0])
            self.y = np.linspace(0, 2 * np.pi, self.shape[1]).reshape(-1, 1)
            self.im = plt.imshow(self.f(self.x, self.y), animated=True)
        plt.show()


if __name__ == '__main__':
    """Test program"""
    p = SINQHMView()
    p.live(1)
