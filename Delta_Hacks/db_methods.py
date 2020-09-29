import psycopg2
import json

with open('auth.json') as r:
    config = json.load(r)

class methods():
    def __init__(self, config):
        self.host = config['host']
        self.username = config['username']
        self.pw = config['password']
        self.port = config['port']
        self.dbname = config['database']
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.pw,
                port=self.port,
                database=self.dbname
            )
            print('database connected')

    def new_entry(self, first, last, birthday, provider, spot):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO queues(first,last,birthday,provider,spot)"
                    f"VALUES ('{first}','{last}','{birthday}','{provider}',{spot});")
        self.conn.commit()
        cur.close()

        print("new entry added")
    def new_spot(self):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT MAX(spot) "
                    f"FROM queues")
        max = cur.fetchone()
        if max[0] == None:
            max = 1
        else:
            max = max[0]+1
        cur.close()
        print("new person, now we have ", max)#issue on tupel + int
        return max

    def get_spot(self, first, last):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT spot FROM queues "
                    f"WHERE first = '{first}' AND last = '{last}';")
        spot = cur.fetchone()
        cur.close()
        return spot
        
    def total_infront(self, first, last):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT spot FROM queues "
                    f"WHERE first='{first}' AND last='{last}';")
        current_spot = cur.fetchone()
        if current_spot != None:
            cur.execute("SELECT * FROM queues "
                        f"WHERE spot < {current_spot[0]};")
            total_list = list(cur.fetchall())
            total = len(total_list)
            cur.close()
            print(total, " total")
            return total
        return 0

    def leave(self, first, last, spot):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("DELETE FROM queues "
                        f"WHERE first = '{first}' AND last = '{last}';")
        self.conn.commit()
        cur.close()
        print(first, last, "left")




