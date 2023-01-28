from bokeh.embed import components
from flask import Flask, render_template, request
import pytrends
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
from io import BytesIO
import base64
import urllib

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Google trends' oldest date is 2004-01-01

@app.route('/graph', methods=['POST'])
def graph():
    # Get the user's input
    word = request.form['word']
    # timeframe = request.form['timeframe']
    timeframe = request.form['timeframe-start'] + ' ' + request.form['timeframe-end']

    # Authenticate and connect to the API
    pytrends = TrendReq()

    # Get data from the API
    pytrends.build_payload(kw_list=[word], timeframe=timeframe)
    data = pytrends.interest_over_time()

    # Create new figure
    # plt.figure()

    # Create a plot (bokeh)
    bokeh_plot = figure(title=f'Popularity of "{word}" over time',
                        x_axis_label='Time',
                        x_axis_type='datetime',
                        y_axis_label='Popularity')
    bokeh_plot.xaxis[0].ticker.desired_num_ticks = 7
    bokeh_plot.line(data.index, data[word], line_width=2)

    html = file_html(bokeh_plot, CDN, "my plot")
    return html


if __name__ == '__main__':
    app.run(debug=True)
