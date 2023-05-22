from invtype_bases import GUIBase
from .database import PartsDatabase
from .signal_master import PartsSignalMaster


class PartsGUI(GUIBase):
    def __init__(self, database: PartsDatabase, sig_master: PartsSignalMaster):
        super().__init__(database, sig_master)


