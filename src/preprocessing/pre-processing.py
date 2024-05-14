import pandas as pd
import numpy as np 
import geopandas as gpd
from src.standardize_medals import standardize_medal_types

#define paths to datasets
hosts_path = '../data/raw/olympic_hosts.csv'
medals_path = '../data/raw/olympic_medals.csv'
results_path = '../data/raw/olympic_results.csv'
athletes_path = '../data/raw/athlete_events.csv'

#read datasets 
hosts = pd.read_csv(hosts_path, header = 0)
medals = pd.read_csv(medals_path, header = 0)
results = pd.read_csv(results_path, header = 0)
athletes = pd.read_csv(athletes_path, header = 0)

datasets = [hosts, medals, results, athletes]
#standardize medal descriptions
datasets = [standardize_medal_types(df) for df in datasets]

#check for missing values
for df in datasets:
    missing_values = df.isnull().sum()
    print(missing_values)
    print()

world = gpd.read_file('../data/raw/countries.geojson')
mapping_dict = dict(zip(world['ADMIN'], world['ISO_A3']))

#MANUAL UPDATES FOR COUNTRIES THAT NO LONGER EXIST 
update_countries = {
    'AHO': 'NLD', #antilles of netherlands 
    'ISV': 'VIR', #us virgin islands
    'TPE': 'CHN', #taipei
    'BOH': 'CZE', #bohemia, now czechia
    'OAR': 'RUS', #russia, after doping scandal
    'FRG': 'DEU', #germany
    'IRI': 'IRN', #iran
    'SCG': 'SRB', #majority serbian winners
    'URS': 'RUS', #drop?
    'YUG': 'SRB', #yugoslavia, majority serbian winners
    'UAR': 'EGY', #united arab region
    'ROC': 'RUS', #russian olympic committee
    'BAH': 'BHS', #bahamas
    'TCH': 'CZE', #czechoslovakia
    'GDR': 'DEU'  
}


#drop all country columns except for country_3_letter_code
for i, df in enumerate(datasets):
    if 'country_name' in df.columns:
        if 'country_3_letter_code' in df.columns:
            #update country codes to current ISO_A3 codes
            df['country_3_letter_code'] = df['country_3_letter_code'].map(update_countries).fillna(df['country_3_letter_code'])
            mapping_dict = dict(zip(world['ADMIN'], world['ISO_A3']))
            df['updated_country_code'] = df['country_name'].map(mapping_dict)
            df['country_3_letter_code'] = df['updated_country_code'].fillna(df['country_3_letter_code'])

        #drop country name columns and intermediate column
        df.drop(columns=['updated_country_code'], inplace=True)
        df.drop(columns=['country_name'], inplace=True)
    if 'country_code' in df.columns:
        df.drop(columns=['country_code'], inplace=True)
    #remove all urls 
    if 'athlete_url' in df.columns:
        df.drop(columns = 'athlete_url', inplace = True)
    #remove bio column
    if 'bio' in df.columns:
        df.drop(columns = 'bio', inplace = True)
    if 'value_unit' and 'value_type' in df.columns:
        df.drop(columns = ['value_unit', 'value_type', 'rank_equal'], inplace = True)
    #impute missing values for medal_type 
    if 'Medal' in df.columns:
        df['Medal'].fillna('NONE', inplace=True)
    if 'medal_type' in df.columns:
        df['medal_type'].fillna('NONE', inplace=True)
    
    #update list of datasets
    datasets[i] = df

athletes = datasets[3]
results = datasets[2]
medals = datasets[1]
hosts = datasets[0]
#remove results without placement information 
results = results[(results['rank_position'].notnull()) | (results['medal_type'].isin(['GOLD', 'SILVER', 'BRONZE']))]


# change some sport names
new_names = {
    'Cycling BMX': 'Cycling BMX Racing', #Cycling BMX is called BMX Racing now
    'Baseball': 'Baseball/Softball', #Baseball/Softball is the current category 
    '3x3 Basketball': 'Basketball 3x3', 
    #only one official discipline cateogry for Equestrian sports 
    'Equestrian  Vaulting': 'Equestrian',
    'Equestrian Dressage': 'Equestrian',
    'Equestrian Eventing': 'Equestrian',
    'Equestrian Jumping': 'Equestrian',
    #renamed sports
    'Rugby': 'Rugby Sevens',
    'Short Track Speed Skating': 'Short Track',
    'Synchronized Swimming': 'Artistic Swimming',
    'Trampoline Gymnastics': 'Trampoline'
}

#sports only featured at one games
one_time = ['Basque Pelota', 'Croquet', 'Military Patrol', 'Rackets', 'Roque', 'Water Motorsports']

datasets = [hosts, medals, results, athletes]  
for i, df in enumerate(datasets):
    if 'discipline_title' in df.columns:
        df['discipline_title'] = df['discipline_title'].replace(new_names)
        #df = df[~df['discipline_title'].isin(one_time)]
        datasets[i] = df

    if 'participant_type' in df.columns:
        df['participant_type'] = df['participant_type'].replace('GameTeam', 'Team')
        datasets[i] = df

athletes = datasets[3]
results = datasets[2]
medals = datasets[1]
hosts = datasets[0]

## JOINING TABLES 
merged_medals_hosts = medals.merge(hosts, how='left', left_on='slug_game', right_on='game_slug')

merge_drop = ['game_slug', 'game_end_date', 'game_start_date', 'slug_game', 'participant_title']
merged_medals_hosts.drop(columns = merge_drop, axis=1, inplace = True)


## Duplciated medals for team sports 
#group columns team members have in common
aggregated = merged_medals_hosts.groupby(['discipline_title', 'event_title', 'event_gender', 'medal_type', 'participant_type', 'country_3_letter_code', 'game_location', 'game_season', 
                            'game_year', 'game_name']
                            ).size().reset_index(name='medal_count')

#drop duplicates 
medals = aggregated.drop_duplicates(subset=['discipline_title', 'event_title', 'event_gender', 'medal_type', 'country_3_letter_code','game_location', 'game_season', 'game_year', 'game_name'])
#drop intermediary column
medals = medals.drop(columns = 'medal_count', inplace = False)

#save summer and winter games data seperately
summer = medals[medals['game_season'] == 'Summer'].reset_index(drop = True)
winter = medals[medals['game_season'] == 'Winter'].reset_index(drop = True)
for df in (summer, winter):
    df.drop(columns = 'game_season', inplace = True)

#save a dataframe with complete height and weight data
spec_columns = ['Height', 'Weight', 'Age']
height_weight_complete = athletes.dropna(subset = spec_columns)
athletes_height_weight = pd.DataFrame(height_weight_complete)
#drop missing rows of height, weight, age
athletes = athletes.drop(columns = spec_columns)

#specify directories to save tables
merged_path = '../data/derived/medals.csv'
cleaned_results_path  = '../data/derived/results.csv'
summer_path = '../data/derived/summer_medals.csv'
winter_path = '../data/derived/winter_medals.csv'
height_weight_path = '../data/derived/athletes_height_weight.csv'
athletes_path = '../data/derived/athletes.csv'

#save processed tables to derived directory
medals.to_csv(merged_path, index=False)
results.to_csv(cleaned_results_path, index = False)
summer.to_csv(summer_path, index = False)
winter.to_csv(winter_path, index = False)
athletes_height_weight.to_csv(height_weight_path, index = False)
athletes.to_csv(athletes_path, index = False)
