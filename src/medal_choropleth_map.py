## IMPORT LIBRARIES
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

world = gpd.read_file('../Coursework_2/data/world_countries/countries.geojson') #load world map file 
world = world[world['ADMIN'] != 'Antarctica'] #exclude antartica on the map 

def get_choropleth(df, season, ax, html_dashboard = False, title_size = 14, tick_size = 12):

    #set size specs depending on dashboard type
    if html_dashboard: 
        title_size = 24
        tick_size = 17
    
    #count total number of medals by country
    df_medals = df.groupby('country_3_letter_code').size().reset_index(name='Total Medals')
    #merge map and medal data 
    medals_map_data = pd.merge(world, df_medals, how='left', left_on='ISO_A3', right_on='country_3_letter_code')

    #create choropleth plot
    #fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    world.plot(ax=ax, color='lightgray', edgecolor='white') #plot world map

    #adjust plot color and title depending on which dataset is used
    if season == 'Winter': 
        medals_map_data.plot(ax = ax, column = 'Total Medals', cmap = 'Blues', legend = True, cax = cax)
         #apply medal data 
        ax.set_title('Winter Olympic Medals Won by Country', fontweight = 'bold', fontsize = title_size) #winter medals won
    elif season == 'Summer':
        medals_map_data.plot(ax = ax, column = 'Total Medals', cmap = 'Reds', legend = True, cax = cax) #apply medal data 
        ax.set_title('Summer Olympic Medals Won by Country', fontweight = 'bold', fontsize = title_size) #summer medals won
    else: 
        medals_map_data.plot(ax = ax, column = 'Total Medals', cmap = 'Greens', legend = True, cax = cax) #apply medal data 
        ax.set_title('Olympic Medals Won by Country', fontweight = 'bold') #total medals won

    #add legend
    legend = ax.get_legend()
    if legend:
        for text in legend.get_texts():
            text.set_fontsize(tick_size)

    ax.set_axis_off()
    plt.tight_layout()
    
    return ax

    