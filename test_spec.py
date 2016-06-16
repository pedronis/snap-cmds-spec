import support
import snap
import store
import disk


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

    def test_refresh_not_found(self):
        err = snap.refresh("baz")
        self.check_err_matches(err, '.*cannot find snap "baz".*')

    def test_refresh(self):
        store.setup("baz", stable=1)

        snap.install("baz")
        self.check_revision("baz", 1)

        err = disk.bin_run("baz")
        self.check_no_err(err)

        store.setup("baz", stable=2)

        snap.refresh("baz")
        self.check_revision("baz", 2)

        err = disk.bin_run("baz")
        self.check_no_err(err)

    def test_refresh_to_edge(self):
        store.setup("baz", stable=1, edge=2)

        snap.install("baz")
        self.check_revision("baz", 1)

        snap.refresh("baz", channel="edge")
        self.check_revision("baz", 2)

    def test_refresh_to_edge_and_back(self):
        # this is the current "buggy" behavior
        store.setup("baz", stable=1, edge=2)

        snap.install("baz")
        self.check_revision("baz", 1)

        err = disk.bin_run("baz")
        self.check_no_err(err)

        snap.refresh("baz", channel="edge")
        self.check_revision("baz", 2)

        err = disk.bin_run("baz")
        self.check_no_err(err)

        err = snap.refresh("baz", channel="stable")
        self.check_err_matches(err, '.*revision 1 of snap "baz" already installed.*')
