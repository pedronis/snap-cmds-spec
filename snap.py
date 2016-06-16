# snap cmd
import snapd
import disk


def run(name):
    if '.' in name:
        snap_name, app_name = name.split('.')
    else:
        snap_name, app_name = name, name

    # cheating, looking into snapd details
    snapst = snapd.get_snapst(snap_name)
    if snapst is None:
        raise Exception("cannot find snap %s" % snap_name)
    revision = snapst.current()['revision']

    which = "%s/%s" % (snap_name, revision)
    ver = disk.snap_dirs[which]['version']

    executable = disk.bin_lookup(which, app_name)

    env = {
        "SNAP_REVISION": revision,
        "SNAP_VERSION": ver,
        "SNAP_DATA": which,
    }
    return executable(env)


def install(snap, channel=None):
    return snapd.install(snap, channel=channel)


def refresh(snap, channel=None):
    return snapd.update(snap, channel=channel)
