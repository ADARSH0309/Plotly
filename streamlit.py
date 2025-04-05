import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

np.random.seed(42)

years = [2020, 2021, 2022, 2023, 2024]
regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
products = ['Solar Panels', 'Wind Turbines', 'Eco Batteries', 'Water Purifiers']

df = pd.DataFrame({
    'Year': np.repeat(years, len(regions) * len(products) * 10),
    'Region': np.tile(np.repeat(regions, len(products) * 10), len(years)),
    'Product': np.tile(np.repeat(products, 10), len(years) * len(regions)),
    'Sales': np.random.randint(50, 500, size=len(years) * len(regions) * len(products) * 10),  # Units sold
    'Customer_Satisfaction': np.random.uniform(3.5, 5.0, size=len(years) * len(regions) * len(products) * 10),  # Rating out of 5
    'CO2_Reduction': np.random.uniform(100, 1000, size=len(years) * len(regions) * len(products) * 10),  # Tons of CO2 reduced
    'Production_Cost': np.random.uniform(1000, 10000, size=len(years) * len(regions) * len(products) * 10),  # In USD
    'Latitude': np.tile(np.repeat([40.7, 51.5, 35.6, -23.5, -1.2], len(products) * 10), len(years)),  # Approx. region coords
    'Longitude': np.tile(np.repeat([-74.0, -0.1, 139.7, -46.6, 36.8], len(products) * 10), len(years))
})

print(df.shape)
print(df.head())


st.title("Sales and CO2 Reduction by Region and Product")

# Create a line chart
fig = px.scatter_geo(df, hover_name='Region', lat='Latitude', lon='Longitude', size='CO2_Reduction', projection='natural earth')
st.plotly_chart(fig, use_container_width=True)

# Create a bar chart
fig2 = px.bar(df, x='Region', y='CO2_Reduction', title='CO2 Reduction by Region')
st.plotly_chart(fig2, use_container_width=True)

# Create a scatter plot
fig3 = px.scatter(df, x='Sales', y='Customer_Satisfaction', title='Sales and Customer Satisfaction')
st.plotly_chart(fig3, use_container_width=True)
