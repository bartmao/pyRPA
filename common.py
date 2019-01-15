import json

configs = json.load(open('config.json'))
selectors = json.load(open('selectors.json'))


def log(msg):
    if(configs["logLevel"] == "dev" or configs["logLevel"] == "trace"):
        print(msg)

def trace(msg):
    if(configs["logLevel"] == "trace"):
        print(msg)