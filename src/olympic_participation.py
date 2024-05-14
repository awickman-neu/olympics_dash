import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

## FUNCTION TO GET ATHLETE PARTICIPATION PLOT
def get_athlete_participation_plot(df, ax, html_dashboard = False, title_size = 12, label_size = 8, legend_fontsize = 9, tick_size = 9):
    
    #set plot specs depending on dashboard type
    if html_dashboard: 
        title_size = 24
        label_size = 15
        legend_fontsize = 18
        tick_size = 15

    #sort summer and winter athletes
    summer_athletes = df[df['Season'] == 'Summer']
    winter_athletes = df[df['Season'] == 'Winter']

    #sort by year
    summer_years = sorted(summer_athletes['Year'].unique())
    winter_years = sorted(winter_athletes['Year'].unique())

    summer_years_array = np.array(list(summer_years))
    winter_years_array = np.array(list(winter_years))
    #merge all olympic game years 
    all_years = set(summer_years).union(winter_years) 

    #get unique number of athletes for each season by year
    unique_summer_athletes = summer_athletes.groupby('Year')['ID'].nunique().reset_index(name='Number of Athletes')
    unique_winter_athletes = winter_athletes.groupby('Year')['ID'].nunique().reset_index(name='Number of Athletes')

    #
    summer_athletes_filled = unique_summer_athletes.set_index('Year').reindex(all_years).fillna(0)['Number of Athletes'].values
    winter_athletes_filled = unique_winter_athletes.set_index('Year').reindex(all_years).fillna(0)['Number of Athletes'].values

    ax.bar(list(all_years), summer_athletes_filled, width = 1.6, color='#FF6347', bottom = winter_athletes_filled, label = 'Summer Games')
    ax.bar(list(all_years), winter_athletes_filled, width = 1.6, color='#4682B4', label = 'Winter Games')

    summer_coeffs = Polynomial.fit(summer_years_array, unique_summer_athletes['Number of Athletes'], 1)
    winter_coeffs = Polynomial.fit(winter_years_array, unique_winter_athletes['Number of Athletes'], 1)

    summer_trend_line = summer_coeffs(summer_years_array)
    winter_trend_line = winter_coeffs(winter_years_array)

    ax.plot(summer_years_array, summer_trend_line, color='#FF6347', linestyle='--')
    ax.plot(winter_years_array, winter_trend_line, color='#4682B4', linestyle='--')

    #WORLD WAR SHADED REGION
    ax.axvspan(1914, 1918, color='gray', alpha=0.3)
    ax.axvspan(1939, 1945, color='gray', alpha=0.3)
    ax.text(1942, 1000, 'WWII', fontsize = label_size, ha ='center', color='grey')
    ax.text(1916, 1000, 'WWI', fontsize = label_size, ha ='center',color='grey')
    if html_dashboard: 
        ax.set_title('Athlete Participation per Games', fontweight = 'bold', fontsize = title_size)
    else: 
        ax.set_title('')
    ax.set_xlabel('Year', fontsize = label_size)
    ax.set_ylabel('Number of Unique Athletes', fontsize = label_size)
    ax.legend(fontsize = legend_fontsize)
    ax.grid(False)
    ax.tick_params(axis = 'x', rotation=45, labelsize = tick_size)
    ax.tick_params(axis = 'y', rotation=45, labelsize = tick_size)

    return ax


    
## FUNCTION TO GET COUNTRY PARTICIPATION PLOT
def get_country_participation(df, ax, html_dashboard = False, title_size = 12, label_size = 10, legend_fontsize = 10, tick_size = 10):

    #set plot specs depending on dashboard type
    if html_dashboard: 
        title_size = 24
        label_size = 15
        legend_fontsize = 18
        tick_size = 15

    #sort summer and winter athletes
    summer_athletes = df[df['Season'] == 'Summer']
    winter_athletes = df[df['Season'] == 'Winter']
    summer_participation = summer_athletes.groupby('Year')['NOC'].nunique()
    winter_participation = winter_athletes.groupby('Year')['NOC'].nunique()

    #sort by year
    summer_years = sorted(summer_athletes['Year'].unique())
    winter_years = sorted(winter_athletes['Year'].unique())

    ax.bar(summer_years, summer_participation, color='red', width = 1.6, label='Summer Games')
    ax.bar(winter_years, winter_participation, color='blue', width = 1.6, label='Winter Games')
    #shaded area to indicate world wars 
    ax.axvspan(1914, 1918, color='gray', alpha=0.3)
    ax.axvspan(1939, 1945, color='gray', alpha=0.3)
    ax.text(1942, 25, 'WWII', fontsize= label_size, ha ='center', color = 'grey')
    ax.text(1916, 25, 'WWI', fontsize= label_size, ha='center', color = 'grey')
    if html_dashboard: 
        ax.set_title('Country Participation per Games', fontweight = 'bold', fontsize = title_size)
    else: 
        ax.set_title('Country and Athlete Participation per Games', fontweight = 'bold', fontsize = title_size)
    ax.set_ylabel('Number of Countries', fontsize = label_size)
    ax.set_xlabel('')
    ax.tick_params(axis='x', labelsize=tick_size)
    ax.tick_params(axis='y', labelsize=tick_size)
    ax.legend(fontsize = legend_fontsize)
    ax.grid(False)
    ax.tick_params(axis = 'x', rotation=45)

    return ax


def get_gender_participation(df, title_size = 24, label_size = 15, legend_fontsize = 18, tick_size = 15):

    gender_participation = df.groupby(['Year', 'Sex'])['ID'].nunique().reset_index()
    gender_participation_pivot = gender_participation.pivot(index='Year', columns='Sex', values='ID').fillna(0)
    
    #create gender participant plot 
    fig, ax = plt.subplots()
    gender_participation_pivot.plot(kind = 'bar', stacked = True, color = ['violet', 'blue'], ax = ax)
    plt.title('Gender Participation per Games', fontweight = 'bold', fontsize = title_size)
    plt.xlabel('Year')
    plt.ylabel('Number of Athletes')
    plt.xticks(rotation = 45, ha = 'right')
    plt.legend(title = 'Gender', fontsize = legend_fontsize)
    plt.tight_layout()

    return fig

