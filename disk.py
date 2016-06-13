import bin
import snapd

snap_dirs = {}
data_dirs = {}


def state_reset():
    snap_dirs.clear()
    data_dirs.clear()


def run(name):
    snapst = snapd.get_snapst(name)
    if snapst is None:
        raise Exception("cannot find script for %s" % name)

    revision = snapst.current()['revision']
    script = getattr(bin, name)
    ver = snap_dirs["%s/%s" % (name, revision)]['version']

    env = {
        "SNAP_REVISION": revision,
        "SNAP_VERSION": ver,
        "SNAP_DATA": "%s/%s" % (name, revision)
    }
    return script(env)
