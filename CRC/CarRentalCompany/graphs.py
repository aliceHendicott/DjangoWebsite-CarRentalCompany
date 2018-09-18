import pygal

from .models import *

def testGraph():
    bar_chart = pygal.Bar() # Then create a
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 1]) # Add some values
    bar_chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/bar_chart.svg') 

def testGraph1():
    pie_chart = pygal.Pie(inner_radius = 0.2)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 4)
    pie_chart.add('Firefox', 11)
    pie_chart.add('Chrome', 20)
    pie_chart.add('Safari', 1)
    pie_chart.add('Opera', 2.3)
    pie_chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/pie_chart.svg') def testGraph2():    line_chart = pygal.HorizontalBar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.range = [0, 100]    line_chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/horiz_chart.svg') 