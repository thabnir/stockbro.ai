from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template, request
from pytrends.request import TrendReq
import yfinance as yf

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph():
    # Get the user's input
    word = request.form['word']
    stock = request.form['stock-ticker']
    start = request.form['timeframe-start']
    end = request.form['timeframe-end']

    trend_data = get_trend_data(word, start + ' ' + end)
    stock_data = get_stock_data('AAPL', start, end)

    # Create a plot (bokeh)
    bokeh_plot = figure(title=f'Popularity of "{word}" over time',
                        x_axis_label='Time',
                        x_axis_type='datetime',
                        y_axis_label='Popularity',
                        )
    bokeh_plot.line(trend_data.index, trend_data[word], line_width=2)
    bokeh_plot.xaxis[0].ticker.desired_num_ticks = 10
    html = file_html(bokeh_plot, CDN, "my plot")

    # embed html in the template (graph.html)
    return render_template('graph.html',
                           plot_div=html
                           )


def get_trend_data(word, timeframe, geo=''):
    app.logger.info(f'Getting data for {word} during {timeframe} at {geo}...')
    # Authenticate and connect to the API
    pytr = TrendReq()
    # Get data from the API
    pytr.build_payload(kw_list=[word], timeframe=timeframe, geo=geo)
    data = pytr.interest_over_time()
    return data


def get_stock_data(ticker_name, start, end):
    app.logger.info(f'Getting data for {ticker_name} from {start} to {end}...')
    ticker = yf.Ticker(ticker_name)
    # Get data from the API
    data = ticker.history(start=start, end=end)
    # data = yf.download(ticker, start=start, end=end)
    return data


if __name__ == '__main__':
    app.run(debug=True)
