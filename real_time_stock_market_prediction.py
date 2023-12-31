# -*- coding: utf-8 -*-
"""Real-Time Stock Market Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G3pk3fWtEj20VnEl-8RtvdPYZy7T6Pa4
"""

# Commented out IPython magic to ensure Python compatibility.
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
# %matplotlib inline
from sklearn.metrics import mean_absolute_error, mean_squared_error

company_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'GS', 'WMT', 'KO']
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

company_data = {}

for symbol in company_symbols:
    df = yf.download(symbol, start=start_date, end=end_date)
    company_data[symbol] = df

df

company_models={}
for symbol, df in company_data.items():
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    df['Target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    X = df[['Close']]
    y = df['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    company_models[symbol] = model

for symbol, df in company_data.items():
    model = company_models[symbol]
    X_test = df[['Close']].tail(1)  # Use the last closing price for testing
    y_test = df['Close'].tail(1)  # True value for the last day
    y_pred = model.predict(X_test)

    # Calculate and print evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f"Company: {symbol}")
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print("\n")

# Calculate daily returns for each company
# Calculate daily returns for each company
for symbol, df in company_data.items():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.title(f'Closing Price for {symbol}')
    plt.grid(True)
    plt.show()

for symbol, df in company_data.items():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Volume'], label='Volume', color='green')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.title(f'Sales Volume for {symbol}')
    plt.grid(True)
    plt.show()

for symbol, df in company_data.items():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label=symbol)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.title(f'Stock Price Movements for {symbol}')
    plt.grid(True)
    plt.show()

# Generate random data as a placeholder for tech_rets
np.random.seed(42)
data = np.random.randn(100, 10)
tech_rets = pd.DataFrame(data, columns=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'GS', 'WMT', 'KO'])

rets = tech_rets.dropna()

area = np.pi * 20

plt.figure(figsize=(10, 8))
plt.scatter(rets.mean(), rets.std(), s=area)
plt.xlabel('Expected return')
plt.ylabel('Risk')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom',
                 arrowprops=dict(arrowstyle='-', color='blue', connectionstyle='arc3,rad=-0.3'))

plt.show()

for symbol, model in company_models.items():
    latest_closing_price = company_data[symbol]['Close'].iloc[-1]
    latest_data = pd.DataFrame({'Close': [latest_closing_price]})
    predicted_price = model.predict(latest_data)
    print(f"Predicted Price for {symbol} on the next day: {predicted_price[0]}")