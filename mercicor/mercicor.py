__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class Mercicor:

    def __init__(self, iface):
        _ = iface
        self.provider = None

    def initProcessing(self):
        if not self.provider:
            pass

    def initGui(self):
        self.initProcessing()

    def unload(self):
        pass
