import argparse as argparse

from python.authentication import Authenticator
from python.connection import HttpConnector
from python.hmplot import SINQHMView
from python.signals import GracefulKiller
from time import sleep
import numpy as np

def main(args):
    shape = [10,20]
    if args.demo is not True:
        authorized_user = Authenticator().authenticate()
        connector = HttpConnector(args.hostname, authorized_user)
        shape = connector.get_shape()[0:-1]

    view = SINQHMView(shape)
    killer = GracefulKiller()

    while 1:
        if args.demo is not True:
            data = connector.get()
        else:
            data = np.random.randint(0,100,np.prod(shape))
        view.plot(data)
        if killer.kill_now:
            break
        sleep(args.interval)
        if killer.kill_now:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SINQ Histogram Memory live viewer.')
    parser.add_argument('-i','--interval', action='store',type=int,
                        default=5, help='update interval')
    parser.add_argument('--demo', action='store_true', help='demo mode')
    parser.add_argument('--hostname', action='store', type=str,
                        default='localhost:8080', help='SINQ Histogram Memory host')
    args = parser.parse_args()

    main(args)
