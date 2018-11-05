class SINQHMError(Exception):
    """The basic exception class for exceptions.

    Every SINQHMError subclass has a "category" attribute, a string that is
    shown to the user instead of the exception class.

       def doRead(self, maxage=0):
           if not self._ready:
               raise SINQHMError(self, 'device is not ready')
    """
    category = 'Error'
    device = None
    tacoerr = None

    def __init__(self, *args, **kwds):
        # store the originating device on the exception
        args = list(args)
        nargs = len(args)
        if nargs:
            if args[0] is None:
                del args[0]
            elif not isinstance(args[0], str):
                self.device = args[0]
                prefix = '[%s] ' % args[0].name
                if nargs > 1 and args[1].startswith(prefix):
                    # do not add a prefix if it already exists
                    del args[0]
                else:
                    args[0] = prefix
        self.__dict__.update(kwds)
        Exception.__init__(self, ''.join(args))


class CommunicationError(SINQHMError):
    """Exception to be raised when some hardware communication fails."""
    category = 'Communication error'


class AuthenticationError(SINQHMError):
    """Exception to be raised when some hardware communication fails."""
    category = 'Authentication error'