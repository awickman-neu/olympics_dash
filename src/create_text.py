import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image as XLImage

#FUNCTION TO CREATE DASHBOARD HEADER
def create_text_fig(text, figsize):
    fig, ax = plt.subplots(figsize = figsize)
    ax.axis('off')
    ax.text(0.5, 0.5, text, fontsize = 19, ha = 'center', va = 'center', fontweight = 'bold')
    return fig

#FUNCTION TO CREATE STATISTICS SECTION
def create_stat_widgets(value, title, face_color):
    fig, ax = plt.subplots(figsize=(2.8, 1.4))
    ax.axis('off')
    ax.text(0.5, 0.5, f"{value}\n{title}", fontsize=14, ha='center', va='center', fontweight = 'bold', color = 'white')

    #set background color of figure 
    fig.patch.set_facecolor(face_color)
    
    widget_image_path = f"../Coursework_2/outputs/{title.replace(' ', '_').lower()}_widget.png"
    fig.savefig(widget_image_path, bbox_inches='tight')
    plt.close(fig)

    widget_image = XLImage(widget_image_path)

    return widget_image
