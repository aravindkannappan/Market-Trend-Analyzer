## Market Trend Analyzer
# Overview
The Market Trend Analyzer is a Python-based tool for analyzing stock or cryptocurrency market trends. It fetches historical price data, calculates technical indicators (SMA, EMA, RSI, MACD), detects bullish/bearish trends, and visualizes results with candlestick charts. The tool supports both stocks (via yfinance) and cryptocurrencies (via ccxt) and saves analysis results to a CSV file.
Features

Data Fetching: Retrieves historical price data for stocks or cryptocurrencies.
Technical Indicators:
Simple Moving Average (SMA)
Exponential Moving Average (EMA)
Relative Strength Index (RSI)
Moving Average Convergence Divergence (MACD)


Trend Detection: Identifies bullish, bearish, or neutral trends based on SMA and RSI.
Visualization: Generates candlestick charts with indicators using matplotlib and mplfinance.
Output: Saves analysis to a CSV file and chart to a PNG file.
Logging: Logs operations and errors to a file (market_analyzer.log) and console.

## Requirements

Python 3.8+
Required libraries:pip install yfinance ccxt pandas numpy matplotlib seaborn mplfinance



## Installation

Clone or download the repository.
Install dependencies:pip install -r requirements.txt

Alternatively, install individually:pip install yfinance ccxt pandas numpy matplotlib seaborn mplfinance



## Usage
Run the analyzer from the command line with the following arguments:
python market_trend_analyzer.py --symbol <SYMBOL> --market <MARKET> --timeframe <TIMEFRAME> --start-date <START_DATE> --end-date <END_DATE> --output-csv <CSV_FILE> --output-plot <PLOT_FILE>

## Arguments

--symbol: Market symbol (e.g., AAPL for Apple stock, BTC/USDT for Bitcoin).
--market: Market type (stock or crypto). Default: stock.
--timeframe: Data timeframe (e.g., 1d for daily, 1h for hourly). Default: 1d.
--start-date: Start date (YYYY-MM-DD). Default: 1 year ago.
--end-date: End date (YYYY-MM-DD). Default: today.
--output-csv: Output CSV file path. Default: market_analysis.csv.
--output-plot: Output plot file path. Default: market_trend.png.

## Example
Analyze Apple stock for the past year:
python market_trend_analyzer.py --symbol AAPL --market stock --timeframe 1d --start-date 2024-05-27 --end-date 2025-05-27 --output-csv apple_analysis.csv --output-plot apple_trend.png

## Analyze Bitcoin (BTC/USDT) for the past 30 days:
python market_trend_analyzer.py --symbol BTC/USDT --market crypto --timeframe 1h --start-date 2025-04-27 --end-date 2025-05-27 --output-csv btc_analysis.csv --output-plot btc_trend.png

## Output

CSV File: Contains price data and calculated indicators (e.g., SMA, EMA, RSI, MACD, Trend).
PNG File: Candlestick chart with price, moving averages, RSI, and MACD.
Log File: market_analyzer.log records operations and errors.

## Technical Details

Data Sources:
Stocks: yfinance (Yahoo Finance API).
Cryptocurrencies: ccxt (Binance exchange).


## Indicators:
SMA: 20-day and 50-day.
EMA: 20-day.
RSI: 14-period.
MACD: 12-26-9 configuration.


Trend Detection: Combines SMA crossover and RSI thresholds.
Visualization: Uses mplfinance for candlestick charts and matplotlib for indicator plots.

## Limitations

Requires internet access for data fetching.
Cryptocurrency data is limited to exchanges supported by ccxt (e.g., Binance).
Timeframe support depends on the data source (e.g., 1h, 1d).
No real-time data; historical data only.

## Troubleshooting

No data retrieved: Check symbol format, date range, or internet connection.
Module not found: Ensure all dependencies are installed.
Invalid timeframe: Use supported timeframes (1h, 1d, etc.).
Check market_analyzer.log for detailed error messages.

## Contributing
Feel free to submit issues or pull requests for improvements, such as additional indicators or data sources.
License
This project is licensed under the MIT License.

