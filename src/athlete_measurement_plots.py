import pandas as pd
import matplotlib.pyplot as plt

def get_measurement_plots(df, figsize, html_dashboard = False, title_size = 12, label_size = 9, legend_fontsize = 9, tick_size = 9):

    if html_dashboard:
        title_size = 24
        label_size = 17
        legend_fontsize = 18
        tick_size = 17  

    fig, axs = plt.subplots(1, 3, figsize = figsize)

    # AGE DISTRIBUTION PLOT 
    axs[0].hist(df[df['Sex'] == 'M']['Age'], bins=20, color='#ADD8E6', edgecolor='black', alpha = 0.8, label='Male')
    axs[0].hist(df[df['Sex'] == 'F']['Age'], bins=20, color='#FFB6C1', edgecolor='black', alpha = 0.8, label='Female')
    axs[0].set_xlabel('Age', fontsize = label_size)
    #axs[0].set_ylabel('Frequency', fontsize = label_size)
    axs[0].set_title('Age Distribution', fontweight='bold', fontsize = title_size)
    axs[0].tick_params(axis='x', labelsize=tick_size)
    axs[0].tick_params(axis='y', labelsize=tick_size)
    axs[0].legend(fontsize=legend_fontsize)

    # HEIGHT DISTRIBUTION PLOT 
    axs[1].hist(df[df['Sex'] == 'M']['Height'], bins=20, color='#6495ED', edgecolor='black', alpha = 0.8, label='Male')
    axs[1].hist(df[df['Sex'] == 'F']['Height'], bins=20, color='#FF69B4', edgecolor='black', alpha = 0.8, label='Female')
    axs[1].set_xlabel('Height (cm)', fontsize = label_size)
    #axs[1].set_ylabel('Frequency', fontsize = label_size)
    axs[1].set_title('Height Distribution', fontweight='bold', fontsize = title_size)
    axs[1].tick_params(axis='x', labelsize=tick_size)
    axs[1].tick_params(axis='y', labelsize=tick_size)
    axs[1].legend(fontsize=legend_fontsize)

    # WEIGHT DISTRIBUTION PLOT 
    axs[2].hist(df[df['Sex'] == 'M']['Weight'], bins=20, color='#4169E1', edgecolor='black', alpha = 0.8, label='Male')
    axs[2].hist(df[df['Sex'] == 'F']['Weight'], bins=20, color='#FF1493', edgecolor='black', alpha = 0.8, label='Female')
    axs[2].set_xlabel('Weight (kg)', fontsize = label_size)
    #axs[2].set_ylabel('Frequency', fontsize = label_size)
    axs[2].set_title('Weight Distribution', fontweight='bold', fontsize = title_size)
    axs[2].tick_params(axis='x', labelsize=tick_size)
    axs[2].tick_params(axis='y', labelsize=tick_size)
    axs[2].legend(fontsize=legend_fontsize)
    plt.tight_layout()

    return fig