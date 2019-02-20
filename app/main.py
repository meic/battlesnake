import json
import os
import random
import bottle
from pprint import pprint

from api import ping_response, start_response, move_response, end_response

MOVE_MAP = (
    ((0, -1), 'up'),
    ((1, 0), 'right'),
    ((0, 1), 'down'),
    ((-1, 0), 'left')
)


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#e542f4"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    pprint(data, indent=4)
    bad_locs = set()
    for snake in data['board']['snakes']:
        for body in snake['body']:
            bad_locs.add((body['x'], body['y']))
    heads = []
    for snake in data['board']['snakes']:
        if snake['id'] == data['you']['id']:
            continue
        heads.append((snake['body'][0]['x'], snake['body'][0]['y']))

    cur_p = data['you']['body'][0]
    cur_p = (cur_p['x'], cur_p['y'])

    options = []
    safe_options = []
    for vec, direction in MOVE_MAP:
        new_p = (cur_p[0]+vec[0], cur_p[1]+vec[1])
        if new_p[0] < 0 or new_p[0] >= data['board']['width']:
            continue
        if new_p[1] < 0 or new_p[1] >= data['board']['height']:
            continue
        if new_p in bad_locs:
            continue
        options.append((vec, direction))
        for head in heads:
            if abs(head[0]-new_p[0]) + abs(head[1]-new_p[1]) == 1:
                break
        else:
            safe_options.append((vec, direction))
    print(options)
    print(safe_options)
    if safe_options:
        vec, direction = random.choice(safe_options)
        print('Moving safe:', direction)
        return move_response(direction)
    if options:
        vec, direction = random.choice(options)
        print('Moving:', direction)
        return move_response(direction)

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
