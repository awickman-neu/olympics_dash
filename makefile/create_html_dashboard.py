
## IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#excel libraries 
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as XLImage

#from src import top_10_countries
from src.top_10 import total_medal_tally, athlete_medal_tally
from src.athlete_measurement_plots import get_measurement_plots
from src.medal_choropleth_map import get_choropleth
from src.olympic_participation import get_athlete_participation_plot, get_gender_participation, get_country_participation
from src.simple_statistics import get_total_athletes, get_host_cities, get_total_medals, get_number_disciplines


#read csv file of processed athlete, medal data
athletes = pd.read_csv('../Coursework_2/data/derived/athletes.csv')
medals = pd.read_csv('../Coursework_2/data/derived/medals.csv')
summer_df = pd.read_csv("../Coursework_2/data/derived/summer_medals.csv")
winter_df = pd.read_csv("../Coursework_2/data/derived/winter_medals.csv")
athlete_measurements = pd.read_csv("../Coursework_2/data/derived/athletes_height_weight.csv")
results = pd.read_csv('../Coursework_2/data/derived/results.csv')

## COUNTRY PARTICIPATION PLOT
fig1, ax1 = plt.subplots(figsize=(15, 5))
get_country_participation(athletes, ax1,  html_dashboard = True)
country_participation_plot_path = '../Coursework_2/outputs/country_participation_plot.png'
fig1.savefig(country_participation_plot_path, bbox_inches='tight')
plt.close(fig1)

## ATHLETE PARTICIPATION PLOT
fig2, ax2 = plt.subplots(figsize=(15, 5))
get_athlete_participation_plot(athletes, ax2, html_dashboard = True)
athlete_participation_plot_path = '../Coursework_2/outputs/athlete_participation_plot.png'
fig2.savefig(athlete_participation_plot_path, bbox_inches='tight')
plt.close(fig2)

## SUMMER MEDALS CHOROPLETH
fig1, ax1 = plt.subplots(figsize=(15, 5))
get_choropleth(summer_df, 'Summer', ax1, html_dashboard = True)
summer_path = '../Coursework_2/outputs/summer_choropleth_map.png'
fig1.savefig(summer_path, bbox_inches='tight')
plt.close(fig1)

## WINTER MEDALS CHOROPLETH
fig2, ax2 = plt.subplots(figsize=(15, 5))
get_choropleth(winter_df, 'Winter', ax2, html_dashboard = True)
winter_path = '../Coursework_2/outputs/winter_choropleth_map.png'
fig2.savefig(winter_path, bbox_inches='tight')
plt.close(fig2)

## COUNTRY MEDAL TALLY
fig, axes = plt.subplots(1, 2, figsize=(22, 10))
total_medal_tally(medals, axes[0], html_dashboard = True)
athlete_medal_tally(athletes, axes[1], html_dashboard = True) ## ATHLETE MEDAL TALLY
plt.tight_layout() 
medal_tally_path = '../Coursework_2/outputs/medal_tally.png'
fig.savefig(medal_tally_path)
plt.close(fig)

## ATHLETE MEASUREMENT PLOTS
fig = get_measurement_plots(athlete_measurements, figsize = (22, 10), html_dashboard = True)
athlete_measurement_plot_path = '../Coursework_2/outputs/athlete_measurements.png'
fig.savefig(athlete_measurement_plot_path, bbox_inches='tight')
plt.close(fig)

total_medals = get_total_medals(medals)
total_athletes = get_total_athletes(athletes)
host_cities = get_host_cities(medals)
disciplines = get_number_disciplines(results)

## STYLE AND CONTENT DASHBOARD 
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Olympic Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            text-align: center;
            background: #f4f4f4;
        }}
        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center; 
            padding: 10px 0;
            flex-wrap: wrap;
        }}
        .row1-plots {{
            display: flex;
            justify-content: space-between;
            flex-direction: column;
            align-items: center;
            width: 100%;
            margin-bottom: 0px;
        }}
        .row1-plot {{
            width: 100%; 
            margin: 10px 0;
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .olympic-rings-container {{
            flex: 1 0 20%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .olympic-rings {{
            max-width: 80%;
            height: auto;
        }}
        .statistics-section {{
            width: 90%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            margin-top: 5px;
        }}
        .statistic {{
            flex: 1;
            margin: 5px;
            padding: 5px;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            max-width: 150px;
            text-align: center;
            max-height: 100px;
            color: white;
            font-weight: bold; 
        }}
        .statistic p {{
            font-size: 22px;
        }}
        .header-content > div, .header-content > img {{
            width: 38%;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center; 
            margin-bottom: 20px; 
        }}
        .header h1 {{
            flex-grow: 1;
        }}
        .header img {{
            width: 500px;
            height: 216px;
            flex-shrink: 0;
        }}
        .dashboard {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }}
        .dashboard-item {{
            flex: 1 1 300px;
            max-width: 45%;
            margin: 10px;
        }}
        img {{
            width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="header-content">
        <div class="row1-plots">
            <img src="{country_participation_plot_path}" alt="Participation Plot - Country" class="row1-plot">
            <img src="{athlete_participation_plot_path}" alt="Participation Plot - Athlete" class="row1-plot">
        </div>
        <div class="olympic-rings-container">
            <img src="../Coursework_2/input_images/olympic_rings.png" alt="Olympic Rings" class="olympic-rings">
            <h2>120 Years of the Olympic Games<br>Athens 1896 - Rio 2016</h2>
            <div class="statistics-section">
                <div class="statistic" style="background-color:#FFD700">
                    <p>{total_medals}</p>
                    <h3>Medals Won</h3>
                </div>
                <div class="statistic" style="background-color:#008000">
                    <p>{total_athletes}</p>
                    <h3>Total Athletes</h3>
                </div>
            </div>
            <div class="statistics-section">
                <div class="statistic" style="background-color:#0000FF">
                    <p>{host_cities}</p>
                    <h3>Host Cities</h3>
                </div>
                <div class="statistic" style="background-color:red">
                    <p>{disciplines}</p>
                    <h3>Disciplines</h3>
                </div>
            </div>
        </div>
        <div class="row1-plots">
            <img src="{summer_path}" alt="Olympic Medals Choropleth - Summer" class="row1-plot">
            <img src="{winter_path}" alt="Olympic Medals Choropleth - Winter" class="row1-plot">
        </div>
    </div>
    <div class="dashboard">
        <div class="dashboard-item">
            <img src="{medal_tally_path}" alt="Medal Tally" class = "row1-plot">
        </div>
        <div class="dashboard-item">
            <img src="{athlete_measurement_plot_path}" alt="Olympic Athletes Measurements" class = "row1-plot">
        </div>
    </div>
</body>
</html>
"""


## CREATE HTML DASHBOARD AND SAVE IN REPORTS
html_file_path = '../Coursework_2/reports/olympic_dashboard.html'
with open(html_file_path, 'w') as f:
    f.write(html_content)

print(f"HTML dashboard saved as '{html_file_path}'")