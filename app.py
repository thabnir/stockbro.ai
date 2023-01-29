import csv
import os
import sys

import pandas as pd
import yfinance as yf
import openai
from bokeh.embed import file_html
from bokeh.models import Range1d, LinearAxis, WheelZoomTool, HoverTool
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template, request
from pytrends.request import TrendReq
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

ticker_list = []
with open("tickers_new_sorted.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        ticker_list.append(row[0])  # Add the ticker to the list

with open('openai.txt', 'r') as f:
    prompt = f.read().strip()


class InputForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired()])
    stock_ticker = StringField('Stock Ticker', validators=[DataRequired()])
    timeframe_start = StringField('Start Date', validators=[DataRequired()])
    timeframe_end = StringField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    # print('Hello world!', file=sys.stderr)
    return render_template('index.html', ticker_list=ticker_list)


def generate_sass(word, ticker, correlation, sample_size, start_date, end_date):
    full_prompt = prompt + f'{ticker}|{word}|{correlation}|{sample_size}|{start_date}|{end_date} -> '
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=full_prompt,
        temperature=0.7,
        max_tokens=100,
    )
    return response.choices[0].text


@app.route('/graph', methods=['POST'])
def graph():
    print('Trying to graph', file=sys.stderr)
    # for key in request.form:
    #     print(f'{key}: {request.form[key]}', file=sys.stderr)
    # Get the user's input
    if request.form['word'] == '' or request.form['stock-ticker'] == '' \
            or request.form['timeframe-start'] == '' or request.form['timeframe-end'] == '':
        return render_template('index.html', ticker_list=ticker_list, error='Error: Please fill out all fields')
    word = request.form['word']
    ticker = request.form['stock-ticker']
    start = request.form['timeframe-start']
    end = request.form['timeframe-end']

    if start > end:
        return render_template('index.html', ticker_list=ticker_list, error='Error: Start date must be before end date')

    # Get the data
    trend_data = get_trend_data(word, start + ' ' + end)
    stock_data = get_stock_data(ticker, start, end)

    if stock_data is None:
        return render_template('index.html', ticker_list=ticker_list, error='Error: Invalid ticker')
    elif trend_data is None:
        return render_template('index.html', ticker_list=ticker_list, error='Error: Invalid trend data')

    html = plot_data(word, ticker, trend_data, stock_data)

    correlation, sample_size = get_correlation(trend_data[word], stock_data['Close'])
    print(f'Correlation from {sample_size} samples: {correlation}', file=sys.stderr)

    if pd.isna(correlation):
        correlation = 'Not enough data'
    # embeds html in the template (graph.html)
    return render_template(
        'graph.html',
        plot_div=html,
        correlation=correlation,
        samples=sample_size,
        ai_commentary=generate_sass(word, ticker, correlation, sample_size, start, end),
        word=word,
        ticker=ticker,
    )


def plot_data(word, ticker, trend_data, stock_data):
    print(f'Graphing data for {word} and {ticker}...', file=sys.stderr)
    # Create a plot (bokeh)
    p = figure(title=f'Popularity of "{word}" and price of {ticker} over time',
               x_axis_label='Date',
               x_axis_type='datetime',
               y_axis_label='Popularity',
               )

    # Plot word popularity
    p.line(trend_data.index, trend_data[word], line_width=2, legend_label=word)
    p.y_range = Range1d(trend_data[word].min() - 1, trend_data[word].max() + 1)

    stock_range = "second y" + "_range"
    p.extra_y_ranges = {stock_range: Range1d(stock_data['Close'].min() - 1, stock_data['Close'].max() + 1)}
    # label the right y-axis
    p.add_layout(LinearAxis(y_range_name=stock_range, axis_label='Price (USD)'), 'right')

    # Plot stock price
    p.line(stock_data.index,
           stock_data['Close'],
           line_width=2, color='red',
           legend_label=ticker,
           y_range_name=stock_range)

    p.add_layout(LinearAxis(y_range_name=stock_range), "right")

    p.xaxis[0].ticker.desired_num_ticks = 10
    p.legend.location = 'top_left'
    p.legend.click_policy = 'hide'
    # set wheel zoom to on by default
    p.toolbar.active_scroll = p.select_one(WheelZoomTool)
    p.title.text_font_size = '16pt'

    # add a hover tool that shows the date and the popularity to the word
    hover = HoverTool(tooltips=[('Date', '@x{%F}'), ('Popularity', '@y')],
                      formatters={'@x': 'datetime'},
                      mode='vline')
    p.add_tools(hover)

    # add a hover tool that shows the date and the price to the stock
    hover = HoverTool(tooltips=[('Date', '@x{%F}'), (ticker, '$@y')],
                      formatters={'@x': 'datetime'},
                      mode='vline',
                      renderers=[p.renderers[1]])
    p.add_tools(hover)

    html = file_html(p, CDN, "my plot")
    return html


def get_trend_data(word, timeframe, geo=''):
    print(f'Getting data for {word} during {timeframe} at {geo}...', file=sys.stderr)
    # Authenticate and connect to the API
    pytr = TrendReq()
    # Get data from the API
    pytr.build_payload(kw_list=[word], timeframe=timeframe, geo=geo)
    data = pytr.interest_over_time()
    return data


def get_stock_data(ticker_name, start, end):
    print(f'Getting data for {ticker_name} from {start} to {end}...', file=sys.stderr)
    ticker = yf.Ticker(ticker_name)
    # Get data from the API
    data = ticker.history(start=start, end=end)
    return data


def get_correlation(word_data, stock_close_data):
    print(f'Getting correlation between\n{word_data}\nand\n{stock_close_data}\n...', file=sys.stderr)
    net_data = get_merged_data(word_data, stock_close_data)
    print(f'Correlation between {word_data.name} and Close:\n{net_data[word_data.name].corr(net_data["Close"])}',
          file=sys.stderr)
    correlation = net_data[word_data.name].corr(net_data['Close'])
    return correlation, net_data.size


def get_merged_data(word_data, stock_close_data):
    # convert stock_data from datetime64[ns, America/New_York] to datetime64[ns]
    stock_close_data.index = stock_close_data.index.tz_localize(None)
    # Merge the data
    merged_data = pd.merge(word_data, stock_close_data, left_on='date', right_on='Date')
    # merged_data = pd.merge(word_data, stock_close_data, left_index=True, right_index=True)
    # merged_data = merged_data.dropna()
    print(f'Merged data:\n{merged_data}', file=sys.stderr)
    return merged_data


def get_stocks_data(ticker_names, start, end):
    print(f'Getting data for {ticker_names} from {start} to {end}...', file=sys.stderr)
    tickers = yf.Tickers(ticker_names)  # ex: 'AAPL MSFT GOOG'
    stocks = tickers.history(start=start, end=end)
    return stocks


if __name__ == '__main__':
    app.run(debug=True)
