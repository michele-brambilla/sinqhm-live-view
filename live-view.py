import argparse as argparse

from python.authentication import Authenticator
from python.connection import HttpConnector
from python.hmplot import SINQHMView


def main(args):
    shape = args.shape
    """ Run the demo mode """
    if args.demo is True:
        if shape is None:
            shape = [10, 20]
        view = SINQHMView(shape=shape)
        view.live(args.interval)
        return

    authorized_user = Authenticator().authenticate()
    connector = HttpConnector(args.hostname, authorized_user, demo=args.demo)
    """ if the shape is not provided on the command line tries to guess 
    from the histogram memory configuration """
    if shape is None:
        shape = connector.get_shape()

    view = SINQHMView(connection=connector, shape=shape)
    view.live(args.interval)
    return


if __name__ == '__main__':
    """The SINQ histogram memory live viewer.

    The program requires the authorization to access the histogram memory, 
    then using http requests reads the data and plots the resulting histogram.
    
    To kill the program simply close the plot window. 
    """

    parser = argparse.ArgumentParser(description='SINQ Histogram Memory live viewer.')
    parser.add_argument('-i', '--interval', action='store', type=int,
                        default=5, help='update interval')
    parser.add_argument('-s', '--shape', action='store', type=int, nargs='+',
                        help='histogram shape')
    parser.add_argument('--demo', action='store_true', help='demo mode', default=None)
    parser.add_argument('--hostname', action='store', type=str,
                        default='localhost:8080', help='SINQ Histogram Memory host')
    args = parser.parse_args()

    main(args)
