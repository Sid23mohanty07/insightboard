def detect_cycles(tasks: list):
    graph = {t["id"]: t["dependencies"] for t in tasks}
    visited = set()
    stack = set()
    blocked = set()

    def dfs(node):
        if node in stack:
            blocked.add(node)
            return
        if node in visited:
            return

        visited.add(node)
        stack.add(node)

        for dep in graph.get(node, []):
            dfs(dep)

        stack.remove(node)

    for task in tasks:
        dfs(task["id"])

    return blocked
