from .error import AuthenticationError

from collections import namedtuple
User = namedtuple('User', 'name, password')

class Authenticator():
    """Authenticates against the fixed list of usernames, passwords and
    user levels given in the "passwd" parameter (in order).

    An empty password means that any password is accepted.
    An empty username means that any username is accepted.
    Password less entries and anonymous entries are restricted
    to 'at most' USER level. If both fields are unspecified, we still request
    a username and restrict to GUEST level.
    """
    parameters = {'username' :'38ef1f498a09bdeb60928a81c0f77bb4',
                  'password' : '9e94b15ed312fa42232fd87a55db0d39'}

    def _hash(self, value, hash):
        import hashlib
        value = value.encode('utf-8')
        if hash == hashlib.md5(value).hexdigest():
            return value
        return None

    def __init__(self):
        pass

    def authenticate(self):
        import getpass
        username = ''
        password = ''
        try:
            username = getpass.getpass(prompt='User: ')
            username = username.strip().lower()
            if self._hash(username,self.parameters['username']) is None:
                raise AuthenticationError('Wrong username')

            password = getpass.getpass(prompt='Password: ')
            password = password.strip().lower()
            if self._hash(password,self.parameters['password']) is None:
                raise AuthenticationError('Wrong password')
        except KeyboardInterrupt as e:
            print(e)

        return User(username, password)
