def sanitize_dependencies(tasks: list):
    valid_ids = {task["id"] for task in tasks}

    for task in tasks:
        task["dependencies"] = [
            d for d in task["dependencies"] if d in valid_ids
        ]

    return tasks
