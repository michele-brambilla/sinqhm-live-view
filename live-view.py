import argparse as argparse

from python.authentication import Authenticator
from python.authentication import User
from python.connection import HttpConnector
from python.hmplot import SINQHMView
from python.signals import GracefulKiller
from time import sleep


def main(args):
    if args.demo is not True:
        print('real')
        authorized_user = Authenticator().authenticate()
    else:
        print('demo')
        authorized_user = User('nouser','nopasswd')

    connector = HttpConnector(args.hostname, authorized_user,demo=args.demo)
    if args.shape is None:
        shape = connector.get_shape()
    else:
        shape = args.shape

    view = SINQHMView(shape)
    killer = GracefulKiller()

    while 1:
        data = connector.get()
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
    parser.add_argument('-s', '--shape', action='store', type=int, nargs='+',
                        help='histogram shape')
    parser.add_argument('--demo', action='store_true', help='demo mode', default=None)
    parser.add_argument('--hostname', action='store', type=str,
                        default='localhost:8080', help='SINQ Histogram Memory host')
    args = parser.parse_args()

    main(args)
