from voeventhandler.voeventsorting import VoeventSorting
from voeventhandler.databaseinterface import DatabaseInterface
from voeventhandler.emailnotifier import EmailNotifier

class VoeventHandler(object):
    
    def __init__(self):
        self.db = DatabaseInterface()
        self.voevent_sorter = VoeventSorting()
        self.email_notifier = EmailNotifier()

    def handleVoevent(self, voevent):
        voeventdata = self.voevent_sorter.sort(voevent)
        self.db.insert_voevent(voeventdata)
        result_row = self.db.meange_correlated_instruments(voeventdata)
        self.email_notifier.sendEmails(voeventdata, result_row)
    
    def printVoevent(self, voevent):
        voeventdata = self.voevent_sorter.sort(voevent)
        print(voeventdata)