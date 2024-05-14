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
from top_10 import total_medal_tally, athlete_medal_tally
from athlete_measurement_plots import get_measurement_plots
from medal_choropleth_map import get_choropleth
from olympic_participation import get_athlete_participation_plot, get_gender_participation, get_country_participation
from excel_specs import get_fig_size
from create_text import create_text_fig, create_stat_widgets
from simple_statistics import get_total_athletes, get_host_cities, get_total_medals, get_number_disciplines


## FUNCTION TO CREATE DASHBOARD 

def create_excel_dashboard():

    #read csv file of processed athlete, medal data
    athletes = pd.read_csv('../Coursework_2/data/derived/athletes.csv')
    medals = pd.read_csv('../Coursework_2/data/derived/medals.csv')
    summer_df = pd.read_csv("../Coursework_2/data/derived/summer_medals.csv")
    winter_df = pd.read_csv("../Coursework_2/data/derived/winter_medals.csv")
    athlete_measurements = pd.read_csv("../Coursework_2/data/derived/athletes_height_weight.csv")
    results = pd.read_csv('../Coursework_2/data/derived/results.csv')

    ## COUNTRY AND ATHLETE PARTICIPATION PLOTS & GENDER
    width, height = get_fig_size(13,34)
    fig, axes = plt.subplots(2, 1, figsize=(width, height))
    ax1 = axes[0]
    get_country_participation(athletes, ax1)
    ax2 = axes[1]
    get_athlete_participation_plot(athletes, ax2)
    fig.patch.set_linewidth(2)
    combined_participation_plot_path = '../Coursework_2/outputs/combined_plot.png' #participation plot path
    plt.savefig(combined_participation_plot_path, dpi = 100) #save plot

    '''## GENDER PARTICIPATION PLOT 
    fig = get_gender_participation(athletes)
    gender_participation_plot_path = '../Coursework_2/outputs/gender_participation_plot.png'
    plt.savefig(gender_participation_plot_path)
    plt.close(fig)
    '''

    ## SUMMER MEDALS CHOROPLETH
    fig, axes = plt.subplots(2,1, figsize = (width, height))
    ax1 = axes[0]
    get_choropleth(summer_df, 'Summer', ax1)

    ## WINTER MEDALS CHOROPLETH
    ax2 = axes[1]
    get_choropleth(winter_df, 'Winter', ax2)
    combined_choropleth_plot_path = '../Coursework_2/outputs/medal_choropleth_map.png'
    fig.savefig(combined_choropleth_plot_path, bbox_inches='tight')

    ## MEDAL TALLY TOP 10 
    width, height = get_fig_size(20.5, 21) 
    fig, axes = plt.subplots(1,2, figsize = (width, height))
    ax1 = axes[0]
    total_medal_tally(medals, ax1)

    ## ATHLETE TALLY TOP 10
    ax2 = axes[1]
    athlete_medal_tally(athletes, ax2)
    fig.tight_layout()
    both_tallies_path = '../Coursework_2/outputs/athlete_medal_tally.png'
    fig.savefig(both_tallies_path, bbox_inches='tight')

    ## ATHLETE MEASUREMENT PLOTS
    width, height = get_fig_size(12, 21) 
    fig = get_measurement_plots(athlete_measurements, figsize = (width, height))
    athlete_measurement_plot_path = '../Coursework_2/outputs/athlete_measurements.png'
    fig.savefig(athlete_measurement_plot_path, bbox_inches='tight')
    plt.close(fig)

    ## CREATE WORKSHEET FOR DASHBOARD
    wb = Workbook()
    ws = wb.active
    ws.title = 'Dashboard'

    ## CREATE IMAGES
    combined_participation = Image(combined_participation_plot_path)
    combined_choropleth = Image(combined_choropleth_plot_path)
    both_tallies_image = Image(both_tallies_path)
    athlete_measurements_image = Image(athlete_measurement_plot_path)

    ## OLYMPIC RINGS 
    olumpic_rings = PILImage.open('../Coursework_2/input_images/olympic_rings.png')
    new_img = PILImage.new("RGB", olumpic_rings.size, "white")
    new_img.paste(olumpic_rings, (0, 0), olumpic_rings)
    olympic_rings_complete_path = '../Coursework_2/input_images/olympic_rings_complete.png'
    new_img.save(olympic_rings_complete_path)
    olympic_rings_image = XLImage(olympic_rings_complete_path)
    olympic_rings_image.width = 500 
    olympic_rings_image.height = 216   
    
    ## DASHBOARD HEADER 
    text = "120 Years of the Olympic Games \n Athens 1896 - Rio 2016"
    text_width, text_height = get_fig_size(7, 10) 
    fig = create_text_fig(text, figsize = (text_width, text_height))
    text_path = '../Coursework_2/outputs/header.png'
    fig.savefig(text_path)
    plt.close(fig)
    text_image = XLImage(text_path)

    ## SIMPLE STATISTICS
    total_medals = get_total_medals(medals)
    total_medals_widget = create_stat_widgets(total_medals,  "Medals Won", "#FFD700")
    total_athletes = get_total_athletes(athletes)
    total_athletes_widget = create_stat_widgets(total_athletes, "Athletes", '#008000')
    host_cities = get_host_cities(medals)
    host_cities_widget = create_stat_widgets(host_cities, "Host Cities", '#0000FF')
    disciplines = get_number_disciplines(results)
    disciplines_widget = create_stat_widgets(disciplines, "Disciplines", "red")

    ## ADD PLOTS TO EXCEL DASHBOARD 
    ws.add_image(combined_participation, 'A1')
    ws.add_image(combined_choropleth, 'U1')
    ws.add_image(both_tallies_image, 'A35')
    ws.add_image(athlete_measurements_image, 'U35')
    ws.add_image(olympic_rings_image, 'N1')
    ws.add_image(text_image, 'N12')
    ws.add_image(total_medals_widget, 'N28')
    ws.add_image(total_athletes_widget, 'R28')
    ws.add_image(host_cities_widget, 'N22')
    ws.add_image(disciplines_widget, 'R22')
    
    ## SAVE EXCEL DASHBOARD
    excel_file_path = '../Coursework_2/reports/olympic_dashboard.xlsx'
    wb.save(excel_file_path)