import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Fetch Stock Data
def fetch_stock_data(stock_symbol="TSLA", api_key=None):
    if api_key is None:
        raise ValueError("API Key is required")

    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": api_key
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print("Error fetching stock data")
        return None

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df = df.astype(float)
    df = df[::-1]  # Reverse to chronological order
    df["Date"] = pd.to_datetime(df.index)
    df.set_index("Date", inplace=True)
    df = df.rename(columns={
        "1. open": "Open", "2. high": "High",
        "3. low": "Low", "4. close": "Close",
        "5. volume": "Volume"
    })
    return df


# Prepare Data for Training
def prepare_data(df):
    df["Next Close"] = df["Close"].shift(-1)  # Shift for prediction
    df.dropna(inplace=True)

    X = df[["Open", "High", "Low", "Volume"]]
    y = df["Next Close"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
def train_model(stock_symbol, api_key):
    df = fetch_stock_data(stock_symbol, api_key)
    if df is None:
        return None, None

    X_train, X_test, y_train, y_test = prepare_data(df)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    error = mean_absolute_error(y_test, y_pred)

    print(f"Model trained for {stock_symbol}. MAE: {error:.2f}")

    return model, df

# Predict Next Day Stock Price
def predict_next_day(model, df):
    latest_data = df.iloc[-1][["Open", "High", "Low", "Volume"]].to_frame().T  # Convert to DataFrame
    predicted_price = model.predict(latest_data)[0]
    return predicted_price
