from enum import Enum
import heapq
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


class TreeNode:
    def __init__(self, player, boxes, move=None, parent=None):
        self.player = player
        self.boxes = boxes
        self.move = move
        self.parent = parent

    def get_path(self):
        path = []
        node = self

        while node.parent is not None:
            path.append(node.move)
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
        root = TreeNode(self.player, frozenset(self.boxes))
        frontier = [root]
        visited = set()

        while frontier:
            node = frontier.pop(0)

            if all(box in self.targets for box in node.boxes):
                return node.get_path()

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
                    new_node = TreeNode(new_player, new_boxes, move, node)
                    frontier.append(new_node)
        return None
    
    
    def informed_search(self, heuristic_fn, use_astar: bool):
        root = TreeNode(self.player, frozenset(self.boxes))
        frontier = []
        visited = set()
        counter = count() # Para desempatar nodos con la misma prioridad y evitar comparar TreeNode vs TreeNode

        # (priority, g(n), TreeNode)
        h = heuristic_fn(root, self.targets)
        heapq.heappush(frontier, (h, next(counter), 0, root))

        while frontier:
            _, _, g, node = heapq.heappop(frontier)

            if all(box in self.targets for box in node.boxes):
                return node.get_path()

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
                    new_node = TreeNode(new_player, new_boxes, move, node)
                    g_nuevo = g + 1
                    h = heuristic_fn(new_node, self.targets)
                    priority = h if not use_astar else g_nuevo + h
                    heapq.heappush(frontier, (priority, next(counter), g_nuevo, new_node))

        return None
    
    
    

def heuristica_manhattan(node: TreeNode, targets: set[tuple[int, int]]) -> int:
    total = 0
    for box in node.boxes:
        # Calcular la distancia de esta caja a todos los objetivos
        distancias = [abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in targets]
        # Tomar la mínima distancia para esta caja
        total += min(distancias)
    return total