# on disk: data and looking up executables
import snap
import app

snap_dirs = {}
data_dirs = {}


def state_reset():
    snap_dirs.clear()
    data_dirs.clear()


def bin_run(name):
    return snap.run(name)


def bin_lookup(snap_name_revno, app_name):
    # for now assume the executable is the same across revisions
    snap_name = snap_name_revno.split('/')[0]
    return getattr(app, "%s_%s" % (snap_name, app_name))
