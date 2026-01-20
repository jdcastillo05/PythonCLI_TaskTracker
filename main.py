import argparse
import json
import os

# Create parser
parser = argparse.ArgumentParser()

# Defining args we want to collect
parser.add_argument("action") # Action we wanna do
parser.add_argument("data") # What we wanna affect

# Actually get arguments to parse
args = parser.parse_args()

path = 'tasklist.json'
if os.path.exists(path):
    print(f"'{path}' exists, accessing...")
else:
    print(f"'{path}' does not exist, creating...")

# Reading command
action = args.action

if action == "add":