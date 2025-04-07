import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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



# Create a bar chart

col2, col3 = st.columns(2)

with col2:

    fig2 = px.bar(df, x='Region', y='CO2_Reduction', title='CO2 Reduction by Region')
    st.plotly_chart(fig2, use_container_width=True)

# Create a scatter plot
with col3:
    fig3 = px.scatter(df, x='Sales', y='Customer_Satisfaction', title='Sales and Customer Satisfaction')
    st.plotly_chart(fig3, use_container_width=True)


st.title("Sales and CO2 Reduction by Region and Product")

# Create a line chart
fig = px.scatter_geo(df, hover_name='Region', lat='Latitude', lon='Longitude', size='CO2_Reduction', projection='natural earth')
st.plotly_chart(fig, use_container_width=True)




agg_data = df.groupby(['Region', 'Product', 'Latitude', 'Longitude']).agg({
    'Sales': 'sum',
    'Customer_Satisfaction': 'mean',
    'CO2_Reduction': 'mean',
    'Production_Cost': 'mean'
}).reset_index()


fig = px.scatter_geo(agg_data,lat='Latitude',lon='Longitude',size='Sales',color='Customer_Satisfaction',hover_name='Region',
                     hover_data={'Product': True, 'Sales': ':.0f','CO2_Reduction': ':.1f tons', 'Production_Cost': '$,.0f'},
                     color_continuous_scale='Greens',
                     title='Green Impact Bubble Map')

st.plotly_chart(fig, use_container_width=True)
fig.update_geos(projection_type='natural earth', showcoastlines=True, coastlinecolor='Black', landcolor='lightgray')



# Create a funnel chart
groupby_data = df.groupby(['Region', 'Product']).agg({'Sales': 'sum','Customer_Satisfaction': 'mean','CO2_Reduction': 'sum',
                                                      'Production_Cost': 'sum'}).reset_index()

groupby_data['Total_Production'] = groupby_data['Sales'] * 1.2
fig = px.funnel(data_frame=groupby_data,x='Sales',y='Product',color='Region',title='Sales Funnel',template='plotly_dark',)
st.plotly_chart(fig, use_container_width=True)





# Create a density contour plot
north_america = df[df['Region'] == 'North America']

fig = px.density_contour(data_frame=north_america,x='Production_Cost',y='CO2_Reduction',marginal_x='histogram',
    marginal_y='histogram',title='EcoTech Density Flow - North America',template='plotly_dark',color_discrete_sequence=['#00FF00'])


fig.update_layout(height=600,width=800,xaxis_title='Production Cost ($)',yaxis_title='CO₂ Reduction (tons)',
                  margin=dict(l=50, r=50, b=50, t=50))

st.plotly_chart(fig, use_container_width=True)





# Create a violin plot

df_2023 = df[df['Year'] == 2023]

fig = px.violin(data_frame=df_2023,x=north_america['Customer_Satisfaction'],y=north_america['Product'],box=True,points='all',title='Customer Satisfaction by Product - North America')
fig.update_layout(xaxis_title='Product',yaxis_title='Customer Satisfaction',legend_title='Region',height=600,width=800,template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)







# Create a 3D surface plot
pvt = df.pivot_table(index='Region', columns='Year', values='Sales', aggfunc='sum')

fig = go.Figure(data=[go.Surface(z=pvt.values, x=pvt.columns, y=pvt.index)])

fig.update_layout(scene=dict(xaxis_title='Year',yaxis_title='Region',zaxis_title='Sales'), template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)



# Create a 3D scatter plot
fig = px.scatter_3d(df,
                    x='Longitude',y='Latitude',z='Sales',color='CO2_Reduction',size='Customer_Satisfaction',animation_frame='Year',
                    color_continuous_scale='Viridis',hover_data=['Product'],title='EcoTech Interactive Globe')
fig.update_traces(marker=dict(size=5, opacity=0.8), selector=dict(mode='markers'))
fig.update_layout(scene=dict(aspectmode='cube'), template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)



# Create a radar chart
categories = ['Sales', 'Customer Satisfaction', 'CO2 Reduction', 'Production Cost']
solar = [0.8, 0.9, 0.7, 0.6]  

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=solar,theta=categories,fill='toself',line_color='forestgreen',name='Solar Panels'))

fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[-1,1])))
st.plotly_chart(fig, use_container_width=True)







# Create a parallel coordinates plot
filtered_df = df[(df['Year'] == 2021) & (df['Product'] == 'Eco Batteries')]

region_color_map = {region: idx for idx, region in enumerate(filtered_df['Region'].unique())}
filtered_df['Region_Color'] = filtered_df['Region'].map(region_color_map)

fig = px.parallel_coordinates(filtered_df, color='Region_Color', dimensions=['Production_Cost', 'Sales', 'Customer_Satisfaction', 'CO2_Reduction'], color_continuous_scale=px.colors.sequential.Viridis, title='Eco Batteries in 2021', color_continuous_midpoint=0.5)
fig.update_layout(title='Eco Batteries in 2021',height=600,width=800,template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)






# Create a sunburst chart
st.title("EcoTech Interactive Dashboard")
fig = px.sunburst(df,path=['Year','Region','Product'],values='Sales',color='Customer_Satisfaction',color_continuous_scale='blues',title='EcoTech Sunburst Chart',branchvalues='total')
fig.update_layout(title='EcoTech Sunburst Chart',height=800,width=800,template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)



