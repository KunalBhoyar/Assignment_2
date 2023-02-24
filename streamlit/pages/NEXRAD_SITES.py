import streamlit as st
import pandas as pd

import importlib.util
import os
from frontendAPICalls import *

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

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    sites_data = pd.DataFrame.from_dict(api_getNEXRADSitesLoc(st.session_state.logged_in))

    sites_data.rename(columns={"Lat": "lat", "Lon": "lon"}, inplace=True)

    st.map(sites_data)

if st.session_state.logged_in:
    main()
else:
    st.write('Please login to access this page!')