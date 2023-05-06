import streamlit as st
import mysql.connector
from PIL import Image
import pandas as pd
import io
import ast
import sys
import subprocess


Game_id = sys.argv[1]

st.write("# {}".format(Game_id))

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='j!hwanl!m97', database='TFT')
cursor = cnx.cursor()

query = """
SELECT Datetime, ingame_duration, Game_type, Participants
FROM TFT.Match_record
WHERE Game_id = %s
"""
st.write("# Match info")

cursor.execute(query, (f"{Game_id}",))

for (Datetime, ingame_duration, Game_type, Participants) in cursor:
    Participants = ast.literal_eval(Participants)
    columns = st.columns(3)


    Player_button1 = columns[0]
    with Player_button1:
        if st.button("Player1"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[0]])

    Player_button2 = columns[0]
    with Player_button2:
        if st.button("Player2"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[1]])
    
    Player_button3 = columns[0]
    with Player_button3:
        if st.button("Player3"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[2]])
    
    Player_button4 = columns[0]
    with Player_button4:
        if st.button("Player4"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[3]])
    
    Player_button5 = columns[0]
    with Player_button5:
        if st.button("Player5"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[4]])
    
    Player_button6 = columns[0]
    with Player_button6:
        if st.button("Player6"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[5]])
    
    Player_button7 = columns[0]
    with Player_button7:
        if st.button("Player7"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[6]])

    Player_button8 = columns[0]
    with Player_button8:
        if st.button("Player8"):
            subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Participants[7]])

    columns[1].write(f"### Datetime: {Datetime}")
    columns[1].write(f"### Ingame Duration: {ingame_duration} m")
    columns[1].write(f"### Game Type: {Game_type}")


cursor.close()
cnx.close()
