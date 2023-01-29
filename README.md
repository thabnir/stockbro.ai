Project built for McHacks 10
by Thabnir, clarariachi & Rain1618

## Inspiration
Money. Stonks. We like that.
We were originally inspired by a research paper (see below) which found that the search volume of certain words associated with the economy (e.g. debt) could be indicative of the general direction of the stock market and predict future stock movements. We wanted to extend this idea and see if we could find other keywords that may be indicative of the future of the stock market. As data can be sometimes tedious to understand, we also built a bot that tells you in no uncertain terms whether of not there is a correlation between the keyword and the stock (and occasionally _questions_ the thought process behind your selection). 

Said research paper: 
Preis, T., Moat, H. & Stanley, H. Quantifying Trading Behavior in Financial Markets Using Google Trends. Sci Rep 3, 1684 (2013). [link]https://doi.org/10.1038/srep01684
## What it does
Stock Bro AI attempts to predict the stock market by finding obscure correlations between a stock's prices and Google Trends over time by calculating the Pearson correlation coefficient. Spoiler: it doesn't work. It also regularly sends sardonic comments to put finance bros who think they know how the stock market works in their place.
## How we built it
We made a Flask app and used html  + Bokeh to plot graphs showing correlations between a Google search's popularity over time and the associated stock's price. A variety of data science libraries like pandas along with yfinance and pytrends were used to retrieve and process the necessary data from Yahoo Finance and Google Trends respectively. 
## Challenges we ran into
We first made our chatbot using Cohere but had to redo it by training it with OpenAI to be able to  implement it into the project with a more expansive training set. We also had to make the dataset used to train the robot as there are no preexisting dataset that quite fit our criteria of condescending, sarcastic and cynically humorous. Furthermore, it was challenging to integrate the various tools we used to build the app and the behind-the-scenes data.
## Accomplishments that we're proud of
We're proud of being able to make a working project in under 24 hours by learning as we go, especially as none of us had extensive previous experience with any of the tools we used. We also found the robot very funny (unsurprising as it was trained on insults we wrote) :smirk:
## What we learned
We had to read up on and implement a variety of data science concepts in order to process large amounts of data and create interactive visualizations of said data. Additionally, we learned how to use Flask, pandas, pytrends, yfinance, bokeh, NLP, basic HTML... and trained a little bot to say bad things! Most importantly, we learned that Stackoverflow takes you far in life. 
## What's next for Stock Bro AI
I'll let it tell you what's next: it's constantly making "predictions"! We will also work on implementing a proper machine learning model (perhaps an MLP Classifier) as inspired by the literature and see if it is able to predict the up and downturns of the stock market more closely. If the urge strikes, we might also improve upon the _aesthetics_ of the website.
