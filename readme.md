# Task tracker.

Simple CLI task tracker for backend roadmap.

Usage:

- `help`: prints the following commands in the CLI.
- `add "<description>"`: adds a task with the description given.
- `update <task-id> "<description>"`: Updated the description of the task with id = task-id with the description given.
- `delete <task-id>`: deletes the task with id = task-id from the tasks.json file.
- `mark-in-progress <task-id>`: marks the task with id = task-id as WIP.
- `mark-done <task-id>`: marks the task with id = task-id as DONE.
- `list`: list all the tasks contained in the tasks.json file.
- `quit`: exits the program.
