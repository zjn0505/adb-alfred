import sys
import os

function = os.getenv('function')
config = os.getenv(function)
path = config.split("|")[1]

print (path)