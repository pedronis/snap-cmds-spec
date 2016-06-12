import support
import snap
import store


class TestScenarios(support.ScenarioSupport):

    def test_snap_not_found(self):
        err = snap.install("baz")
        self.check_err_matches(err, ".*snap not found.*")

    def test_install(self):
        store.setup("baz", stable=1)

        snap.install("baz")
        self.check_revision("baz", 1)

    def test_already_installed(self):
        store.setup("baz", stable=1)

        snap.install("baz")
        self.check_revision("baz", 1)

        err = snap.install("baz")
        self.check_err_matches(err, '.*snap "baz" already installed.*')
