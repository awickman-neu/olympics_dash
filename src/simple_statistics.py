## OLYMPIC STATISTICS

def get_total_medals(df):
    #medals.csv is required
    total_medals = df.groupby('medal_type').size().sum()
    return total_medals

def get_total_athletes(df):
    #athletes.csv is required
    total_athletes = df['ID'].nunique()
    return total_athletes

def get_host_cities(df):
    #medals.csv is required
    host_cities = df['game_location'].nunique()
    return host_cities

def get_number_disciplines(df):
    #results.csv or summer/winter/medals.csv is required
    disciplines = df['discipline_title'].nunique()
    return disciplines