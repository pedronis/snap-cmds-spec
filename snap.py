# snap cmd
import snapd


def install(snap, channel=None):
    return snapd.install(snap, channel=channel)


def refresh(snap, channel=None):
    return snapd.update(snap, channel=channel)
