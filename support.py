import unittest
import store
import snapd
import disk


class ScenarioSupport(unittest.TestCase):

    def setUp(self):
        store.state_reset()
        snapd.state_reset()
        disk.state_reset()

    def check_no_err(self, err):
        self.assertIsNone(err)

    def check_err_matches(self, err, regexp):
        if not err:
            self.fail("expected error, got %s" % err)
        self.assertRegex(err, regexp)

    def check_revision(self, snap_name, revision):
        snap = snapd.snaps.get(snap_name)
        if not snap:
            self.fail("%s not present" % snap_name)
        if not snap.active:
            self.fail("%s not active" % snap_name)
        if not snap.sequence or snap.sequence[-1]["revision"] != str(revision):
            self.fail("%s not at revision %s" % (snap_name, revision))
