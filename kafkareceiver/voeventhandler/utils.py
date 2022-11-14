import re

class Utils:

    @staticmethod
    def triggerId_from_graceID(graceID):
        last = str(ord(graceID[-1]) - 96)
        result = re.sub("[^0-9]", "", graceID) + last.zfill(2)
        return result
    
    @staticmethod
    def graceID_from_triggerId(mission, triggerID):
        
        identity = triggerID
        mission = mission
        gw_alert_id = 0

        if mission == 'LIGO_TEST' or mission == 'LIGO':
            
            THRESHOLD = 4.0

            if mission == 'LIGO_TEST':
                char = 'MS'
            elif mission == 'LIGO':
                char = 'S'

            if len(identity[6:]) == 2:
                gw_alert_id = "%s%s%s" % (char, identity[:6], chr(int(identity[6:8])+96))
                #print("gw_alert_id = ", gw_alert_id)
            if len(identity[6:]) == 4:
                gw_alert_id = "%s%s%s%s" % (char, identity[:6], chr(int(identity[6:8])+96), chr(int(identity[8:10])+96))
                #print ("gw_alert_id = ", gw_alert_id)
            if len(identity[6:]) == 6:
                gw_alert_id = "%s%s%s%s%s" % (char, identity[:6], chr(int(identity[6:8])+96), chr(int(identity[8:10])+96), chr(int(identity[10:12])+96))
                #print ("gw_alert_id = ", gw_alert_id)
            if len(identity[6:]) == 8:
                gw_alert_id = "%s%s%s%s%s" % (char, identity[:6], chr(int(identity[6:8])+96), chr(int(identity[8:10])+96), chr(int(identity[10,12])+96), chr(int(identity[12,14])+96))
                #print("gw_alert_id = ", gw_alert_id)
                
        else:
            gw_alert_id = triggerID
        
        return gw_alert_id
