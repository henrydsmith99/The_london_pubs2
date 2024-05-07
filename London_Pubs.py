'''
Name: Henry Smith
CS230: Section 5
Data: London Pubs
URL:
Description: This program filters the london pubs database and opens a variety of visualizations about the data.

'''
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np


path = "C:/Users/henry/pythonProject/"

df_pubs = pd.read_csv(path + "open_pubs_10000_sample.csv")


#[DA1] - cleaning the data
df_pubs['latitude'] = pd.to_numeric(df_pubs['latitude'], errors='coerce')   # converting data to numeric type, section 1 of AI report
df_pubs['longitude'] = pd.to_numeric(df_pubs['longitude'], errors='coerce') # converting data to numeric type


#[DA9]
np.random.seed(42)
df_pubs['rating'] = np.random.randint(1, 101, df_pubs.shape[0]) #see AI report section 2


#[DA2]- sorting data by descending order column
#[DA3]- Top largest or smallest values of a column
#[PY3] - Function called upon two times
def local_authority_count(data):

    count_df_pubs=data['local_authority'].value_counts()
    sorted_counts= count_df_pubs.sort_values(ascending=False) # orders pubs in decending order, with the most at the top.
    top_count = sorted_counts.index[0] # returns the index of the top value
    return(top_count)

# [DA4] - Filtering data by one condition

def filter_postcode(data, specific_postcode):
    only_postcode=data[data["postcode"]]==specific_postcode
    return only_postcode

# [DA5] - Filtering data by two or more conditions with AND or OR
# [PY1]
def filter_local_authority_postcode(data, specific_post,specific_LA=local_authority_count(df_pubs)):
    filtered_pubs=df_pubs[(df_pubs['local_authority']==specific_LA)& df_pubs['postcode']==specific_post]
    return filtered_pubs

#[PY4]
def names_list(data):
    names_list= [name for name in data['name']]
    return names_list

#[PY2]
def get_mean_lat_lon(df):
    return df['latitude'].mean(), df['longitude'].mean()
#[VIZI 1]
def pub_map(data):
    sort_authorities= np.sort(df_pubs['local_authority'].unique()) #alphabatizes the authorities show they show up in the right order for the dropdown.
    #[ST1] - drop down
    select_local_authority = st.selectbox('Select a Local Authority:', sort_authorities) #creates dropdown to select local authority

    #[ST2] - slider
    min_rating = st.sidebar.slider('Minimum Rating', min_value=1, max_value=100, value=50)

    filtered_data= df_pubs[(df_pubs['local_authority'] == select_local_authority) &(df_pubs['rating']>=min_rating)]
    if filtered_data.empty:
        st.warning ("No pubs meet the specified conditions.")
    #[VIZ1] - creating a scatterplot map
    else:
        st.title("Scatterplot Map")

        # Map view state initialization
        view_state = pdk.ViewState(
            latitude=filtered_data['latitude'].astype(float).mean(),
            longitude=filtered_data['longitude'].astype(float).mean(),
            zoom=9,
            pitch=0
        )
        # Define tooltip to show data on hover
        tool_tip = {
            "html": "<b>Name:</b> {name}<br/> <b>Address:</b> {address}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }

        # Define layers for the map
        layer1 = pdk.Layer(
            'ScatterplotLayer',
            filtered_data,
            get_position='[longitude, latitude]',
            get_radius=500,
            get_color=[0, 200, 0],
            pickable=True
        )

        layer2 = pdk.Layer(
            'ScatterplotLayer',
            filtered_data,
            get_position='[longitude, latitude]',
            get_radius=300,
            get_color=[0, 0, 255],
            pickable=True
        )

        # Create the deck.gl map
        map = pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v12',
            initial_view_state=view_state,
            layers=[layer1, layer2],
            tooltip=tool_tip
        )

    # Display the map in the Streamlit app
        st.pydeck_chart(map)

        max_rating = filtered_data['rating'].max() # gets max rating from filtered_data

        highest_rated_pub = filtered_data[filtered_data['rating'] == max_rating] # find row where ratings equals the max_rating

    # Display the result
        pub_name = highest_rated_pub['name'].iloc[0]  # .iloc[0] to get the value from the first row, in case there are multiple
        local_authority = highest_rated_pub['local_authority'].iloc[0]
        rating = highest_rated_pub['rating'].iloc[0]  # ratings column

        message = f"The highest rated pub in {local_authority} is {pub_name} with a {rating} rating."
        st.write(message)
        #[ST3] [VIZI1]
        if st.checkbox ('Show Raw Data'):
            st.write(filtered_data)

def main():
    st.title("London Pubs")
    pub_map(df_pubs)
    print(df_pubs)
    print(names_list(df_pubs))
main()