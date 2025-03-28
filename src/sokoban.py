import heapq
from enum import Enum
from itertools import count

movimientos = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


class Chars(str, Enum):
    WALL = "#"
    EMPTY = " "
    BOX = "$"
    TARGET = "."
    PLAYER = "@"
    BOX_ON_TARGET = "*"
    PLAYER_ON_TARGET = "+"


class State:
    def __init__(self, player, boxes, move=None, parent=None):
        self.player = player
        self.boxes = boxes
        self.move = move
        self.parent = parent

    def get_path(self):
        path = []
        node = self

        while node is not None:
            player = {"x": node.player[0], "y": node.player[1]}
            boxes = [{"x": box[0], "y": box[1]} for box in node.boxes]
            path.append({"player": player, "boxes": boxes, "move": node.move})
            node = node.parent

        return path[::-1]


class Sokoban:
    def __init__(self, filename):
        self.map, self.player, self.boxes, self.targets = self.load_level(filename)

    def load_level(self, filename):
        map = []
        player = None
        boxes = set()
        targets = set()

        with open(filename, "r") as f:
            for y, line in enumerate(f):
                map.append([])

                for x, char in enumerate(line.rstrip("\n")):
                    if char == Chars.WALL.value:
                        map[y].append(Chars.WALL)
                    else:
                        map[y].append(Chars.EMPTY)
                        if char == Chars.PLAYER.value:
                            player = (x, y)
                        elif char == Chars.BOX.value:
                            boxes.add((x, y))
                        elif char == Chars.TARGET.value:
                            targets.add((x, y))

        return map, player, boxes, targets

    def bfs(self):
        root = State(self.player, frozenset(self.boxes))
        frontier = [root]
        visited = set()

        expanded_nodes = 0

        while frontier:
            node = frontier.pop(0)
            expanded_nodes += 1

            if all(box in self.targets for box in node.boxes):
                frontier_count = len(frontier)
                targets = [{"x": target[0], "y": target[1]} for target in self.targets]
                path = node.get_path()
                return {
                    "map": self.map,
                    "targets": targets,
                    "frontier_nodes": frontier_count,
                    "expanded_nodes": expanded_nodes,
                    "steps": len(path) - 1,
                    "path": path,
                }

            for move, (dx, dy) in movimientos.items():
                new_player = (node.player[0] + dx, node.player[1] + dy)

                if self.map[new_player[1]][new_player[0]] == Chars.WALL:
                    continue

                new_boxes = node.boxes

                if new_player in node.boxes:
                    new_box = (new_player[0] + dx, new_player[1] + dy)

                    if new_box in node.boxes or self.map[new_box[1]][new_box[0]] == Chars.WALL:
                        continue

                    new_boxes = frozenset((new_box if box == new_player else box) for box in node.boxes)

                new_state = (new_player, new_boxes)

                if new_state not in visited:
                    visited.add(new_state)
                    new_node = State(new_player, new_boxes, move, node)
                    frontier.append(new_node)

        return None

    def dfs(self):
        root = State(self.player, frozenset(self.boxes))
        frontier = [root]
        visited = set()

        expanded_nodes = 0

        while frontier:
            node = frontier.pop()
            expanded_nodes += 1

            if all(box in self.targets for box in node.boxes):
                frontier_count = len(frontier)
                targets_dict = [{"x": target[0], "y": target[1]} for target in self.targets]
                path = node.get_path()
                return {
                    "map": self.map,
                    "targets": targets_dict,
                    "frontier_nodes": frontier_count,
                    "expanded_nodes": expanded_nodes,
                    "steps": len(path) - 1,
                    "path": path,
                }

            for move, (dx, dy) in movimientos.items():
                new_player = (node.player[0] + dx, node.player[1] + dy)

                if self.map[new_player[1]][new_player[0]] == Chars.WALL:
                    continue

                new_boxes = node.boxes

                if new_player in node.boxes:
                    new_box = (new_player[0] + dx, new_player[1] + dy)

                    if new_box in node.boxes or self.map[new_box[1]][new_box[0]] == Chars.WALL:
                        continue

                    new_boxes = frozenset((new_box if box == new_player else box) for box in node.boxes)

                new_state = (new_player, new_boxes)

                if new_state not in visited:
                    visited.add(new_state)
                    new_node = State(new_player, new_boxes, move, node)
                    frontier.append(new_node)

        return None

    def informed_search(self, heuristic_fn, use_astar: bool):
        root = State(self.player, frozenset(self.boxes))
        frontier = []
        visited = dict()
        counter = count()

        expanded_nodes = 0

        h = heuristic_fn(root, self.targets)
        heapq.heappush(frontier, (h, next(counter), 0, root))

        while frontier:
            _, _, g, node = heapq.heappop(frontier)
            expanded_nodes += 1

            if all(box in self.targets for box in node.boxes):
                frontier_count = len(frontier)
                targets_dict = [{"x": target[0], "y": target[1]} for target in self.targets]
                path = node.get_path()
                return {
                    "map": self.map,
                    "targets": targets_dict,
                    "frontier_nodes": frontier_count,
                    "expanded_nodes": expanded_nodes,
                    "steps": len(path) - 1,
                    "path": path,
                }

            for move, (dx, dy) in movimientos.items():
                new_player = (node.player[0] + dx, node.player[1] + dy)

                if self.map[new_player[1]][new_player[0]] == Chars.WALL:
                    continue

                new_boxes = node.boxes

                if new_player in node.boxes:
                    new_box = (new_player[0] + dx, new_player[1] + dy)

                    if new_box in node.boxes or self.map[new_box[1]][new_box[0]] == Chars.WALL:
                        continue

                    new_boxes = frozenset((new_box if box == new_player else box) for box in node.boxes)

                new_state = (new_player, new_boxes)
                new_g = g + 1

                if new_state not in visited or new_g < visited[new_state]:
                    visited[new_state] = new_g
                    new_node = State(new_player, new_boxes, move, node)
                    h = heuristic_fn(new_node, self.targets)
                    priority = h if not use_astar else new_g + h
                    heapq.heappush(frontier, (priority, next(counter), new_g, new_node))

        return None


def heuristica_manhattan(node: State, targets: set[tuple[int, int]]) -> int:
    total = 0
    
    for box in node.boxes:
        distancias = [abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in targets]
        total += min(distancias)

    return total


def heuristica_euclidean(node: State, targets: set[tuple[int, int]]) -> int:
    total = 0

    for box in node.boxes:
        distancias = [((box[0] - goal[0]) ** 2 + (box[1] - goal[1]) ** 2) ** 0.5 for goal in targets]
        total += min(distancias)

    return total
