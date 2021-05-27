import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.cm as cm

# https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021
df = pd.read_csv('/data/world-happiness-report-2021.csv')

# define variables
x_name = 'Healthy life expectancy'
y_name = 'Freedom to make life choices'
tooltip_name = 'Country name'

x = df[x_name]
y = df[y_name]
tt = df[tooltip_name].values

indicators = {'gdp':{
                'name':'Log GDP per capita',
                'values':df['Logged GDP per capita'].values,
                'poly':Polygon([(0, 1.4), (0, 1.6), (2, 1.6), (2, 1.4)])
              },
              'ss':{
                'name':'Social support',
                'values':df['Social support'].values,
                'poly':Polygon([(0, 1.2), (0, 1.4), (2, 1.4), (2, 1.2)]) 
              },
              'gen':{
                'name':'Generosity',
                'values':df['Generosity'].values,
                'poly':Polygon([(0, 1.), (0, 1.2), (2, 1.2), (2, 1.)])
              },
              'poc':{
                'name':'Perceptions of corruption',
                'values':df['Perceptions of corruption'].values,
                'poly':Polygon([(0, 0.8), (0, 1.), (2, 1.), (2, 0.8)]) 
              }
             }

# define figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4), gridspec_kw={'width_ratios': [2, 1]}, facecolor='#393939')
ax1.tick_params(axis='both', colors='w')
cmap = plt.get_cmap("viridis")
plt.suptitle('World Happiness Report - 2021', color='w')

# scatter plot
sc = ax1.scatter(x, y, color='black')

# axis 1 labels
ax1.set_xlabel(x_name, color='w')
ax1.set_ylabel(y_name, color='w')

# axis 2 ticks and limits
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlim(0,2)
ax2.set_ylim(0,2)

# place holder for country name in axis 2
cnt = ax2.text(1, 1.8, '', ha='center', fontsize=12)

# indicator texts in axis 2
txt_x = 1.8
txt_y = 1.5
for ind in indicators.keys():
    n = indicators[ind]['name']
    indicators[ind]['txt'] = ax2.text(txt_x, txt_y, n.ljust(len(n)+13), ha='right', fontsize=8)
    txt_y -= 0.2

# line break in axis 2
ax2.plot([0,2],[txt_y-0.1, txt_y-0.1], lw=3, color='#393939')

# annotation / tooltip
annot = ax1.annotate("", xy=(0,0), xytext=(5,5),textcoords="offset points", bbox=dict(boxstyle="round,pad=0.3", fc="w", lw=2))
annot.set_visible(False)

# xy limits
ax1.set_xlim(x.min()*0.95, x.max()*1.05)
ax1.set_ylim(y.min()*0.95, y.max()*1.05)

# notes axis 2
note ="""This visualization was build to showcase
Matplotlib's mouse hover events."""
source = """Dataset at Kaggle: 
/ajaypalsinghlo/world-happiness-report-2021"""

ax2.text(0.05, 0.48, note, ha='left', va='top', fontsize=8)
ax2.text(0.05, 0.2, source, ha='left', va='top', fontsize=7)

# change color map of axis 1
def change_cmap(values, annotation):
    clean_ax2()
    sc.set_norm(plt.Normalize(np.nanmin(values), np.nan_to_num(values).max()))
    annotation.set_color('#2A74A2')
    sc.set_array(values)

# clean text in axis 2 and reset color of axis 1
def clean_ax2():
    for ind in indicators.keys():
        indicators[ind]['txt'].set_color('black')
    sc.set_color('black')

# cursor hover
def hover(event):
    # check if event was in axis 1
    if event.inaxes == ax1:        
        clean_ax2()
        # get the points contained in the event
        cont, ind = sc.contains(event)
        if cont:
            # change annotation position
            annot.xy = (event.xdata, event.ydata)
            # write the name of every point contained in the event
            countries = "{}".format(', '.join([tt[n] for n in ind["ind"]]))
            annot.set_text(countries)
            annot.set_visible(True)
            # get id of selected country
            country_id = ind["ind"][0]
            # set axis 2 country label
            cnt.set_text(tt[country_id])
            # set axis 2 indicators values
            for ind in indicators.keys():
                n = indicators[ind]['name']
                txt = indicators[ind]['txt']
                val = indicators[ind]['values'][country_id]
                txt.set_text('{}: {: 07.3f}'.format(n, val))
        # when stop hovering a point hide annotation
        else:
            annot.set_visible(False)
    # check if event was in axis 2
    elif event.inaxes == ax2:
        # bool to detect when mouse is not over text space
        reset_flag = False
        for ind in indicators.keys():
            # check if cursor position is in text space
            if indicators[ind]['poly'].contains(Point(event.xdata, event.ydata)):
                # clean axis 2 and change color map
                clean_ax2()
                change_cmap(indicators[ind]['values'], indicators[ind]['txt'])
                reset_flag = False
                break
            else:
                reset_flag = True
        # If cursor not over any text clean axis 2 
        if reset_flag:
            clean_ax2()
    fig.canvas.draw_idle()   

# when leaving any axis clean axis 2 and hide annotation
def leave_axes(event):
    clean_ax2()
    annot.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)
fig.canvas.mpl_connect('axes_leave_event', leave_axes)
plt.show()