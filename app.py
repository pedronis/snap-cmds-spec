# snap app behaviors

import store
import disk

version_to_epoch = {}


def init():
    for name, about in store.snaps.items():
        m = version_to_epoch[name] = {}
        for k, v in about.items():
            if k == 'id':
                continue
            m[v['version']] = v['epoch']

init()


def compatible_epochs(e1, e2):
    if e1 == e2:
        return True
    if e2.endswith('*'):
        e2i = int(e2[:-1])
        if compatible_epochs(str(e2i), e1) or compatible_epochs(str(e2i-1), e1):
            return True
    return False


# defines app baz of snap baz
def baz_baz(env):
    d = disk.data_dirs[env["SNAP_DATA"]]
    ver = env["SNAP_VERSION"]
    epoch = version_to_epoch["baz"][ver]
    disk.data_dirs[env["SNAP_DATA"]] = {'V': ver, 'E': epoch}
    if d is not None:
        # check potential data incompability
        old_ver = d['V']
        old_epoch = d['E']
        if old_ver <= ver:
            # forward
            if not compatible_epochs(old_epoch, epoch):
                return "forward: imcompatible epochs"
        else:
            # backward
            if not compatible_epochs(old_epoch, epoch):
                return "backward: imcompatible epochs"
            else:
                return "backward"
