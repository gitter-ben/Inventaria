from core.signal_master import MainSignalMaster
from core.utils import MainDBLoadError


class MainDatabase:
    def __init__(self, directory_path: str, sig_master: MainSignalMaster, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._signal_master = sig_master
        self.saved = True

        raise MainDBLoadError("Some error I guess, I don't really know")

    def new(self, path):
        pass

    def close(self):
        pass
