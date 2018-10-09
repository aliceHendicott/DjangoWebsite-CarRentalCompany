import pygal
from pygal.style import Style
from .models import *

# Factory method to draw different graphs
def drawGraph(type, name, graphdata):
    if (type == 'bar'):
        return bar(name, graphdata)
    elif (type == 'horizBar'):
        return horizBar(name, graphdata)
    elif (type == 'pie'):
        return pie(name, graphdata)

# Styling the graphs
custom_style = Style(
    background = 'transparent',
    label_font_size = 28,
    legend_font_size = 32,
    opacity='.6',
    opacity_hover='.9',
    transition='350ms ease-out',
    font_family='googlefont:Raleway',
    tooltip_font_size = 32)

# Draw a bar graph and save it as svg
def bar(name, graphdata):
    # Create pie chart object and set title
    chart = pygal.Bar(show_legend = False, style = custom_style,
                      x_label_rotation = 30, y_labels_major_every = 1000)
    #chart.title = name

    # Turn data into respective data and label array
    x_labels = []
    x_data = []
    for data in graphdata:
        x_labels.append(data[0])
        x_data.append({'value': data[1], 
                       'xlink': '/cars/14806'})

    # Insert the data
    chart.add('', x_data)
    chart.x_labels = x_labels

    # Export to an svg file
    #chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
    return chart.render(is_unicode=True)


# Draw a horizontal bar graph and save it as svg
def horizBar(name, graphdata):
    # Create horizontal bar chart object and set title
    chart = pygal.HorizontalBar(show_legend = False, style = custom_style,
                                x_label_rotation = 15, y_labels_major_every = 1000)
    #chart.title = name

    # Turn data into respective data and label array
    x_labels = []
    x_data = []
    for data in graphdata:
        x_labels.append(data[0])
        x_data.append({'value': data[1], 
                       'xlink': '/cars/14806'})

    # Insert the data
    chart.add('', x_data)
    chart.x_labels = x_labels

    # Export to an svg file
    #chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
    return chart.render(is_unicode=True)


# Draw a pie graph and save it as svg
def pie(name, graphdata):
    # Create pie chart object and set title
    chart = pygal.Pie(inner_radius = 0.2, style = custom_style,
                      legend_at_bottom = True)
    #chart.title = name
    # Add data by iterating over input
    for data in graphdata:
        chart.add(data[0], [{
        'value': data[1],
        'xlink': '/stores/1'}])
    # Export to an svg file
    #chart.render_to_file('CarRentalCompany/templates/CarRentalCompany/Charts/' + name + '.svg') 
    return chart.render(is_unicode=True)

   

'''
class FruitPieChart():

    def __init__(self, **kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'Amount of Fruits'

    def get_data(self):
        
        #Query the db for chart data, pack them into a dict and return it.
        
        data = {}
        for fruit in Fruit.objects.all():
            data[fruit.name] = fruit.amt

        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for key, value in chart_data.items():
            self.chart.add(key, value)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)
'''