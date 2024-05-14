import matplotlib.pyplot as plt 
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#define colors of medals 
medal_colors = ['#FFD700', '#C0C0C0', '#CD7F32']
top_n = 10 #number of athletes/countries shown

def total_medal_tally(df, ax, html_dashboard = False, title_size = 14, label_size = 8, legend_fontsize = 8, tick_size = 8):

    if html_dashboard: 
        title_size = 24
        label_size = 17
        legend_fontsize = 18
        tick_size = 15
    
    #group by country and medal type
    medal_tally = df.groupby(['country_3_letter_code', 'medal_type']).size().unstack(fill_value = 0)
    #sum the different medals and save in Total column
    medal_tally['Total'] = medal_tally.sum(axis = 1)
    #sort in descending order
    medal_tally = medal_tally.sort_values(by='Total', ascending=False)
    #rearrange order 
    medal_tally = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']]
    #save top 10 countries
    top_countries = medal_tally.head(top_n).reset_index()
    top_countries = top_countries[::-1] #reverse order


    #PLOT MEDAL TALLY
    top_countries[['Gold', 'Silver', 'Bronze']].plot(kind = 'barh', stacked = True, color = medal_colors, ax = ax) #stacked bar plot 
    ax.set_xlabel('Number of Medals', fontsize = label_size)
    ax.set_ylabel('Country', fontsize = label_size)
    ax.set_title('Top 10 Most Awarded Countries', fontweight = 'bold', fontsize = title_size)
    ax.legend(title = 'Medal Type', fontsize = legend_fontsize)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=tick_size)
    ax.set_yticklabels(top_countries['country_3_letter_code'])
    ax.tick_params(axis='y', labelsize=label_size)

    for i, (index, row) in enumerate(top_countries.iterrows()):
        noc = row['country_3_letter_code']
        image_dir = '../Coursework_2/data/flags/'
        image_path = f"{image_dir}{noc}.png"
        try:
            flag_image = plt.imread(image_path)
            if html_dashboard:
                imagebox = OffsetImage(flag_image, zoom=0.07)
                ab = AnnotationBbox(imagebox, (top_countries['Total'].iloc[i] + 120, i), frameon=False)
            else: 
                imagebox = OffsetImage(flag_image, zoom=0.04)
                ab = AnnotationBbox(imagebox, (top_countries['Total'].iloc[i] + 100, i), frameon=False)
            ax.add_artist(ab)   
        except FileNotFoundError:
            continue        
    return ax

def athlete_medal_tally(df, ax, html_dashboard = False, title_size = 14, label_size = 8, legend_fontsize = 8, tick_size = 8):

    if html_dashboard: 
        title_size = 24
        label_size = 15
        legend_fontsize = 18
        tick_size = 15

    medal_df = df[df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
    athlete_medals = medal_df.groupby(['Name', 'Medal']).size().unstack(fill_value=0)

    top_athletes = athlete_medals.sum(axis=1).nlargest(top_n) #get the total medal count
    top_athletes = top_athletes[::-1] #reverse order for plot 

    country_info = df[['Name', 'NOC']].drop_duplicates().set_index('Name')
    top_athletes_countries = top_athletes.to_frame().join(country_info).reset_index()
    top_athletes_countries = top_athletes_countries.drop_duplicates(subset='Name', keep = 'last')


    ## PLOT STACKED BAR PLOT: MEDALLY TALLY
    top_athletes_medals = athlete_medals.loc[top_athletes.index, ['Gold', 'Silver', 'Bronze']]
    top_athletes_medals.plot(kind='barh', stacked=True, color = medal_colors, ax=ax)
    ax.set_xlabel('Number of Medals', fontsize = label_size)
    ax.set_ylabel('')
    ax.set_title('Top {} Most Awarded Athletes'.format(top_n), fontweight='bold', fontsize = title_size)
    ax.legend(title='Medal Type', loc='lower right', fontsize=legend_fontsize)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=tick_size)
    ax.tick_params(axis='y', labelsize=tick_size)

    for i, (index, row) in enumerate(top_athletes_countries.iterrows()):
        noc = row['NOC']
        
        image_dir = '../Coursework_2/data/flags/'
        image_path = f"{image_dir}{noc}.png"
        flag_image = plt.imread(image_path)
        if html_dashboard:
            imagebox = OffsetImage(flag_image, zoom=0.07)
        else: 
            imagebox = OffsetImage(flag_image, zoom=0.04)
        ab = AnnotationBbox(imagebox, (top_athletes_medals.iloc[i].sum() + 1, i), frameon=False)
        ax.add_artist(ab)   
        ax.text(-0.5, i-0.5, noc, ha='right', va='center', style = 'italic', fontsize = label_size)

    return ax



