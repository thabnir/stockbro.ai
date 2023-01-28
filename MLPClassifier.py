import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

trend = pd.read_csv()
stock = pd.read_csv()

# Combine Google Trends and Stock Prices in one CSV file ("stock")
trends = []
for trend in trend["NAME COLUMN"]:
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

X_train, X_test, y_train, y_test = train_test_split(all_X, all_y)
print(X_train.shape)

# MLP Classifier

clf = MLPClassifier(max_iter=200)
clf.fit(X_train, y_train)

print(clf.score(X_test, y_test))

# Predictions on new data
clf.predict(X_test[15:25])  # some range
