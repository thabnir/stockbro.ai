from bokeh.embed import file_html
from bokeh.models import Range1d, LinearAxis
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template, request
from pytrends.request import TrendReq
import yfinance as yf
import logging

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph():
    # Get the user's input
    word = request.form['word']
    user_stock = request.form['stock-ticker']
    start = request.form['timeframe-start']
    end = request.form['timeframe-end']
    html = graph_data(word, user_stock, start, end)
    # embeds html in the template (graph.html)
    return render_template('index.html', plot_div=html)


def graph_data(word, user_stock, start, end):
    trend_data = get_word_data(word, start + ' ' + end)
    stock_data = get_stock_data(user_stock, start, end)

    # Create a plot (bokeh)
    bokeh_plot = figure(title=f'Popularity of the word "{word}" and {user_stock} stock price over time',
                        x_axis_label='Date',
                        x_axis_type='datetime',
                        y_axis_label='Popularity',
                        )
    # Plot word popularity
    bokeh_plot.line(trend_data.index, trend_data[word], line_width=2, legend_label=word)
    bokeh_plot.y_range = Range1d(trend_data[word].min() - 1, trend_data[word].max() + 1)

    stock_range = "second y" + "_range"
    bokeh_plot.extra_y_ranges = {stock_range: Range1d(stock_data['Close'].min() - 1, stock_data['Close'].max() + 1)}

    # Plot stock price
    bokeh_plot.line(stock_data.index,
                    stock_data['Close'],
                    line_width=2, color='red',
                    legend_label=user_stock,
                    y_range_name=stock_range
                    )

    bokeh_plot.add_layout(LinearAxis(y_range_name=stock_range), "right")

    bokeh_plot.xaxis[0].ticker.desired_num_ticks = 10
    bokeh_plot.legend.location = 'top_left'
    bokeh_plot.legend.click_policy = 'hide'

    html = file_html(bokeh_plot, CDN, "my plot")
    return html


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
    tickers = yf.Tickers(ticker_names)  # ex: 'AAPL MSFT GOOG'
    stocks = tickers.history(start=start, end=end)
    return stocks


if __name__ == '__main__':
    app.run(debug=True)
