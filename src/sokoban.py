from enum import Enum

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
        self.parent = parent  # Reference to the previous state (parent node)

    def get_path(self):
        """Reconstruct the path from the root to this node."""
        path = []
        node = self
        while node.parent is not None:  # Root node has no parent
            path.append(node.move)
            node = node.parent
        return path[::-1]  # Reverse to get correct order


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

    def search_tree(self):
        root = TreeNode(self.player, frozenset(self.boxes))  # Root node
        frontier = [root]  # Queue for BFS (can be changed to stack for DFS)
        visited = set()

        while frontier:
            node = frontier.pop(0)  # FIFO (BFS)

            # Check if all boxes are on targets
            if all(box in self.targets for box in node.boxes):
                return node.get_path()  # Return the solution path

            for move, (dx, dy) in movimientos.items():
                new_player = (node.player[0] + dx, node.player[1] + dy)

                # Skip if the player moves into a wall
                if self.map[new_player[1]][new_player[0]] == Chars.WALL:
                    continue

                # Copy boxes
                new_boxes = node.boxes

                # If the player moves into a box
                if new_player in node.boxes:
                    new_box = (new_player[0] + dx, new_player[1] + dy)

                    # If the box moves into a wall or another box, skip
                    if new_box in node.boxes or self.map[new_box[1]][new_box[0]] == Chars.WALL:
                        continue

                    # Create a new frozenset with updated box positions
                    new_boxes = frozenset((new_box if box == new_player else box) for box in node.boxes)

                new_state = (new_player, new_boxes)

                if new_state not in visited:
                    visited.add(new_state)
                    new_node = TreeNode(new_player, new_boxes, move, node)
                    frontier.append(new_node)

        return None  # No solution found

