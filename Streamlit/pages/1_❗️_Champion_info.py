import streamlit as st
import mysql.connector
from PIL import Image
import pandas as pd
import io

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='j!hwanl!m97', database='TFT')
cursor = cnx.cursor()

query = """
SELECT champion, cost, trait1, triat2, trait3
FROM TFT.champion
"""

st.write("# Champion info")
st.text_input("Search Champion",'Sylas')

columns = st.columns([2,1,1,1,1])
columns[0].write("## Champion")
columns[1].write("## Cost")
columns[2].write("## Trait1")
columns[3].write("## Trait2")
columns[4].write("## Trait3")

cursor.execute(query,)

for (champion, cost, trait1, triat2, trait3) in cursor:

    columns = st.columns([2,1,1,1,1])

    img_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/tft/{champion}.png" # Replace with actual URL of image
    with open(img_file, "rb") as f:
        img_data = f.read()
    img = Image.open(io.BytesIO(img_data))
    columns[0].image(img, caption=champion)
    columns[1].write(f"# {cost}")
    columns[2].write(f"#### {trait1}")
    if triat2 != 'None':
        columns[3].write(f"#### {triat2}")
        if trait3 != 'None':
            columns[4].write(f"#### {trait3}")
        else:
            pass
    else:
        pass
        

cursor.close()
cnx.close()
