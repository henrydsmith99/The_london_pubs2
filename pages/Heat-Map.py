import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False)
# Replace 'path_to_your_data.csv' with the actual path to your data file
path = ""
df_pubs=pd.read_csv(path+"open_pubs_10000_sample.csv")
df_pubs['latitude'] = pd.to_numeric(df_pubs['latitude'], errors='coerce')   # converting data to numeric type
df_pubs['longitude'] = pd.to_numeric(df_pubs['longitude'], errors='coerce') # converting data to numeric type

#[VIZI3]
# Streamlit title
st.title('Density of Pubs Based on Geographic Location')

# Plot configuration
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.kdeplot(x=df_pubs['longitude'], y=df_pubs['latitude'], cmap="Reds", shade=True, bw_adjust=0.5, cbar=True)
plt.title('Density of Pubs Based on Geographic Location')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display the plot in Streamlit
st.pyplot()

