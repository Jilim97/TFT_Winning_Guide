import streamlit as st
import mysql.connector
from PIL import Image
import pandas as pd
import io
import ast
import sys

player = sys.argv[1] # Search input from Main.py

st.write("# {}".format(player))

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='j!hwanl!m97', database='TFT')
cursor = cnx.cursor()

# Search information with player puuid
query = """
SELECT Tier, League_Points, Wins, Losses, Win_Rate
FROM TFT.summoner_record
WHERE Player_ID = %s
"""
st.write("# Player info")

cursor.execute(query, (f"{player}",))

for (Tier, League_Points, Wins, Losses , Win_Rate) in cursor:
    columns = st.columns(2)

    tier_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/tft/{Tier}.png" # Tier image
    with open(tier_file, "rb") as f:
        tier_data = f.read()
    img = Image.open(io.BytesIO(tier_data))
    columns[0].image(img, caption = Tier)
    columns[1].write(f"### League Points: {League_Points}pt")
    columns[1].write(f"### Wins: {Wins}")
    columns[1].write(f"### Losses: {Losses}")
    columns[1].write("### Win Rate : {:.3f}%".format(Win_Rate))

cursor.close()
cnx.close()
