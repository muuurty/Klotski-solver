from collections import deque


def state_key(xs, ys):
    return ','.join(map(str, xs)) + '|' + ','.join(map(str, ys))


def is_solution_state(xs, ys, key_idx, goal_x, goal_y):
    return xs[key_idx] == goal_x and ys[key_idx] == goal_y


def can_place(xs, ys, sx, sy, i, nx, ny, grid_w, grid_h):
    if nx < 0 or ny < 0 or nx + sx[i] > grid_w or ny + sy[i] > grid_h:
        return False
    for j in range(len(xs)):
        if j == i:
            continue
        if not (nx + sx[i] <= xs[j] or xs[j] + sx[j] <= nx or ny + sy[i] <= ys[j] or ys[j] + sy[j] <= ny):
            return False
    return True


def all_possible_moves(xs, ys, sx, sy, grid_w, grid_h):
    moves = []
    n = len(xs)
    for i in range(n):
        # down
        if ys[i] + sy[i] < grid_h:
            if can_place(xs, ys, sx, sy, i, xs[i], ys[i]+1, grid_w, grid_h):
                nxs = xs.copy(); nys = ys.copy(); nys[i] = ys[i]+1; moves.append((nxs, nys))
        # right
        if xs[i] + sx[i] < grid_w:
            if can_place(xs, ys, sx, sy, i, xs[i]+1, ys[i], grid_w, grid_h):
                nxs = xs.copy(); nys = ys.copy(); nxs[i] = xs[i]+1; moves.append((nxs, nys))
        # up
        if ys[i] > 0:
            if can_place(xs, ys, sx, sy, i, xs[i], ys[i]-1, grid_w, grid_h):
                nxs = xs.copy(); nys = ys.copy(); nys[i] = ys[i]-1; moves.append((nxs, nys))
        # left
        if xs[i] > 0:
            if can_place(xs, ys, sx, sy, i, xs[i]-1, ys[i], grid_w, grid_h):
                nxs = xs.copy(); nys = ys.copy(); nxs[i] = xs[i]-1; moves.append((nxs, nys))
    return moves


def solve_bfs(start_xs, start_ys, sx, sy, key_index=3, goal_x=0, goal_y=0, grid_w=4, grid_h=5, steps_limit=200000):
    start_key = state_key(start_xs, start_ys)
    if is_solution_state(start_xs, start_ys, key_index, goal_x, goal_y):
        return [ (start_xs.copy(), start_ys.copy()) ], 1

    q = deque()
    q.append((start_xs.copy(), start_ys.copy()))
    parent = { start_key: None }
    visited = 1

    while q:
        xs, ys = q.popleft()
        cur_key = state_key(xs, ys)
        moves = all_possible_moves(xs, ys, sx, sy, grid_w, grid_h)
        for nxs, nys in moves:
            k = state_key(nxs, nys)
            if k in parent:
                continue
            parent[k] = cur_key
            visited += 1
            if is_solution_state(nxs, nys, key_index, goal_x, goal_y):
                # reconstruct path
                path = []
                cur = k
                while cur is not None:
                    left, right = cur.split('|')
                    xs_arr = list(map(int, left.split(','))) if left else []
                    ys_arr = list(map(int, right.split(','))) if right else []
                    path.append((xs_arr, ys_arr))
                    cur = parent[cur]
                path.reverse()
                return path, visited
            q.append((nxs, nys))
            if visited > steps_limit:
                raise RuntimeError('Exceeded node limit')
    return [], visited
