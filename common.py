import yaml

#__config = None

def config():
    __config = None
    if not __config:
        with open('config.yml', mode='r') as f:
            __config = yaml.load(f)

    return __config

