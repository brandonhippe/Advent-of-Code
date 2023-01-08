from collections import defaultdict
import heapq


def bfs(startState, nextStateFunc, abortFunc, trackFunc, **kwargs):
    states = defaultdict(set)
    states[0].add(startState)

    visited = set()

    tracked = None
    while len(states) != 0:
        minT = min(states.keys())

        for state in states[minT]:
            if state in visited:
                continue

            visited.add(state)

            tracked = trackFunc(tracked = tracked, state = state, t = minT, visited = visited, **kwargs)

            if abortFunc(state = state, tracked = tracked, visited = visited, **kwargs):
                return minT if tracked is None else [minT, tracked]

            for newState, t in nextStateFunc(state = state, t = minT, tracked = tracked, visited = visited, **kwargs):
                states[t].add(newState)
                
        del(states[minT])

    return tracked


def aStar(startState, nextStateFunc, abortFunc, heuristicFunc, **kwargs):
    openList = [[heuristicFunc(state = startState, **kwargs), 0, startState]]
    openDict = {startState: heuristicFunc(state = startState, **kwargs)}
    closedDict = {}

    while len(openList) != 0:
        qF, qG, state = heapq.heappop(openList)

        if abortFunc(state = state, **kwargs):
            return qG

        if state in openDict:
            del(openDict[state])
        else:
            continue

        for newState, g in nextStateFunc(state = state, **kwargs):
            nG = g + qG
            nH = heuristicFunc(state = newState, **kwargs)
            nF = nG + nH

            if not (newState in openDict and openDict[newState] <= nF) and not (newState in closedDict and closedDict[newState] <= nF):
                heapq.heappush(openList, [nF, nG, newState])
                openDict[newState] = nF

        closedDict[state] = qF

    return float('-inf')