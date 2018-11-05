import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm

#matplotlib.use('macosx')


class SINQHMView:

    shape = None

    def __init__(self,shape):
        self.shape = shape
        plt.imshow(np.array(np.zeros(shape)),cmap=cm.hot,aspect='auto')
        plt.ion()
        plt.show()

    def plot(self,data):
        plt.clf()
        data = np.reshape(data,self.shape)
        plt.imshow(data,cmap=cm.hot,aspect='auto')
        plt.draw()
        plt.pause(0.001)
        # plt.clf()


if __name__ == '__main__':
    from time import sleep

    shape = [10,10]
    view = SINQHMView(shape)

    for i in range(1,10):
        data = np.random.randint(0,high=10,size=np.prod(shape))
        view.plot(data)
        sleep(2)
