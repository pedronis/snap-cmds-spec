# snapd logic
import store

snaps = {}


def state_reset():
    snaps.clear()


class SnapState(object):

    def __init__(self):
        self.active = False
        self.channel = ""
        self.sequence = []

    def current(self):
        if len(self.sequence):
            return self.sequence[-1]
        return None


def get_snapst(snap_name):
    return snaps.get(snap_name, SnapState())


# matches snapstate.Install
def install(name, channel=None):
    snapst = get_snapst(name)
    if snapst.current() is not None:
        return 'snap "%s" already installed' % name

    channel = channel or "stable"
    rsnap = store.search(name, channel)
    if not rsnap:
        return "snap not found"

    snapst.active = True
    snapst.sequence.append(rsnap)
    snapst.channel = channel
    snaps[name] = snapst
