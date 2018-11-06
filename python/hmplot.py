import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
import matplotlib.animation as animation

#matplotlib.use('macosx')


class SINQHMView:

    shape = None

    def __init__(self, shape):
        self.shape = shape
        self.fig = plt.imshow(np.array(np.zeros(shape)), cmap=cm.hot, aspect='auto')
        plt.ion()
        plt.show()

    def plot(self,values):
        plt.clf()
        histogram = np.reshape(values,self.shape)
        plt.imshow(histogram, cmap=cm.hot, aspect='auto')
        plt.draw()
        plt.pause(0.001)

class SINQHMView1:
    shape = None

    def __init__(self, values, shape, interval=5000):
        self.values = values
        self.shape = shape
        self.fig = plt.figure()
        histogram = np.reshape(values, self.shape)
        self.im = plt.imshow(histogram, animated=True)

        self.ani = animation.FuncAnimation(self.fig, self._updatefig, interval=interval, blit=True)
        plt.show()

    def _updatefig(self,values):
        print('update')
        print(values[0])
        histogram = np.reshape(self.values, self.shape)
        self.im.set_array(histogram)
        return self.im,


class Plotit:



    def f(self,_x, _y):
        return np.sin(_x) + np.cos(_y)

    def _updatefig(self,*args):
        print('update')
        self.x += np.pi / 15.
        self.y += np.pi / 20.
        self.im.set_array(self.f(self.x, self.y))
        return self.im,

    def __init__(self):
        self.fig = plt.figure()
        self.ani = animation.FuncAnimation(self.fig, self._updatefig, interval=50, blit=True)
        self.x = np.linspace(0, 2 * np.pi, 120)
        self.y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)

        self.im = plt.imshow(self.f(self.x, self.y), animated=True)
        plt.show()




if __name__ == '__main__':
    # from time import sleep
    #
    # shape = [10,10]
    # data = np.zeros(np.prod(shape))
    # view = SINQHMView1(data,shape,1000)
    #
    # for i in range(1,10):
    #     data = np.random.randint(0, high=10, size=np.prod(shape))
    #     # view.plot(data)
    #     sleep(2)
    plotit = Plotit()