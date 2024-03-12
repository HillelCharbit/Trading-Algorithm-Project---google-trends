from datetime import datetime
import numpy as np
import pandas as pd
import requests

# Function to make an API call to Binance
def make_api_call(base_url, endpoint="", method="GET", **kwargs):
    # Construct the full URL
    full_url = f'{base_url}{endpoint}'

    # Make the API call
    response = requests.request(method=method, url=full_url, **kwargs)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response
    else:
        # If the request was not successful, raise an exception with the error message
        raise Exception(f'API request failed with status code {response.status_code}: {response.text}')

def get_binance_historical_data(symbol, interval, start_date, end_date=None):
    # define basic parameters for call
    base_url = 'https://fapi.binance.com'
    endpoint = '/fapi/v1/klines'
    method = 'GET'

    # Set the start time parameter in the params dictionary
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': 1500,
        'startTime': start_date  # Start time in milliseconds
    }

    # If end_date is provided, set it in the params dictionary
    if end_date:
        params['endTime'] = end_date

    # Make initial API call to get candles
    response = make_api_call(base_url, endpoint=endpoint, method=method, params=params)

    candles_data = []

    while len(response.json()) > 0:
        # Append the received candles to the list
        candles_data.extend(response.json())

        # Update the start time for the next API call
        params['startTime'] = candles_data[-1][0] + 1  # last candle open_time + 1ms

        # If end_date is provided and the last candle's open_time is greater than or equal to end_date, stop fetching data
        if end_date and candles_data[-1][0] >= end_date:
            break

        # Make the next API call
        response = make_api_call(base_url, endpoint=endpoint, method=method, params=params)

    # Wrap the candles data as a pandas DataFrame
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
               'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
    dtype = {
        'open_time': 'datetime64[ms, Asia/Jerusalem]',
        'open': 'float64',
        'high': 'float64',
        'low': 'float64',
        'close': 'float64',
        'volume': 'float64',
        'close_time': 'datetime64[ms, Asia/Jerusalem]',
        'quote_asset_volume': 'float64',
        'number_of_trades': 'int64',
        'taker_buy_base_asset_volume': 'float64',
        'taker_buy_quote_asset_volume': 'float64',
        'ignore': 'float64'
    }

    df = pd.DataFrame(candles_data, columns=columns)
    df = df.astype(dtype)

    return df

# as you mentioned in the phone call, this could be problamatic to send the dataframe over and over again between the functions
# so instead i made 1 function that excepts the dataframe and calculates apon the dataframe all of the values needed that are applied in the pseudo code below

# Tom version of indicators
def TR(close: pd.Series, high: pd.Series, low: pd.Series) -> pd.Series:
    return (high.where(high > close.shift(1), close.shift(1)) - low.where(low < close.shift(1), close.shift(1)))

def ATR(TR: pd.Series, atr_length: int) -> pd.Series:
    return TR.rolling(window=atr_length).mean()

# crossover function
def CO(a: pd.Series, b: pd.Series) -> pd.Series:
    return (a > b) & (a.shift(1) < b.shift(1))

def UTBot(close, high, low, key_value, atr_length) -> pd.Series:
    lossThreshold = key_value * ATR(TR(close, high, low), atr_length)
    trailingStop = 0 * lossThreshold

    for i in range(1, len(trailingStop)):

        # the previous trailing stop is lower than the current and previous close
        if (close[i] > trailingStop[i - 1]) & (close[i - 1] > trailingStop[i - 1]):
            trailingStop[i] = max(trailingStop[i - 1], close[i] - lossThreshold[i])
        # the previous trailing stop is higher than the current and previous close
        elif (close[i] < trailingStop[i - 1]) & (close[i - 1] < trailingStop[i - 1]):
            trailingStop[i] = min(trailingStop[i - 1], close[i] - lossThreshold[i])
        # the previous trailing stop is lower than the current close and higher than the previous close
        elif (close[i] > trailingStop[i - 1]):
            trailingStop[i] = close[i] - lossThreshold[i]
        # the previous trailing stop is higher than the current close and lower than the previous close
        else:
            trailingStop[i] = close[i] + lossThreshold[i]

    above = CO(close, trailingStop)
    below = CO(trailingStop, close)


    Action = np.select([above, below], [ActionType.BUY, ActionType.SELL], default=ActionType.DONOTHING)
    

    # check if works properly!!!!!!
    return Action

# smoothing function
def SmoothSrs(srs, smoothing_f):
    smoothed_srs = srs.copy()
    for i in range(1, len(smoothed_srs)):
        if np.isnan(smoothed_srs[i-1]):
            smoothed_srs[i] = srs[i]
        else:
            smoothed_srs[i] = smoothed_srs[i-1] + smoothing_f * (srs[i] - smoothed_srs[i-1])
    return smoothed_srs

# normalization function with smoothing
def normNsmooth(srs, stc_length, smoothing_factor):
    # finding the lowest and highest range
    lowest = srs.rolling(stc_length).min()
    highestRange = srs.rolling(stc_length).max() - lowest
    
    # normalizing srs
    normalizedsrs = srs.copy()
    normalizedsrs[highestRange > 0] = ((srs - lowest) / highestRange * 100)*(highestRange > 0)
    normalizedsrs[highestRange <= 0] = np.nan
    normalizedsrs.fillna(method = 'ffill', inplace = True)

    # smoothing the srs
    return SmoothSrs(normalizedsrs, smoothing_factor)

