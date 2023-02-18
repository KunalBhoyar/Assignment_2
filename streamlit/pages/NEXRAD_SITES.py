import streamlit as st
import pandas as pd

import importlib.util
import os

current_directory = os.getcwd()

module_directory = os.path.abspath(os.path.join(current_directory, 'src', 'data'))
module_path = os.path.join(module_directory, 'sqlite_main.py')
ops_path = os.path.join(module_directory, 'backend_ops.py')

spec = importlib.util.spec_from_file_location("sqlite_main", module_path)
spec_ops = importlib.util.spec_from_file_location("backend_ops", ops_path)
db_methods = importlib.util.module_from_spec(spec)
ops = importlib.util.module_from_spec(spec_ops)
spec.loader.exec_module(db_methods)
spec_ops.loader.exec_module(ops)

st.title('Locations of all NEXRAD sites')

sites_data = db_methods.get_nexrad_sites()

sites_data.head()

sitedf = pd.DataFrame(
    {
        "lat": sites_data['Lat'],
        "lon": sites_data['Lon']
    }
)

st.map(sitedf)
