import random

# from pprint import pprint

MOVE_MAP = (
    ((0, -1), 'up'),
    ((1, 0), 'right'),
    ((0, 1), 'down'),
    ((-1, 0), 'left')
)


class Brain:
    def __init__(self, state):
        self.state = state
        self.parse_board()

    def parse_board(self):
        # pprint(self.state, indent=4)
        bad_locs = set()
        for snake in self.state['board']['snakes']:
            for body in snake['body']:
                bad_locs.add((body['x'], body['y']))
        heads = []
        for snake in self.state['board']['snakes']:
            if snake['id'] == self.state['you']['id']:
                continue
            heads.append((snake['body'][0]['x'], snake['body'][0]['y']))

        cur_p = self.state['you']['body'][0]
        cur_p = (cur_p['x'], cur_p['y'])
        self.bad_locs = bad_locs
        self.heads = heads
        self.cur_p = cur_p
        self.board_height = self.state['board']['height']
        self.board_width = self.state['board']['width']

    def get_move(self):
        options = []
        safe_options = []
        for vec, direction in MOVE_MAP:
            new_p = (self.cur_p[0]+vec[0], self.cur_p[1]+vec[1])
            if new_p[0] < 0 or new_p[0] >= self.board_width:
                continue
            if new_p[1] < 0 or new_p[1] >= self.board_height:
                continue
            if new_p in self.bad_locs:
                continue
            options.append((vec, direction))
            for head in self.heads:
                if abs(head[0]-new_p[0]) + abs(head[1]-new_p[1]) == 1:
                    break
            else:
                safe_options.append((vec, direction))
        if safe_options:
            vec, direction = self.get_safest_options(safe_options)
            print('Moving safe:', direction)
            return direction
        if options:
            vec, direction = self.get_safest_options(options)
            print('Moving:', direction)
            return direction

        directions = ['up', 'down', 'left', 'right']
        direction = random.choice(directions)

        return direction

    def get_safest_options(self, starting_points):
        clear_ground = {}
        for vec, direction in starting_points:
            clear_ground[(vec, direction)] = self.bfs(
                (self.cur_p[0]+vec[0], self.cur_p[1]+vec[1])
            )
        best = max(clear_ground.values())
        best_choices = [k for k, v in clear_ground.items() if v == best]
        print(clear_ground, best_choices)
        return random.choice(best_choices)

    def bfs(self, starting_point):
        seen = {starting_point}
        edges = {starting_point}
        while edges:
            p = edges.pop()
            for vec, direction in MOVE_MAP:
                new_p = (p[0]+vec[0], p[1]+vec[1])
                if new_p in seen:
                    continue
                if new_p[0] < 0 or new_p[0] >= self.board_width:
                    continue
                if new_p[1] < 0 or new_p[1] >= self.board_height:
                    continue
                if new_p in self.bad_locs:
                    continue
                seen.add(new_p)
                edges.add(new_p)
        return len(seen)
