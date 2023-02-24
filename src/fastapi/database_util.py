import sqlite3
import json
from dotenv import load_dotenv
import os

load_dotenv()
class database_methods():
    def __init__(self):
        print (os.environ.get('DbUser'))
        conn = sqlite3.connect(os.environ.get('DbUser'))
        self.cursor_user = conn.cursor()
        self.cursor_user.execute('''CREATE TABLE IF NOT EXISTS USER (id INTEGER PRIMARY KEY AUTOINCREMENT ,username TEXT NOT NULL, password TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn_geo = sqlite3.connect(os.environ.get('DbGeo'))
        conn.commit()
        self.cursor_geo = conn_geo.cursor()
        
    def create_connection(self,database_name):
        conn = sqlite3.connect(os.environ.get('DbPath')+"/"+database_name+".db")
        cursor = conn.cursor()
        return conn,cursor
        
    def to_dict_list(self,rows, columns):
        return [dict(zip(columns, row)) for row in rows]

    def add_user(self,username,password):
        try:
            conn,cursor_user=self.create_connection('USER_DATA')
            cursor_user.execute("INSERT INTO USER (username, password) VALUES (?,?)", (username,password))
            conn.commit()
            conn.close()
            return "user_created"
        except Exception as e:
            print("add_user: "+str(e))
            return "failed_insert"
        
    
    def fetch_user(self,user_name):
        try:
            _,cursor_user=self.create_connection('USER_DATA')
            query=f"select * from USER where username='{user_name}'"
            cursor_user.execute(query)
            rows = cursor_user.fetchall()
            if len(rows)==0:
                return "no_user_found"
            else:
                print(self.return_json(rows,cursor_user))
                return self.return_json(rows,cursor_user)
        except Exception as e:
            return 'Exception'

    
    def return_json (self, rows,cursor):
        result = []
        for row in rows:
            d = dict(zip([col[0] for col in cursor.description], row))
            result.append(d)
        # Convert the list of dictionaries to a JSON string
        json_result = json.dumps(result)
        json_obj = json.loads(json_result)
        # Print the JSON string
        return(json_obj)

    #### Query for GOES ####
    
    def geos_get_year(self):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute('SELECT DISTINCT year from goes18meta')
        rows = cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    def geos_get_day(self,year):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT day from goes18meta where year={year}')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    def geos_get_hour(self,year, day):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT hour from goes18meta where year={year} and day={day}')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)
    
    #### Query for NEXRAD ####
    def nexrad_get_year(self):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT year from nexradmetadata')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    def nexrad_get_month(self,year):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT month from nexradmetadata where year={year}')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    def nexrad_get_day(self,year, month):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT day from nexradmetadata where year={year} and month={month}')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    def nexrad_get_sites(self,year, month, day):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT DISTINCT stationcode from nexradmetadata where year={year} and month={month} and day={day}')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)

    #nexrad sites

    def get_nexrad_sites(self):
        _,cursor_geo=self.create_connection('GEOSPATIAL_DATA')
        cursor_geo.execute(f'SELECT lat, lon from nexrad_sites_data')
        rows=cursor_geo.fetchall()
        return self.return_json(rows,cursor_geo)
