import argparse
import datetime
import json
import os

from numpy.matlib import empty

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

mip_parser = subparsers.add_parser("mark-in-progress")
mip_parser.add_argument("id", type=int)

md_parser = subparsers.add_parser("mark-done")
md_parser.add_argument("id", type=int)

list_parser = subparsers.add_parser("list")
list_parser.add_argument("status", choices=["done","todo","in-progress"], nargs='?') # nargs accepts 1 or none args

# Collect parsed items and store as namespace
args = parser.parse_args()


### COMMANDS ###########################################################################################################

### ADD COMMAND #####################################

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



### UPDATE COMMAND ###################################

elif args.command == "update":

    # Check if the JSON tasklist file exists, if not create an empty one
    if os.path.exists(path):

        print(f"'{path}' exists, accessing...")

        # Open the tasklist on read mode
        with open(path, 'r') as f:
            # loading the JSON file into an accessible copy variable
            task_list = json.load(f)

            task_id = args.id

            # Go through task list, look for requested update id
            for item in task_list:
                if item["id"] == task_id:
                    # Create copy of item and edit it
                    updated_item = task_list[task_id]
                    updated_item["description"] = args.description
                    updated_item["updatedAt"] = datetime.datetime.now().isoformat()

        # Write changes to JSON file
        with open(path, 'w') as f:
            json.dump(task_list, f)
            print(f"Task {task_id} has been updated: \n''{updated_item}''\n")
    else:
        print(f"'{path}' does not exist, no tasks to update...")



### DELETE COMMAND ###################################

elif args.command == "delete":

    # Check if the JSON tasklist file exists, if not create an empty one
    if os.path.exists(path):

        print(f"'{path}' exists, accessing...")

        # Open the tasklist on read mode
        with open(path, 'r') as f:
            # loading the JSON file into an accessible copy variable
            task_list = json.load(f)

            task_id = args.id

            # Go through tasklist and clone every task EXCEPT the one we want to delete
            filtered_tasklist = [task for task in task_list if task.get('id') != task_id]

            # Re index
            updated_tasklist = []
            next_id = 0
            for i, task in enumerate(filtered_tasklist):
                # Create a clone but change id
                clone_task = {
                    "id": next_id,
                    "description": task.get('description'),
                    "status": task.get('status'),
                    "createdAt": task.get('createdAt'),
                    "updatedAt": task.get('updatedAt'),
                }
                updated_tasklist.append(clone_task)
                next_id += 1

        # Write changes to JSON file
        with open(path, 'w') as f:
            json.dump(updated_tasklist, f)
            print(f"Task {task_id} has been deleted")
    else:
        print(f"'{path}' does not exist, no tasks to delete...")



### STATUS COMMAND ################################

elif args.command == "mark-in-progress" or args.command == "mark-done":

    # Check if the JSON tasklist file exists, if not create an empty one
    if os.path.exists(path):

        print(f"'{path}' exists, accessing...")

        # Open the tasklist on read mode
        with open(path, 'r') as f:
            # loading the JSON file into an accessible copy variable
            task_list = json.load(f)

            task_id = args.id
            updated_tasklist = task_list
            # Just slightly more efficient than just having two if statements (O(1) vs 0(N))
            status_dictionary = {
                "mark-in-progress": "in-progress",
                "mark-done": "done",
            }
            task_status = status_dictionary.get(args.command)
            task = updated_tasklist[task_id]
            # Create a clone but change id
            clone_task = {
                "id": task.get('id'),
                "description": task.get('description'),
                "status": task_status,
                "createdAt": task.get('createdAt'),
                "updatedAt": task.get('updatedAt'),
            }
            # Replacing old version/updating status.
            updated_tasklist.pop(task_id)
            updated_tasklist.insert(task_id, clone_task)

        # Write changes to JSON file
        with open(path, 'w') as f:
            json.dump(updated_tasklist, f)
            print(f"Task {task_id} status has been changed to {args.command}")
    else:
        print(f"'{path}' does not exist, no statuses to adjust...")



### LIST COMMAND ###########################################

elif args.command == "list":
    # Check if the JSON tasklist file exists, if not create an empty one
    if os.path.exists(path):

        print(f"'{path}' exists, accessing...")

        # Open the tasklist on read mode
        with open(path, 'r') as f:
            # loading the JSON file into an accessible copy variable
            task_list = json.load(f)

            # Filter by status
            task_status = args.status
            # Go through tasklist and clone every task that is of status
            if task_status is None:
                filtered_tasklist = task_list
            else:
                filtered_tasklist = [task for task in task_list if task.get('status') == task_status]
                if not filtered_tasklist:
                    print(f"'No tasks found for status: {task_status}")
            next_id = 0
            # Display all tasks that fit the filter
            print("") # Line break before first for formatting
            for i, task in enumerate(filtered_tasklist):
                print(f"id: {task.get('id')}")
                print(f"description: {task.get('description')}")
                print(f"status: {task.get('status')}")
                print(f"createdAt: {task.get('createdAt')}")
                print(f"updatedAt: {task.get('updatedAt')}\n")
    else:
        print(f"'{path}' does not exist, no tasks to view...")