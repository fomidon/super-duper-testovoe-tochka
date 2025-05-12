import sys
import heapq
import collections
from typing import List, Tuple, Dict, Set


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def locate_entities(
    data: List[List[str]],
) -> Tuple[List[Tuple[int]], Dict[str, Tuple[int, int]]]:
    robots = []
    keys = {}
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == "@":
                robots.append((r, c))
            elif "a" <= ch <= "z":
                keys[ch] = (r, c)
    return robots, keys


def build_key_bitmask(keys: Dict[str, Tuple[int, int]]) -> Tuple[Dict[str, int], int]:
    mapping = {ch: 1 << (ord(ch) - ord("a")) for ch in keys}
    full = 0
    for b in mapping.values():
        full |= b
    return mapping, full


def bfs_from(
    data: List[List[str]], start: Tuple[int, int], char_to_bit: Dict[str, int]
) -> List[Tuple[str, int, int]]:
    R, C = len(data), len(data[0])
    sr, sc = start
    dq = collections.deque([(sr, sc, 0, 0)])
    visited: Dict[Tuple[int, int], Set[int]] = {(sr, sc): {0}}
    result = []

    while dq:
        r, c, dist, mask = dq.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            cell = data[nr][nc]
            if cell == "#":
                continue

            new_mask = mask
            if "A" <= cell <= "Z":
                keych = cell.lower()
                if keych not in char_to_bit:
                    continue  # дверь без ключа
                new_mask |= char_to_bit[keych]

            pos = (nr, nc)
            prev_masks = visited.get(pos, set())
            if any(pm & new_mask == pm for pm in prev_masks):
                continue

            visited[pos] = {pm for pm in prev_masks if pm & new_mask != pm}
            visited[pos].add(new_mask)

            if "a" <= cell <= "z":
                result.append((cell, dist + 1, new_mask))

            dq.append((nr, nc, dist + 1, new_mask))

    return result


def build_adjacency(
    robots: List[Tuple[int, int]],
    keys: Dict[str, Tuple[int, int]],
    char_to_bit: Dict[str, int],
    data: List[List[str]],
) -> Dict[int, List[Tuple[int, int, int]]]:
    adj: Dict[int, List[Tuple[int, int, int]]] = {}
    for idx, start in enumerate(robots):
        adj[idx] = []
        for ch, dist, req in bfs_from(data, start, char_to_bit):
            target = 4 + (ord(ch) - ord("a"))
            adj[idx].append((target, dist, req))

    for ch, pos in keys.items():
        node = 4 + (ord(ch) - ord("a"))
        adj[node] = []
        for ch2, dist, req in bfs_from(data, pos, char_to_bit):
            target = 4 + (ord(ch2) - ord("a"))
            adj[node].append((target, dist, req))

    return adj


def dijkstra_search(
    adjacency: Dict[int, List[Tuple[int, int, int]]], full_mask: int
) -> int:
    start_state = (0, (0, 1, 2, 3), 0)
    pq = [(0, (0, 1, 2, 3), 0)]
    seen: Dict[Tuple[Tuple[int, ...], int], int] = {}

    while pq:
        dist, positions, kmask = heapq.heappop(pq)
        if kmask == full_mask:
            return dist
        if seen.get((positions, kmask), float("inf")) <= dist:
            continue
        seen[(positions, kmask)] = dist

        for i in range(4):
            node = positions[i]
            for target, d, req in adjacency.get(node, []):
                bit = 1 << (target - 4)
                if kmask & bit:
                    continue
                if req & ~kmask:
                    continue
                new_mask = kmask | bit
                new_pos = list(positions)
                new_pos[i] = target
                new_tuple = tuple(new_pos)
                new_dist = dist + d
                if seen.get((new_tuple, new_mask), float("inf")) > new_dist:
                    heapq.heappush(pq, (new_dist, new_tuple, new_mask))

    return -1


def solve(data: List[List[str]]) -> int:
    robots, keys = locate_entities(data)
    if not keys:
        return 0

    char_to_bit, full_mask = build_key_bitmask(keys)
    adjacency = build_adjacency(robots, keys, char_to_bit, data)
    return dijkstra_search(adjacency, full_mask)


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == "__main__":
    main()
