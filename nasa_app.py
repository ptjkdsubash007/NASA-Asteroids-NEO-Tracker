
from PIL import Image
import streamlit as st
import datetime

pages={"Asteroids NEO TRACKER":[st.Page("Asteroids.py", title='Filter Asteroids',icon=":material/tune:")],
        "":[st.Page("Queries.py", title='Queries',icon=':material/note:')]}

pg=st.navigation(pages)
st.set_page_config(page_title="Asteroids NEO TRACKER",page_icon=":material/planet:",layout='wide')
pg.run()





