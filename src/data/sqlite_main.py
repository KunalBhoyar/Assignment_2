import os
import logging
import sqlite3
import pandas as pd
import pathlib as Path

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=LOGLEVEL,
    datefmt='%Y-%m-%d %H:%M:$S'
)

database_file_name = 'GEOSPATIAL_DATA.db'

goes_ddl_file_name = 'goes18meta.sql'
nexrad_ddl_file_name = 'nexradmetadata.sql'
nexrad_site_ddl_file_name = 'nexrad_sites_data.sql'

database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)

goes_ddl_file_path = os.path.join(os.path.dirname(__file__), goes_ddl_file_name)
nexrad_ddl_file_path = os.path.join(os.path.dirname(__file__), nexrad_ddl_file_name)
nexrad_site_ddl_file_path = os.path.join(os.path.dirname(__file__), nexrad_site_ddl_file_name)

def create_database():
    with open(goes_ddl_file_path, 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)   
    db.commit()

    with open(nexrad_ddl_file_path, 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)   
    db.commit()

    with open(nexrad_site_ddl_file_path, 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)   
    db.commit()

    db.close()

def check_database_initialization():
    print(os.path.dirname(__file__))
    if not Path.Path(database_file_path).is_file():
        logging.info(f"Database file not found, initilizing at: {database_file_path}")
        create_database()
    else:
        logging.info("Database file already exist!")

def query_into_dataframe():
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query('SELECT * from goes18meta', db)
    nex = pd.read_sql_query('SELECT * from nexradmetadata', db)
    nex_sites = pd.read_sql_query('SELECT * from nexrad_sites_data', db)
    logging.info(nex)
    logging.info(df)
    logging.info(nex_sites)

def geos_get_year():
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query('SELECT DISTINCT year from goes18meta', db)
    return df

def geos_get_day(year):
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query(f'SELECT DISTINCT day from goes18meta where year={year}', db)
    return df

def geos_get_hour(year, day):
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query(f'SELECT DISTINCT hour from goes18meta where year={year} and day={day}', db)
    return df

#nexrad -- year, month, hour, stationcode

def nexrad_get_year():
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query('SELECT DISTINCT year from nexradmetadata', db)
    return df

def nexrad_get_month(year):
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query(f'SELECT DISTINCT month from nexradmetadata where year={year}', db)
    return df

def nexrad_get_day(year, month):
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query(f'SELECT DISTINCT day from nexradmetadata where year={year} and month={month}', db)
    return df

def nexrad_get_sites(year, month, day):
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query(f'SELECT DISTINCT stationcode from nexradmetadata where year={year} and month={month} and day={day}', db)
    return df

#nexrad sites

def get_nexrad_sites():
    db = sqlite3.connect(database_file_path)
    df = pd.read_sql_query('SELECT lat, lon from nexrad_sites_data', db)
    return df


def main():
    check_database_initialization()
    query_into_dataframe()
    nexrad_get_sites(2022, 1, 1)
    # geos_get_year()


if __name__ == "__main__":
    logging.info('Script Starts')
    main()
    logging.info('Script Ends')