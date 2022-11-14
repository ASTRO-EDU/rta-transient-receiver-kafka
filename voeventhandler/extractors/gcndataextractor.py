from voeventhandler.extractors.templatedataextractor import TemplateDataExtractor
from voeventhandler.utilis.instrumentid import InstrumentId
from voeventhandler.utilis.voeventdata import Voeventdata
from astropy.coordinates import SkyCoord
from astropy import units as u
import voeventparse as vp
import math

class GncDataExtractor(TemplateDataExtractor):


    def __init__(self) -> None:
        super().__init__("gnc")

    def extract(self, voevent) -> Voeventdata:
        return super().extract(voevent)

    def is_ste(self, voevent):
        return 0
    
    def get_instrumentID_and_name(self, voevent) -> tuple:
        packet_type = int(voevent.What.Param[0].attrib["value"])
        if packet_type in [53,54,55]: # INTEGRAL FROM GCN
            return InstrumentId.INTEGRAL.value, "INTEGRAL"
        elif packet_type == 97: #SWIFT 
            return InstrumentId.SWIFT.value, "SWIFT"
        elif packet_type == 111:  #FERMI_GBM 
            return InstrumentId.FERMI_GBM.value, "FERMI_GBM"
        elif packet_type in [125,128]: #FERMI_LAT 
            return InstrumentId.FERMI_LAT.value, "FERMI_LAT"
        elif packet_type == 105: #AGILE_MCAL FROM GCN
            return InstrumentId.AGILE_MCAL.value, "AGILE_MCAL"
        elif packet_type in [150, 151, 152, 163]: #LIGO and LIGO_TEST TBD
            if  "test" in voevent.attrib['role']:
                return InstrumentId.LIGO_TEST.value, "LIGO_TEST"
            if  "observation" in voevent.attrib['role']:
                return InstrumentId.LIGO.value, "LIGO"
        elif packet_type == 158: #ICECUBE_HESE
            return InstrumentId.ICECUBE_HESE.value, "ICECUBE_HESE"
        elif packet_type == 169: #ICECUBE_EHE
            return InstrumentId.ICECUBE_EHE, "ICECUBE_EHE"
        elif packet_type == 173: #ICECUBE_ASTROTRACK_GOLD
            return InstrumentId.ICECUBE_ASTROTRACK_GOLD.value, "ICECUBE_ASTROTRACK_GOLD"
        elif packet_type == 174: #ICECUBE_ASTROTRACK_BRONZE
            return InstrumentId.ICECUBE_ASTROTRACK_BRONZE.value, "ICECUBE_ASTROTRACK_BRONZE"
        elif packet_type == 59: #KONUS
            return InstrumentId.KONUS.value, "KONUS"
        elif packet_type == 134: #MAXI_UNKNOWN
            return InstrumentId.MAXI_UNKNOWN.value, "MAXI_UNKNOWN"
        elif packet_type == 135: #MAXI_KNOWN
            return InstrumentId.MAXI_KNOWN.value, "MAXI_KNOWN"
        else:
            raise Exception(f"Voevent with packet type {packet_type} not supported")

    def get_triggerID(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        return top_params["TrigID"]["value"]

    def get_packet_type(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        return top_params["Packet_Type"]["value"]

    def get_networkID(self, voevent):
        return 1

    def get_l_b(self, voevent):
        ra = float(voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords.Position2D.Value2.C1.text)
        dec = float(voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords.Position2D.Value2.C2.text)
        c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
        return c.galactic.l.degree, c.galactic.b.degree

    def get_position_error(self, voevent):
        return float(voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords.Position2D.Error2Radius.text)

    def get_configuration(self, voevent):
        return "None"

    
    def get_ligo_attributes(self, voevent):
        return {}

    def get_contour(self, l, b, error, url):
        """
        utilized code from https://github.com/ASTRO-EDU/AlertReceiver_GCNnetwork/blob/117ce436b7003af14843cd6fd97ed0c0e1d90eb5/gcn/alert.c#L161
        """
        if l == 0 and b == 0:
            return 0
        l = 0
        b = 0
        r = error
        delta = 0
        if (r < 0.0000001):
            r = 0.1
        steps = int(10. + 10. * r)

        contour = ""

        for i in range(steps):
            l = l - r * math.cos(delta)
            b = b + r * math.sin(delta)
            if (l < 0):
                l = 0
            elif(l >= 360):
                l = 360
            elif (l == 0):
                l = 0
            if (b < -90):
                b = -90
            elif (b > 90):
                b = 90
            elif (b == 0):
                b = 0
                
            delta = delta - 2 * math.pi / steps

            contour = contour + f"{l} {b}\n"
        return contour

    def get_url(self, voevent):
        return "none"