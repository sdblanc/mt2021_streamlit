import streamlit as st

from Experiment_1 import Experiment_1
from Experiment_2 import Experiment_2

st.set_page_config(page_title="MT - Silas Deblanc")
st.sidebar.subheader("Navigation")

pages = {'Experiment 1': Experiment_1,'Experiment 2':Experiment_2}
choice = st.sidebar.radio("Choice your page: ",tuple(pages.keys()))

pages[choice]()

