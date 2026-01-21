import argparse
import json
import os

path = 'tasklist.json'
if os.path.exists(path):
    print(f"'{path}' exists, accessing...")
else:
    print(f"'{path}' does not exist, creating...")


### BASIC CLI STRUCTURE ####################################

# Create parser
parser = argparse.ArgumentParser()

# Defining args we want to collect
parser.add_argument("action")
parser.add_argument("data1")
parser.add_argument("data2")

# Actually get arguments to parse
args = parser.parse_args()

verb = args.action
noun1 = args.data1
noun2 = args.data2

print(f"I want to {verb} {noun1} and {noun2}")

