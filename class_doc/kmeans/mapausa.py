# -*- coding: ascii -*-
"""
Created on Wed Mar 09 13:12:02 2016

@author: FranciscoP.Romero
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap

def show_usa_map(labels):
    
    # create the map
    map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    
    # load the shapefile, use the name 'states'
    map.readshapefile('st99_d00', name='states', drawbounds=True)
    
    # collect the state names from the shapefile attributes so we can
    # look up the shape obect for a state by it's name
    state_names = []
    for shape_dict in map.states_info:
        state_names.append(shape_dict['NAME'])
    
    # extract the list names
    #lst = list(set(state_names))
    #lst.sort()   
    lst = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'] 
    
    
    
    
    colors = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow', 'black']
    
    ax = plt.gca() # get current axes instance
    
    for i in range(len(map.states)):
        seg = map.states[i]
        if state_names[i] != 'Puerto Rico':
            idx = lst.index(state_names[i])
            poly = Polygon(seg, facecolor=colors[labels[idx]],edgecolor=colors[labels[idx]])
            ax.add_patch(poly)
    
    # get Texas and draw the filled polygon
    #seg = map.states[state_names.index('Texas')]
    #poly = Polygon(seg, facecolor='red',edgecolor='red')
    #ax.add_patch(poly)
    
    plt.show()