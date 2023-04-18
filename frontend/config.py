import os

class Config(object):
    SECRET_KEY = b'\x03%\x98\xa5\xe6`JP\xc2\xa9~\xf1\xc9\xde\xd0\xf3'

    MONGODB_SETTINGS = [
        { 
        'db' : 'frontend', 
        'host' : "localhost",
        'port' : 27017,
        'alias' : 'default',
        'username' : '',
        'password' : '',
        }
    ]
