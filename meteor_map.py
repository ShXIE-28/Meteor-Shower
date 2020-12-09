# -*- coding: utf-8 -*-
"""
Meteor Shower Map

@author: shuhui
"""
import plotly.express as px

def create_map(dt,year_s,year_e):
    
    dt = dt[(dt['Year']>=year_s) & (dt['Year']<=year_e)]
    fig = px.scatter_mapbox(dt,lat='Latitude',lon='Longitude',color = 'Elevation',
                            color_continuous_scale=px.colors.diverging.Geyser,
                            range_color=[-300,3000],hover_name='City',
                            hover_data=['Start Date','Time'],zoom=1)
    fig = fig.update_layout(mapbox_style='carto-positron')
    
    return fig

def update_map(dt):
    fig = px.scatter_mapbox(dt,lat='Latitude',lon='Longitude',color = 'Elevation',
                            color_continuous_scale=px.colors.diverging.Geyser,
                            range_color=[-300,3000],hover_name='City',
                            hover_data=['Start Date','Time'],zoom=1)
    fig = fig.update_layout(mapbox_style='carto-positron')
    
    return fig
    