from collections import deque, defaultdict


def read_input():
    with open("p23.input.txt", "r") as f:
        for line in f.readlines():
            link = line.strip().split('-')
            yield link[0], link[1]


def build_graph(links: [(str, str)]):
    graph = defaultdict(set)
    for link in links:
        l1, l2 = link
        graph[l1].add(l2)
        graph[l2].add(l1)
    return graph


def find_cycles(graph: {str: {str}}):
    seen_cycles = set()
    for starting_node in graph:
        paths = deque([[starting_node]])
        while paths:
            path = paths.popleft()
            if len(path) == 3:
                if starting_node in graph[path[-1]]:
                    seen_cycles.add(",".join(sorted(path)))
            else:
                for next_node in graph[path[-1]]:
                    paths.append(path + [next_node])
    return seen_cycles


def find_next_networks(prev_networks: [set], graph: {str: {str}}):
    next_networks = []
    seen = set()
    for network in prev_networks:
        for next_k in graph:
            if next_k in network:
                continue
            if all([network_node in graph[next_k] for network_node in network]):
                next_network = network | {next_k}
                hashkey = ",".join(sorted(next_network))
                if hashkey in seen:
                    continue
                seen.add(hashkey)
                next_networks.append(network | {next_k})
    return next_networks


if __name__ == "__main__":
    total = 0
    links = list(read_input())
    g = build_graph(links)
    networks = [{l1, l2} for l1, l2 in links]
    threes = find_next_networks(networks, g)

    for network in threes:
        for node in network:
            if node[0] == "t":
                total += 1
                break
    print(total)
    while len(networks) > 1:
        networks = find_next_networks(networks, g)
    print(",".join(sorted(networks[0])))

