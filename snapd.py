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
    return do_install(name, channel)


# matches snapstate.Upgrade
def update(name, channel=None):
    snapst = get_snapst(name)
    if snapst.current() is None:
        return 'cannot find snap "%s"' % name

    if not channel:
        channel = snapst.channel

    # XXX: atm update is implemented as an install in the real snapd!
    return do_install(name, channel)


def do_install(name, channel):
    rsnap = store.snap(name, channel or "stable")
    if not rsnap:
        return "snap not found"

    snapst = get_snapst(name)
    for si in snapst.sequence:
        if si['revision'] == rsnap['revision']:
            return 'revision %s of snap "%s" already installed' % (rsnap['revision'], name)

    snapst.active = True
    snapst.sequence.append(rsnap)
    if channel:
        snapst.channel = channel
    snaps[name] = snapst
