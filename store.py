# store logic

snaps = {
    "baz": {
        "id": "baz-id",
        1: {"version": "v1", "epoch": "0"},
        2: {"version": "v2", "epoch": "0"}
        }
}

channel_map = {}
id_to_name = {}


def state_reset():
    channel_map.clear()
    id_to_name.clear()


def setup(snap_name, **chan_map):
    snap = snaps[snap_name]
    snap_id = snap['id']
    id_to_name[snap_id] = snap_name
    for chan, revno in chan_map.items():
        snap_map = channel_map.setdefault(snap_name, {})
        snap_map[chan] = snap[revno].copy()
        snap_map[chan]['snap_id'] = snap_id
        snap_map[chan]['revision'] = revno


def snap(name, channel):
    try:
        rsnap = channel_map[name][channel]
    except KeyError:
        return None
    rsnap = rsnap.copy()
    rsnap['revision'] = str(rsnap['revision'])
    return rsnap
