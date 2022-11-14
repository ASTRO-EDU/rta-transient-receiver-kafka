from voeventhandler.extractors.agiledataextractor import AgileDataExtractor
from voeventhandler.extractors.chimedataextractor import ChimeDataExtractor
from voeventhandler.extractors.gcndataextractor import GncDataExtractor
from voeventhandler.extractors.integraldataextractor import IntegralDataExtractor
from voeventhandler.extractors.ligodataextractor import LigoDataExtractor

class VoeventSorting(object):
    def __init__(self) -> None:
        self.agile = AgileDataExtractor()
        self.chime = ChimeDataExtractor()
        self.gcn = GncDataExtractor()
        self.integral = IntegralDataExtractor()
        self.ligo = LigoDataExtractor()

    def sort(self, voevent):
        if "gcn" in voevent.attrib['ivorn']:
            return (self.gcn.extract(voevent))
        elif "gwnet" in voevent.attrib['ivorn']:
            return (self.ligo.extract(voevent))
        elif "chimenet" in voevent.attrib['ivorn']:
            return (self.chime.extract(voevent))
        elif "INTEGRAL" in voevent.attrib['ivorn']:
            return (self.integral.extract(voevent))
        elif "AGILE" in voevent.attrib['ivorn']:
            return (self.agile.extract(voevent))
        else:
            raise Exception(f"Notice not supported  ivorn is {self.voevent.attrib['ivorn']}")