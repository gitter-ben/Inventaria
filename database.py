from core.signal_master import GlobalSignalMaster


class MainDatabase:
    def __init__(self, sig_master: GlobalSignalMaster, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._signal_master = sig_master
        self.saved = True

    def new(self, path):
        pass

    def close(self):
        pass
