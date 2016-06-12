# store logic

snaps = {
    "baz": {
        "id": "baz-id",
        1: {"epoch": "0"}
        }
}

channel_map = {
}


def state_reset():
    channel_map.clear()


def setup(snap_name, **chan_map):
    snap = snaps[snap_name]
    snap_id = snap['id']
    for chan, revno in chan_map.items():
        snap_map = channel_map.setdefault(snap_name, {})
        snap_map[chan] = snap[revno].copy()
        snap_map[chan]['snap_id'] = snap_id
        snap_map[chan]['revision'] = revno


def search(q, channel):
    try:
        return channel_map[q][channel]
    except KeyError:
        return None