# complete function for calculating osciallatior
def STCosi(srs, fast_length, slow_length, stc_length, smoothing_factor = 0.5):
    
    # ema calculation for fast and slow length's
    fast_ema = srs.ewm(span = fast_length).mean()
    slow_ema = srs.ewm(span = slow_length).mean()

    # MacdDiff calculation
    MacdDiff = fast_ema - slow_ema

    smoothedMacd = normNsmooth(MacdDiff, stc_length, smoothing_factor)
    FinalSTC = normNsmooth(smoothedMacd, stc_length, smoothing_factor)
    
    return FinalSTC

def calc_TR(df) -> pd.DataFrame:
    df['prev_close'] = df['close'].shift(1)

    df['TR'] = df.apply(lambda row: max(row['high'], row['prev_close']) - min(row['low'], row['prev_close']), axis=1)
    return df

def calc_ATR(df, atr_length) -> pd.DataFrame:
    df['ATR'] = df['TR'].rolling(window=atr_length).mean()
    return df

def calc_crossover(df, a, b, target_col_name):
    df[target_col_name] = (df[a] > df[b]) & (df[a].shift(1) < df[b].shift(1))
    return df

def calc_UTBot(df, key_value, atr_length):
    df['loss_threshold'] = key_value * df['ATR']
    df['trailing_stop'] = np.nan

    for i in range(1, len(df)):

        # upward trend
        if (df['close'][i] > df['trailing_stop'][i - 1]) & (df['close'][i - 1] > df['trailing_stop'][i - 1]):
            df['trailing_stop'][i] = max(df['trailing_stop'][i - 1], df['close'][i] - df['loss_threshold'][i])

        # downward trend
        elif (df['close'][i] < df['trailing_stop'][i - 1]) & (df['close'][i - 1] < df['trailing_stop'][i - 1]):
            df['trailing_stop'][i] = min(df['trailing_stop'][i - 1], df['close'][i] - df['loss_threshold'][i])

        elif (df['close'][i] > df['trailing_stop'][i - 1]):
            df['trailing_stop'][i] = df['close'][i] - df['loss_threshold'][i]

        else:
            df['trailing_stop'][i] = df['close'][i] + df['loss_threshold'][i]

        # stop loss

    df = calc_crossover(df, 'close', 'trailing_stop', 'crossover_above')
    df = calc_crossover(df, 'trailing_stop', 'close', 'crossover_below')

    df['buy'] = df.crossover_above.astype(int)
    df['sell'] = df.crossover_below.astype(int)
    return df

# done in STCosi
def EMACalc(df, length, target_col_name):
    df[target_col_name] = df['close'].ewm(span=length,min_periods=length, adjust=False).mean()
    return df

# done in STCosi
def MacdDiff(df, fast_length, slow_length):
    EMACalc(df, fast_length, 'fastEMA')
    EMACalc(df, slow_length, 'slowEMA')
    df['macd_diff'] = df['fastEMA'] - df['slowEMA']
    return df

# made a function for use in STCosi
def smooth_srs(srs, smoothing_f):
    smoothed_srs = []
    smoothed_srs[0] = srs[0]

    for i in range(1, len(srs)):
        if pd.isna(smoothed_srs[i - 1]):
            smoothed_srs[i] = srs[i]

        else:
            smoothed_srs[i] = smoothed_srs[i-1] + smoothing_f * (srs[i] - smoothed_srs[i-1])
    return smoothed_srs

# done in STCosi
def NormalizeSmoothSrs(series, window_length, smoothing_f):
    lowest = series.rolling(window_length).min()
    highest_range = series.rolling(window_length).max() - lowest

    normalized_series = series
    if(highest_range > 0):
        normalized_value = (series - lowest) / highest_range * 100
    else:
        normalized_value = np.nan
    normalized_series.ffill(inplace=True)

    smoothed_series = smooth_srs(normalized_series, smoothing_f)
    return smoothed_series

def STC(close, stc_length, fast_length, slow_length, smoothing_factor=0.5):
    macd_diff = MacdDiff(close, fast_length, slow_length)
    normalized_macd = NormalizeSmoothSrs(macd_diff, stc_length, smoothing_factor)
    final_stc = NormalizeSmoothSrs(normalized_macd, stc_length, smoothing_factor)
    return final_stc

def calc_ut_bot(df):
    df = calc_TR(df)
    df = calc_ATR(df, 15)
    df = calc_UTBot(df, key_value=1, atr_length=15)
    return df


def main():
    start_date = int(datetime(year=2024, month=1, day=1).timestamp() * 1000)
    end_date = int(datetime(year=2024, month=1, day=7).timestamp() * 1000)

    df = get_binance_historical_data('BTCUSDT', '30m', start_date, end_date)
    ut_bot = calc_ut_bot(df.copy())
    # need to change parameters for them not being magic numbers
    osi = STCosi(df.close, 23, 50, 10, 0.5)


if __name__ == '__main__':
    main()
