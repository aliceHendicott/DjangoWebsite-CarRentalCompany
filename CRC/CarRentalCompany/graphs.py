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
    chart = pygal.Bar() # Then create a
    chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 1]) # Add some values
    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 

def pie(name, graphdata):
    chart = pygal.Pie(inner_radius = 0.2)
    chart.title = 'Browser usage in February 2012 (in %)'
    chart.add('IE', 4)
    chart.add('Firefox', 11)
    chart.add('Chrome', 20)
    chart.add('Safari', 1)
    chart.add('Opera', 2.3)
    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
def horizBar(name, graphdata):    chart = pygal.HorizontalBar()
    chart.title = 'Browser usage evolution (in %)'
    chart.x_labels = map(str, range(2002, 2013))
    chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    chart.range = [0, 100]    chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
