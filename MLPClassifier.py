import pandas as pd
from pytrends.request import TrendReq
import pytrends
from functionsForMLP import *
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.pipeline import make_pipeline

pytrend = TrendReq()
kw_list = ["word"]
pytrends.build_payload(kw_list, timeframe='today 5-y')

trend = pytrend.interest_over_time()
stock = pd.read_csv("S&P.csv")
stock = stock.drop(['High', 'Low'], axis=1)
stock['target'] = target_binary(stock.Close)
stock = stock.reset_index()

# Combine Google Trends and Stock Prices in one CSV file ("stock")
trends = []
for trend in trend["NAME COLUMN"]: #name of volume of trade
    trends.append(trend)

stock["Trend"] = trends

data = stock
print(data.head())

# Clean up and preprocess the data
def preprocess(data):
    x = data.iloc[:]
    y = data.iloc[:]

    return x, y


all_X, all_y = preprocess(data)

X_train, X_test, y_train, y_test = train_test_split(all_X, all_y, shuffle=False)
print(X_train.shape)

# MLP Classifier

clf = MLPClassifier(max_iter=200)
clf.fit(X_train, y_train)

print(clf.score(X_test, y_test))

# Predictions on new data
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
