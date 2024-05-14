## SWEDISH EXCEL SPECS 

def get_fig_size(nr_cells_wide, nr_cells_high):

    #excel specs in points
    cell_width = 51
    cell_height = 14.42

    #inch conversion for figsize(.,.)
    inch_per_point = 1 / 72

    #convert specified number of cells dim to inches 
    cell_width_inch = nr_cells_wide * cell_width * inch_per_point
    cell_height_inch = nr_cells_high * cell_height * inch_per_point

    #return the fig size measurements for plot
    return cell_width_inch, cell_height_inch


