import pygal
from .models import *

# Factory method
def drawGraph(type, name, graphdata):
    if (type == 'bar'):
        bar(name, graphdata)
    elif (type == 'horizBar'):
        horizBar(name, graphdata)
    elif (type == 'pie'):
        pie(name, graphdata)
    else:
        print('adsf')

def bar(name, graphdata):
    chart = pygal.Bar(show_legend = False)
    chart.title = name
    x_labels = []
    x_data = []
    for data in graphdata:
        x_labels.append(data[0])
        x_data.append(data[1])
    chart.x_labels = x_data
    chart.add(name, x_data)
    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 

def pie(name, graphdata):
    chart = pygal.Pie(inner_radius = 0.2, show_legend = False)
    chart.title = name
    for data in graphdata:
        chart.add(data[0], data[1])
    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 

def horizBar(name, graphdata):
    chart = pygal.HorizontalBar(show_legend = False)
    chart.title = name
    x_labels = []
    x_data = []
    for data in graphdata:
        x_labels.append(data[0])
        x_data.append(data[1])
    chart.x_labels = x_data
    chart.add(name, x_data)
    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
