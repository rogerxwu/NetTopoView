# Demo
# treat each interface as a graph, use BFS to traverse all nodes
import json
from collections import defaultdict, deque

# Get the simulated metadata
devices = defaultdict(dict)
for device in ["device_A", "device_B", "device_C", "device_D"]:
    for metadata in ["get_facts", "get_lldp_neighbors"]:
        with open("./metadata/{}/{}.json".format(device, metadata), "r") as file:
            devices[device][metadata] = json.load(file)
# print(json.dumps(devices, indent=4))


def get_facts(device):
    return device["get_facts"]


def get_lldp_neighbors(device):
    return device["get_lldp_neighbors"]


# Build graph
graph = defaultdict(set)
for device in devices:
    for lldp_neighbor in devices[device]["get_lldp_neighbors"]:
        neighbor = lldp_neighbor["lldp_neighbor"]["connected_device"]
        graph[devices[device]["get_facts"]["hostname"]].add(neighbor)
        graph[neighbor].add(devices[device]["get_facts"]["hostname"])

print(graph)


def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    connections = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    connections.append((node, neighbor))
                    queue.append(neighbor)

    return connections


# output the connections first, then render the graphics

connections = bfs(graph, "Router_A")
print(connections)
print("\nAll connections in the network:")
for conn in connections:
    print(f"{conn[0]} ↔ {conn[1]}")
