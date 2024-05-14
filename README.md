# Coursework 2 - Olympic Dashboard
Author: 02509292

This project's reference data is [AthleteEvents](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) and [120_Years_of_Olympics](https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018?select=olympic_hosts.csv). 

**data/** contains all data used for the dashboard. [raw](./data/raw/) has the data from the reference datasets, [derived](./data/derived/) has the cleaned and processed datasets as .csv files, [world_countries](./data/world_countries/) has a .geojson file for the world plots, and [flags](./data/flags/) contains the country flag images used for plots. 

**src/** contains the .py scripts for preprocessing and data visualization. [preprocessing](./src/preprocessing/) contains the .py script to clean and organize the new datasets. 

**makefile/** contains a create_html_dashboard.py file that will output the dashboard in .html format and a create_xlsx_dashboard.py that will output the dashboard in excel format. The identical scripts are available in .ipynb files. 

**outputs/** stores all .png outputs used for the dashboards

**reports/** contains the final dashboard in .xlx and .html format. 

To reproduce this project it is suggested to:  
- 1: Create the derived datasets using the [.py script](./src/preprocessing/pre-processing.py) or [.ipynb file](./src/preprocessing/pre-processing.ipynb). 
- 2: Create the dashboard in your desired format:
    - [html](./makefile/create_html_dashboard.py)
    - [Excel](./makefile/create_xlsx_dashboard.py)
- 3: View your final dashboard which is located [here](./reports/)
