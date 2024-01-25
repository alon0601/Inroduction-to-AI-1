from collections import deque
from edge import edge


def bfs(start, destination, gragh_state, deliveries=None):
    gathered_points = set()
    queue = deque([(start, [])])
    time = gragh_state.graph_state['T']
    while queue:
        point, path = queue.popleft()
        if destination == 'P':
            for p in gragh_state.graph_state['P']:
                if p.point == point:
                    if time >= p.p_time:
                        return path[0] if path else path
                    else:
                        break  # unless there can be two packs on the same point?
        elif destination == 'D':
            for d in deliveries:
                if d.delivery == point:
                    if time <= d.d_time:
                        return path[0] if path else path
                    else:
                        break  # unless there can be two deliveries to the same point?
        elif destination == 'F':
            for fe in gragh_state.graph_state['F']:
                if point in fe.points:
                    return path[0] if path else path

        if point in gathered_points:
            continue
        gathered_points.add(point)
        x, y = point
        neighbors = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]

        for neighbor in neighbors:
            nx, ny = neighbor
            if (0 <= nx <= gragh_state.graph_state['X'] and 0 <= ny <= gragh_state.graph_state['Y'] and
                    edge(nx, ny, x, y) not in gragh_state.graph_state['B'] and neighbor not in gathered_points):
                queue.append(((nx, ny), path + [neighbor]))

    return []