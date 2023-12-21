from itertools import zip_longest


def fix_wiring(cables, sockets, plugs):
    return (
        f"{'plug' if plug else 'weld'} {cable} {'into' if plug else 'to'} "
        f"{socket} {f'using {plug}' if plug else 'without plug'}"
        for cable, socket, plug in
        zip_longest(
            [cable for cable in cables
                if isinstance(cable, str) and cable.startswith('cable')],
            [socket for socket in sockets
                if isinstance(socket, str) and socket.startswith('socket')],
            [plug for plug in plugs
                if isinstance(plug, str) and plug.startswith('plug')])
        if cable and socket
    )


if __name__ == "__main__":
    plugs = ['plug1', 'plug2', 'plug3']
    sockets = ['socket1', 'socket2', 'socket3', 'socket4']
    cables = ['cable1', 'cable2', 'cable3', 'cable4']

    for c in fix_wiring(cables, sockets, plugs):
        print(c)
