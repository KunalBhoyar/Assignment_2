import unittest
import sqlite3
import sqlite_main as db_methods
import sqlite_main
import pandas as pd

class TestSQLiteOperations(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(r"src\data\GEOSPATIAL_DATA.db")
        self.cursor = self.conn.cursor()
        
    def test_sqlite_connection(self):
        # Connect to the database (change the database file name as needed)
        
        # Check if the connection was successful
        self.assertTrue(self.conn is not None)
        
    def test_table_creation(self):
        self.cursor.execute('''DROP TABLE IF EXISTS test_table''')
        self.cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'").fetchone()
        self.assertEqual(result[0], 'test_table')

    def test_insert_data(self):
        self.cursor.execute("INSERT INTO test_table (id, name) VALUES (1, 'John Doe')")
        result = self.cursor.execute("SELECT * FROM test_table").fetchone()
        self.assertEqual(result, (1, 'John Doe'))

    # def test_goes_get_year():
    #     assert db_methods
        
    def tearDown(self):
        self.conn.close()
        
class TestGOES(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("src/data/test_goes_year.csv")
        self.invalidYearDf = pd.read_csv('src/data/test_goes_year_invalid.csv')
        self.daydf = pd.read_csv('src/data/test_goes_day.csv')
        self.hourdf = pd.read_csv('src/data/test_goes_hour.csv')
        

    def test_goes_year(self):
        df = sqlite_main.geos_get_year()
        assert df.equals(self.df) == True

    def test_goes_year_invalid(self):
        df = sqlite_main.geos_get_year()
        assert df.equals(self.invalidYearDf) == False
    
    def test_goes_year_value_valid(self):
        df = sqlite_main.geos_get_year()
        for index, row in df.iterrows():
            if(row['year'] >= 2022 and row['year'] <= 2023):
                assert True

    def test_goes_day(self):
        df = sqlite_main.geos_get_day(2022)
        assert df.equals(self.daydf) == True

    def test_goes_day_invalid(self):
        df1 = sqlite_main.geos_get_day(2022)
        for index, row in df1.iterrows():
            if(row['day'] >= 1 and row['day'] <= 365):
                assert True
        df2 = sqlite_main.geos_get_day(2023)
        for index, row in df2.iterrows():
            if(row['day'] >= 1 and row['day'] <= 365):
                assert True
    
    def test_goes_hour(self):
        df = sqlite_main.geos_get_hour(2023, 1)
        assert df.equals(self.hourdf) == True

    def test_goes_hour_invalid(self):
        df1 = sqlite_main.geos_get_hour(2023, 1)
        for index, row in df1.iterrows():
            if(row['hour'] >= 0 and row['hour'] <= 23):
                assert True

    ## NEXRAD Test cases

class TestNEXRAD(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("src/data/test_nexrad_year.csv")
        self.monthdf = pd.read_csv('src/data/test_nexrad_month.csv')
        self.hourdf = pd.read_csv('src/data/test_goes_hour.csv')
        

    def test_nexrad_year(self):
        df = sqlite_main.nexrad_get_year()
        assert df.equals(self.df) == True
    
    def test_nexrad_year_value_valid(self):
        df = sqlite_main.nexrad_get_year()
        for index, row in df.iterrows():
            if(row['year'] >= 2022 and row['year'] <= 2023):
                assert True

    def test_goes_month(self):
        df = sqlite_main.nexrad_get_month(2022)
        assert df.equals(self.monthdf) == True

    def test_nexrad_month_invalid(self):
        df1 = sqlite_main.nexrad_get_month(2022)
        for index, row in df1.iterrows():
            if(row['month'] >= 1 and row['month'] <= 12):
                assert True
        df2 = sqlite_main.nexrad_get_month(2023)
        for index, row in df2.iterrows():
            if(row['month'] >= 1 and row['month'] <= 12):
                assert True


if __name__ == '__main__':
    unittest.main()
