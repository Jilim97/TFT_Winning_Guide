import streamlit as st
import mysql.connector
from PIL import Image
import pandas as pd
import io
import ast
import subprocess


st.set_page_config(
    page_title="TFT Winning Guide 1.0.0",
    layout="centered",
    )

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='j!hwanl!m97', database='TFT')
cursor = cnx.cursor()

# Define query to retrieve data from Game table
# Augments has dictionary form {aug1:A,aug2:B,aug3:C} -> Find pattern inside
query = """
SELECT Game_ID, Player_ID, Placement, Augments, Deck_Name, Traits, Champions 
FROM TFT.Game_Record
WHERE Augments LIKE %s AND Augments LIKE %s AND Augments LIKE %s 
AND Placement >= %s AND  Placement <= %s 
"""

# Need apiName for loading image (Image files are downloaded same webpage from eu_us.json)
items =pd.read_csv("/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/items.csv")
item_aug_list = {items.loc[i, 'apiName'] : items.loc[i, 'name'] for i in range(items.shape[0])}
item_dict = {items.loc[i, 'apiName'] : items.loc[i, 'icon_Lower'] for i in range(items.shape[0])}



# Get user input for Augment filter
augment_filter_1 = st.sidebar.text_input('Enter Augment 1:', '')
augment_filter_2 = st.sidebar.text_input('Enter Augment 2:', '')
augment_filter_3 = st.sidebar.text_input('Enter Augment 3:', '')
placement_range = st.sidebar.slider('Select placement range', 1, 8, (1, 4))


# Execute query with user input
if augment_filter_1 != '' or augment_filter_2 != '' or augment_filter_3 != '':
    cursor.execute(query, (f"%{augment_filter_1}%", f"%{augment_filter_2}%", f"%{augment_filter_3}%",placement_range[0], placement_range[1]))
    key_num = 0
    st.write("# TFT Winning Guide")
    # Display results in a table with clickable links to related data
    for (Game_ID, Player_ID, Placement, Augments, Deck_Name, Traits, Champions) in cursor:
        key_num += 1 # Make specific key number for button

        # str to dict and list
        Champions = ast.literal_eval(Champions)
        Augments = ast.literal_eval(Augments)
        Traits = ast.literal_eval(Traits)
        
        if len(Champions) > 0:
            # Make Title row for Deck Name
            column_title = st.columns([3,1])
            column_title[0].write(f"## {Deck_Name}")

            num = len(Champions)
            my_list = [2] + [1 for i in range(num)]
            # Make rows for Deck information (Champions, itmes, champion tier, Player id, Deck guide, Match info)
            columns = st.columns(my_list)
           
            # Make augment row
            colums_a = st.columns([1,1,1])
            columns_aug = st.columns([1,1,1])

            # Connect to other data
            Deck_button = columns[0]
            Player_button = columns[0]
            Match_button = columns[0]

            # Load other tables
            with Deck_button:
                if st.button("Deck Guide", key=key_num):
                    subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/deck.py', Deck_Name])

            with Player_button:
                if st.button("Player",key=f"{Player_ID}{key_num}"):
                    subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/player.py', Player_ID])

            with Match_button:
                if st.button("Match info",key=f"{Game_ID}{key_num}"):
                    subprocess.call(['streamlit', 'run', '/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/game.py', Game_ID])
            
            columns[0].write(f"##### Rank: {Placement}")

            colums_a[0].write("###### Augment 1: ")
            columns_aug[0].write(Augments['augment1'])
            colums_a[1].write("###### Augment 2: ")
            columns_aug[1].write(Augments['augment2'])
            colums_a[2].write("###### Augment 3: ")
            columns_aug[2].write(Augments['augment3'])

            column_len = 1
            for i, (trait, data) in enumerate(Traits.items()):
                tier = data['tier_current']
                if tier != 0:
                    column_len += 1
                else:
                    pass

            colums_t = st.columns(1)
            columns_trait = st.columns([1 for i in range(column_len)])

            colums_t[0].write("###### Activated Synergy:")
            trait_index = 0
            for i, (trait, data) in enumerate(Traits.items()):

                tier = data['tier_current']
                if tier != 0:
                    columns_trait[trait_index].write(trait + f" {tier} tier")
                    trait_index += 1
                else:
                    pass

            # Load champion and item data
            for i, (champion, data) in enumerate(Champions.items()):
                items_list = data['items']
                tier = data['tier_current']

                img_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/tft/{champion}.png" 
                with open(img_file, "rb") as f:
                    img_data = f.read()
                img = Image.open(io.BytesIO(img_data))

                star_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/tft/{tier}.png"
                with open(star_file, "rb") as f:
                    star_data = f.read() 
                star = Image.open(io.BytesIO(star_data))
                columns[i+1].image(img, caption=champion)
                columns[i+1].image(star)
                columns[i+1].write("###### Items:")

                for k in items_list:
                    item = item_dict[k]
                    item_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/{item}"
                    with open(item_file, "rb") as f:
                        item_data = f.read() 
                    item_img = Image.open(io.BytesIO(item_data))
                    columns[i+1].image(item_img, width=30)
 
        else:
            pass
else:
    # Display message if no filter is provided
    st.write("# TFT Winning Guide")

    st.markdown(
    """
    ## BATTLE FOR THE CONVERGENCE
    Draft, deploy, and dominate with a revolving roster of League of Legends champions in a round-based battle for supremacy. Outsmart your opponents and adapt as you go the strategy is all up to you.
    
    ### Check out the links 
    - Download [TFT](https://teamfighttactics.leagueoflegends.com/en-gb/?utm_source=riotbar&utm_medium=productcard%2Bwww.leagueoflegends.com&utm_campaign=tft&utm_content=tft_keyart_set8release)
    - Check out [Patch_Note](https://www.leagueoflegends.com/en-pl/news/tags/patch-notes/)
    """
    )
    Main_file = f"/Users/jihwanlim/Desktop/Ghent/Msc/DB/Final_Data/tft/TFT_Main.jpeg" # Replace with actual URL of image
    with open(Main_file, "rb") as f:
        main_data = f.read()
    main = Image.open(io.BytesIO(main_data))
    st.image(main, width=1000)

    


# Close database connection
cursor.close()
cnx.close()

