import json

configs = json.load(open('config.json', encoding='utf8'))
selectors = json.load(open('selectors.json', encoding='utf8'))


def log(msg):
    if(configs["logLevel"] == "dev" or configs["logLevel"] == "trace"):
        print(msg)

def trace(msg):
    if(configs["logLevel"] == "trace"):
        print(msg)