import os

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")

    MONGODB_SETTINGS = [
        { 
        'db' : os.getenv("MONGODB_DATABASE"), 
        'host' : os.getenv("MONGODB_HOSTNAME"),
        'port' : int(os.getenv("MONGODB_PORT")),
        'alias' : 'default',
        'username' : os.getenv("MONGODB_USERNAME"),
        'password' : os.getenv("MONGODB_PASSWORD"),
        }
    ]
