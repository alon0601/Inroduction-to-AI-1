from global_function import expand, number_expands
from heapq import heappop, heappush, heapify


def a_star(problem, h):
    limit = 10000
    open_arr = [problem.Initial_State]
    heapify(open_arr)
    close = []
    count = 0
    while (limit):
        if len(open_arr) == 0:
            return "failure"
        else:
            state = heappop(open_arr)
            count += 1
            if count % 10 == 0:
                print("loop num: ", count)
            if problem.Goal_Test(state, h):
                return state
            if not in_close(close, state):  ## there is a problem with the node state
                close.insert(0, state)
                expand_array = expand(state, h)
                for state_ex in expand_array:
                    heappush(open_arr, state_ex)
        limit -= number_expands


def restore_path(state):
    path = [state.Node]
    while state.prev != None:
        path.insert(0, state.Prev.Node)
        state = state.prev
    return path


def in_close(close, state):
    for s in close:
        if s.Node == state.Node and s.Node.f < state.Node.f:
            return True
    return False