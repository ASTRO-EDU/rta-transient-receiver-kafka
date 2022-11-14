from voeventhandler.utilis.voeventdata import Voeventdata
from astropy.time import Time
import voeventparse as vp
import numpy as np

class TemplateDataExtractor(object):
    
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def extract(self, voevent) -> Voeventdata:
        is_ste = self.is_ste(voevent)
        instrument_id, name= self.get_instrumentID_and_name(voevent)
        trigger_id = self.get_triggerID(voevent)
        packet_type = self.get_packet_type(voevent)
        isoTime, UTC = self.get_time_from_voevent(voevent)
        network_id = self.get_networkID(voevent)
        l, b = self.get_l_b(voevent)
        position_error = self.get_position_error(voevent)
        notice = vp.prettystr(voevent)
        configuration = self.get_configuration(voevent)
        url = self.get_url(voevent)
        contour = self.get_contour(l, b, position_error, url)
        ligo_attributes = self.get_ligo_attributes(voevent) 
        
        seqNum = -1 #to be removed in the future couse should be set by a sql query
        tstart = 0
        tstop = 0
        last = 1

        #here need to be create a new class that store the previusly 
        #extracted data and return it
        return Voeventdata(self.datasource, is_ste, instrument_id, trigger_id,
                    packet_type, isoTime, UTC, network_id, l, b, position_error,
                    notice, configuration, url, contour, ligo_attributes,
                    name, seqNum, tstart, tstop, last)

    def is_ste(self, voevent) -> tuple:
        raise NotImplementedError

    def get_instrumentID_and_name(self, voevent):
        raise NotImplementedError

    def get_triggerID(self, voevent):
        raise NotImplementedError

    def get_packet_type(args, voevent):
        raise NotImplementedError

    def get_time_from_voevent(self, voevent):
        iso_time = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords.Time.TimeInstant.ISOTime.text
        t = Time(iso_time, format="fits", scale="utc")
        return np.round(t.unix - 1072915200), t.fits

    def get_networkID(self, voevent):
        raise NotImplementedError

    def get_l_b(self, voevent):
        raise NotImplementedError

    def get_position_error(self, voevent):
        raise NotImplementedError

    def get_configuration(self, voevent):
        raise NotImplementedError

    def get_url(self, voevent):
        raise NotImplementedError

    def get_contour(self, l, b, url):
        raise NotImplementedError

    def get_ligo_attributes(self, voevent):
        raise NotImplementedError

    def __repr__(self):
        return "class for data extraction from: %s"% (self.datasource)

    def __str__(self):
        return "class for data extraction from: %s"% (self.datasource)