# import random
from pathfinding import BattlesnakeAStarPathfinder


def calc_astar(request, start_coords, end_coords, force_target_traversible=False):
    st = (start_coords["x"], start_coords["y"])
    et = (end_coords["x"], end_coords["y"])
    astar_solver = BattlesnakeAStarPathfinder(
        request["board"],
        target=et,
        force_target_traversible=force_target_traversible,
    )
    return astar_solver.astar(st, et)


def calc_path_exists(
    self,
    request,
    start_coords,
    end_coords,
    force_target_traversible=False,
    debug=False,
):
    astar_path = self._calc_astar(
        request, start_coords, end_coords, force_target_traversible
    )
    if debug:
        print(f"  A*: {start_coords}, {end_coords}, {astar_path}")
    return astar_path is not None


def calc_path_length(self, request, start_coords, end_coords):
    astar_path = self._calc_astar(request, start_coords, end_coords)
    if astar_path:
        return len(list(astar_path))
    return None


def calc_possible_moves(request):
    possible_moves = ["up", "down", "left", "right"]

    def remove_move(move):
        if move in possible_moves:
            possible_moves.remove(move)

    head = request["you"]["body"][0]

    # Remove oob from possible moves
    if head["x"] == 0:
        remove_move("left")
    if head["y"] == 0:
        remove_move("down")
    if head["x"] == request["board"]["width"] - 1:
        remove_move("right")
    if head["y"] == request["board"]["height"] - 1:
        remove_move("up")

    # Remove all snake bodies, excluding tails, from possible moves
    for snake in request["board"]["snakes"]:
        necks = snake["body"][:-1]
        for neck in necks:
            if (neck["x"] == head["x"] + 1) and (neck["y"] == head["y"]):
                remove_move("right")
            if (neck["x"] == head["x"] - 1) and (neck["y"] == head["y"]):
                remove_move("left")
            if (neck["x"] == head["x"]) and (neck["y"] == head["y"] + 1):
                remove_move("up")
            if (neck["x"] == head["x"]) and (neck["y"] == head["y"] - 1):
                remove_move("down")

    return possible_moves


def calc_targets(request):
    targets = []

    # head_coords = request["you"]["head"]
    tail_coords = request["you"]["body"][-1]

    targets.append(tail_coords)
    targets.append({"x": tail_coords["x"] + 1, "y": tail_coords["y"]})
    targets.append({"x": tail_coords["x"] - 1, "y": tail_coords["y"]})
    targets.append({"x": tail_coords["x"], "y": tail_coords["y"] + 1})
    targets.append({"x": tail_coords["x"], "y": tail_coords["y"] - 1})

    return targets


def calc_best_move(request, moves, targets):
    head_coords = request["you"]["head"]

    for target_coords in targets:
        print(f" TARGET -> {target_coords}")

        distance_moves = []
        for move in moves:
            move_coords = calc_move_coords(head_coords, move)
            path_length = calc_path_length(request, move_coords, target_coords)
            if path_length:
                distance_moves.append((move, path_length))

        if distance_moves:
            distance_moves.sort(key=lambda x: x[1])
            return distance_moves[0][0]

    if moves:
        return moves[0]

    print("   NO VALID MOVES TO ALL TARGETS")
    return "up"


def calc_move_coords(coords, move):
    if move == "up":
        return {"x": coords["x"], "y": coords["y"] + 1}
    if move == "down":
        return {"x": coords["x"], "y": coords["y"] - 1}
    if move == "right":
        return {"x": coords["x"] + 1, "y": coords["y"]}
    return {"x": coords["x"] - 1, "y": coords["y"]}


class Battlesnake:
    def __init__(self):
        self.apiversion = "1"
        self.author = "bvanvugt"
        self.version = "Day 5"
        self.color = "#36627b"
        self.head = "silly"
        self.tail = "curled"

    def move(self, request):
        turn = request["turn"]
        print(f"\n{turn}")

        move = "up"
        possible_moves = calc_possible_moves(request)
        if possible_moves:
            targets = calc_targets(request)
            move = calc_best_move(request, possible_moves, targets)

        print(f"{turn}: {possible_moves} -> {move}")
        return move
