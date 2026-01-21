import argparse
import datetime
import json
import os

path = 'tasklist.json'

### BASIC CLI STRUCTURE ####################################

# Create parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

## Subparsers ####
add_parser = subparsers.add_parser("add")
add_parser.add_argument("description")

update_parser = subparsers.add_parser("update")
update_parser.add_argument("id", type=int)
update_parser.add_argument("description")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=int)
delete_parser.add_argument("description")

# Collect parsed items and store as namespace
args = parser.parse_args()


### COMMANDS ################################################

if args.command == "add":

    # Check if the JSON tasklist file exists, if not create an empty one
    if not os.path.exists(path):
        print(f"'{path}' does not exist, creating...")
        with open(path, 'w') as f:
            json.dump([], f)

    print(f"'{path}' exists, accessing...")

    # Open the tasklist on read mode
    with open(path, 'r') as f:
        # loading the JSON file into an accessible copy variable
        task_list = json.load(f)

        # Calculating next id
        if task_list:
            next_id = max(task["id"] for task in task_list) + 1
        else:
            next_id = 0

        # Creating new task to add
        new_task = {
            "id": next_id,
            "description": args.description,
            "status": "todo",
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
        }

        # Adding new task to the tasklist copy
        task_list.append(new_task)

    # Opening tasklist but now in write mode
    with open(path, 'w') as f:
        # Overwrite JSON file with updates
        json.dump(task_list, f)
        print(f"Task added successfully (ID: {next_id})")



if args.command == "update":

    # Check if the JSON tasklist file exists, if not create an empty one
    if os.path.exists(path):

        print(f"'{path}' exists, accessing...")

        # Open the tasklist on read mode
        with open(path, 'r') as f:
            # loading the JSON file into an accessible copy variable
            task_list = json.load(f)

            task_id = args.id

            for item in task_list:
                if item["id"] == task_id:
                    print("THE ID WE'RE LOOKING AT IS " + str(item["id"]))
                    updated_item = task_list[task_id]
                    updated_item["description"] = args.description
                    updated_item["updatedAt"] = datetime.datetime.now().isoformat()

        with open(path, 'w') as f:
            json.dump(task_list, f)
            print(f"Task {task_id} has been updated: \n''{updated_item}''\n")
    else:
        print(f"'{path}' does not exist, no tasks to update...")

