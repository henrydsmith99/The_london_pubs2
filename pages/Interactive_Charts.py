import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import pandas as pd
import random as rd
import numpy as np
import seaborn as sns


path = "C:/Users/henry/pythonProject/"
# Load data
df_pubs = pd.read_csv(path + "open_pubs_10000_sample.csv")
st.set_option('deprecation.showPyplotGlobalUse', False)

#[DA1] - cleaning the data
df_pubs['latitude'] = pd.to_numeric(df_pubs['latitude'], errors='coerce')   # converting data to numeric type
df_pubs['longitude'] = pd.to_numeric(df_pubs['longitude'], errors='coerce') # converting data to numeric type

#[DA9]
np.random.seed(42)
df_pubs['rating'] = np.random.randint(1, 101, df_pubs.shape[0])

#[VIZI2]
def top10_chart(data):
    pub_counts = data['local_authority'].value_counts()

    # Sort the counts in descending order
    sorted_pub_counts = pub_counts.sort_values(ascending=False)

    # Select the top 10 local authorities using .iloc
    top_pub_counts = sorted_pub_counts.iloc[:10]

    # Create a bar chart
    plt.figure(figsize=(12, 8))
    top_pub_counts.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Local Authorities by Pub Count')
    plt.xlabel('Local Authority')
    plt.ylabel('Number of Pubs')
    plt.xticks(rotation=50) # rotates the labels, so they are more legible.
    plt.grid(True, axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Display the plot
    st.pyplot(plt)



def ratings_chart(data):
    st.title("Interactive Location Filter and Bar Chart of Ratings")

    # Use a multiselect widget to let the user select multiple local authorities
    all_authorities = np.sort(df_pubs['local_authority'].unique())
    selected_authorities = st.multiselect('Select Local Authorities:', all_authorities, default=all_authorities[0])

    if selected_authorities:
        # Filter data based on the selected local authorities
        filtered_data = df_pubs[df_pubs['local_authority'].isin(selected_authorities)]

        if not filtered_data.empty:
            # Optionally, you can use groupby to aggregate ratings, here's how to get the average rating per local authority
            authority_ratings = filtered_data.groupby('local_authority')['rating'].mean().reset_index()

            # Plotting
            plt.figure(figsize=(10, 5))
            plt.bar(authority_ratings['local_authority'], authority_ratings['rating'], color='skyblue')
            plt.xlabel('Local Authority')
            plt.ylabel('Average Rating')
            plt.title('Average Pub Ratings by Local Authority')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.error("No data available for the selected local authorities.")
    else:
        st.info("Please select at least one local authority to display the data.")



def main():
    st.title("Charts About London Pubs")
    top10_chart(df_pubs)
    ratings_chart(df_pubs)
    #pub_pie(df_pubs)
main()


