from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource
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

    trend_data = get_word_data(word, start + ' ' + end)
    stock_data = get_stock_data('AAPL', start, end)

    # Create a plot (bokeh)
    bokeh_plot = figure(title=f'Popularity of "{word}" over time',
                        x_axis_label='Date',
                        x_axis_type='datetime',
                        y_axis_label='Popularity',
                        )
    bokeh_plot.line(trend_data.index, trend_data[word], line_width=2)
    bokeh_plot.line(stock_data.index, stock_data['Close'], line_width=2, color='red')
    bokeh_plot.xaxis[0].ticker.desired_num_ticks = 10
    bokeh_plot.legend.location = 'top_left'
    bokeh_plot.legend.click_policy = 'hide'
    html = file_html(bokeh_plot, CDN, "my plot")

    # embed html in the template (graph.html)

    # tech demo part
    stocks = get_stocks_data('AAPL MSFT GOOG', start, end)

    stocks_graph = figure(title="Tech Stocks", x_axis_label='Date', y_axis_label='Percentage Growth',
                          x_axis_type='datetime')

    for ticker in stocks['Close'].columns:
        stocks_graph.line(stocks.index, stocks['Close', ticker], line_width=2, legend_label=ticker)

    stocks_graph.legend.location = 'top_left'
    stocks_graph.legend.click_policy = 'hide'

    techdemo_html = file_html(stocks_graph, CDN, "tech demo plot")

    # end of tech demo part

    return render_template('graph.html', plot_div=html, techdemo_div=techdemo_html)


def get_word_data(word, timeframe, geo=''):
    app.logger.info(f'Getting data for {word} during {timeframe} at {geo}...')
    # this logging thing doesn't work for some reason, fix

    # Authenticate and connect to the API
    pytr = TrendReq()
    # Get data from the API
    pytr.build_payload(kw_list=[word], timeframe=timeframe, geo=geo)
    data = pytr.interest_over_time()
    return data


def get_stock_data(ticker_name, start, end):
    app.logger.info(f'Getting data for {ticker_name} from {start} to {end}...')
    # this logging thing doesn't work for some reason, fix

    ticker = yf.Ticker(ticker_name)
    # Get data from the API
    data = ticker.history(start=start, end=end)
    return data


def get_stocks_data(ticker_names, start, end):
    app.logger.info(f'Getting data for {ticker_names} from {start} to {end}...')
    # this logging thing doesn't work for some reason, fix
    tickers = yf.Tickers(ticker_names) # ex: 'AAPL MSFT GOOG'
    stocks = tickers.history(start=start, end=end)
    return stocks


if __name__ == '__main__':
    app.run(debug=True)
