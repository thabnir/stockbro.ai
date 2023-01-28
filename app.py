from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template, request
from pytrends.request import TrendReq

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph():
    # Get the user's input
    word = request.form['word']
    timeframe = request.form['timeframe-start'] + ' ' + request.form['timeframe-end']
    data = get_trend_data(word, timeframe)

    # Create a plot (bokeh)
    bokeh_plot = figure(title=f'Popularity of "{word}" over time',
                        x_axis_label='Time',
                        x_axis_type='datetime',
                        y_axis_label='Popularity')
    bokeh_plot.line(data.index, data[word], line_width=2)
    bokeh_plot.xaxis[0].ticker.desired_num_ticks = 10
    html = file_html(bokeh_plot, CDN, "my plot")
    # embed html in the template (graph.html)
    return render_template('graph.html', plot_div=html)


def get_trend_data(word, timeframe, geo=''):
    # Authenticate and connect to the API
    pytr = TrendReq()
    # Get data from the API
    pytr.build_payload(kw_list=[word], timeframe=timeframe, geo=geo)
    data = pytr.interest_over_time()
    return data


if __name__ == '__main__':
    app.run(debug=True)
