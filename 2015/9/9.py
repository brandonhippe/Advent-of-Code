import time

def shortestPath(adj, collected, memo):
    if len(collected) == len(adj):
        return 0

    shortest = float('inf')
    for n in adj.keys():
        if n in collected:
            continue

        if tuple(collected + [n]) not in memo:
            memo[tuple(collected + [n])] = shortestPath(adj, collected + [n], memo)

        total = memo[tuple(collected + [n])] + (adj[collected[-1]][n] if len(collected) > 0 else 0)
        if total < shortest:
            shortest = total

    return shortest

def longestPath(adj, collected, memo):
    if len(collected) == len(adj):
        return 0

    longest = float('-inf')
    for n in adj.keys():
        if n in collected:
            continue

        if tuple(collected + [n]) not in memo:
            memo[tuple(collected + [n])] = longestPath(adj, collected + [n], memo)

        total = memo[tuple(collected + [n])] + (adj[collected[-1]][n] if len(collected) > 0 else 0)
        if total > longest:
            longest = total

    return longest

def main(verbose):
    with open("input.txt", encoding='UTF-8') as f:
        lines = [line.strip('\n').split(' ') for line in f.readlines()]

    adj = {l: {} for l in list(set([line[0] for line in lines] + [line[2] for line in lines]))}

    for n1, _, n2, _, dist in lines:
        adj[n1][n2] = int(dist)
        adj[n2][n1] = int(dist)

    part1 = shortestPath(adj, [], {})
    part2 = longestPath(adj, [], {})

    if verbose:
        print(f"\nPart 1:\nShortest path to all locations: {part1}\n\nPart 2:\nLongest path to all locations: {part2}")

    return [part1, part2]
    

if __name__ == "__main__":
    init_time = time.perf_counter()
    main("input.txt")
    print(f"\nRan in {time.perf_counter() - init_time} seconds.")
    