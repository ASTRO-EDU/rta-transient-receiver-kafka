import json
import mysql.connector
from datetime import datetime

class DatabaseInterface(object):

    def __init__(self):
        """
        This method is called when the class is instantiated.
        It create a connection to the database. 
        If cannot connect to the database, it raises an exception.
        Read database connection parameters from the config.json file.
        """

        f = open('voeventhandler/config/config.json')
        config = json.load(f)
        db_user = config['Database_user']
        db_password = config['Database_password']
        db_host = config['Database_host']
        db_port = config['Database_port']
        db_name = config['Database_name']
        
        try:
            self.cnx = mysql.connector.connect(user=db_user, password=db_password,
                            host=db_host, port=db_port, database=db_name)
            self.cursor = self.cnx.cursor()               
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password, please set the current parameter as env variable")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise err

    def insert_voevent(self, voevent):
        
        query = f"SELECT receivedsciencealertid FROM receivedsciencealert WHERE instrumentid = {voevent.instrument_id} AND triggerid = {voevent.trigger_id};"
        self.cursor.execute(query)
        check_rsa = self.cursor.fetchone()

        #insert in receivedsciencealert table if not already present
        #get id of the last row inserted
        if check_rsa is None:
            query = f'INSERT INTO receivedsciencealert (instrumentid, networkid, time, triggerid, ste) VALUES ({voevent.instrument_id}, {voevent.network_id}, {voevent.isoTime}, {voevent.trigger_id}, {voevent.is_ste});'
            self.cursor.execute(query)
            self.cnx.commit()

            receivedsciencealertid = self.cursor.lastrowid
        else:
            receivedsciencealertid = int(check_rsa[0]) 

        voevent.set_received_science_alert_id(receivedsciencealertid)


        #seqnum handling
        query = f"SELECT seqnum FROM notice n join receivedsciencealert rsa ON (rsa.receivedsciencealertid = n.receivedsciencealertid) WHERE last = 1 AND rsa.instrumentid = {voevent.instrument_id} AND rsa.triggerid = {voevent.trigger_id}"
        self.cursor.execute(query)
        result_seqnum = self.cursor.fetchone()

        try:
            seqNum = int(result_seqnum[0]) + 1 
        except:
            seqNum = 0
        
        pass
    
        voevent.set_seq_num(seqNum)

        #last handling
        query = f"UPDATE notice SET last = 0 WHERE last = 1 AND receivedsciencealertid = {voevent.receivedsciencealertid};"
        self.cursor.execute(query)
        self.cnx.commit()

        #insert in notice table
        noticetime = datetime.utcnow().isoformat(timespec="seconds")
        query = f"INSERT INTO notice (receivedsciencealertid, seqnum, l, b, error, contour, `last`, `type`, configuration, noticetime, notice, tstart, tstop, url, `attributes`, afisscheck) VALUES ({voevent.receivedsciencealertid}, {voevent.seqNum}, {voevent.l}, {voevent.b}, {voevent.position_error}, '{voevent.contour}', {voevent.last}, {voevent.packet_type}, '{voevent.configuration}', '{noticetime}', '{voevent.notice}', {voevent.tstart}, {voevent.tstop}, '{voevent.url}', '{voevent.ligo_attributes}', 0);"
        self.cursor.execute(query)
        self.cnx.commit()

    def meange_correlated_instruments(self, voeventdata):
        query = f"select ins.name,n.seqnum,n.noticetime,rsa.receivedsciencealertid, rsa.triggerid,rsa.ste,rsa.time as `trigger_time`,ste,notice,JSON_PRETTY(n.attributes) as `attributes` from notice n join receivedsciencealert rsa on ( rsa.receivedsciencealertid = n.receivedsciencealertid) join instrument ins on(ins.instrumentid = rsa.instrumentid) where  ins.name != '{voeventdata.name}' and rsa.instrumentid != 19 and rsa.time >= {voeventdata.isoTime - 10} and rsa.time <= {voeventdata.isoTime + 10} and n.seqnum = (select max(seqnum) from notice n2 join receivedsciencealert rsa2 on ( rsa2.receivedsciencealertid = n2.receivedsciencealertid)  where  rsa.triggerid = rsa2.triggerid ) order by n.noticetime"
        self.cursor.execute(query)
        results_row = self.cursor.fetchall()
        if results_row:
            for row in results_row:
                rsaid = row[3]
                
                try:
                    query = f"INSERT INTO correlations (rsaId1, rsaId2) VALUES({voeventdata.receivedsciencealertid}, {rsaid});"
                    self.cursor.execute(query)
                    self.cnx.commit()
                except:
                    pass

            """
            old query
            query = f"SELECT ins.name, max(n.seqnum),n.noticetime, n.receivedsciencealertid, rsa.triggerid,rsa.ste,rsa.time as `trigger_time` from notice n join correlations c on (n.receivedsciencealertid = c.rsaId2) join receivedsciencealert rsa on ( rsa.receivedsciencealertid = n.receivedsciencealertid) join instrument ins on (ins.instrumentid = rsa.instrumentid) where c.rsaId1 = {voeventdata.receivedsciencealertid} group by n.receivedsciencealertid"
            """
            #new query written by me couse the old one raise the exception: 
            #1055 (42000): Expression #3 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'kafka_alert_db.n.noticetime' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
            query = f"SELECT ins.name, max(n.seqnum),n.noticetime, n.receivedsciencealertid, rsa.triggerid, rsa.ste, rsa.time as `trigger_time` from notice n, correlations c, receivedsciencealert rsa, instrument ins WHERE n.receivedsciencealertid = c.rsaId2 AND rsa.receivedsciencealertid = n.receivedsciencealertid AND ins.instrumentid = rsa.instrumentid AND c.rsaId1 = {voeventdata.receivedsciencealertid} GROUP BY n.receivedsciencealertid, ins.name, n.noticetime;"

            self.cursor.execute(query)
            results_row = self.cursor.fetchall()
            return results_row
        else:
            return None