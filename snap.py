# snap logic
import snapd


def install(snap, channel=None):
    return snapd.install(snap, channel=channel)
