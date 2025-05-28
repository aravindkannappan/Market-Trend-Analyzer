# 📈 Market Trend Analyzer

## Overview
The Market Trend Analyzer is a Python-based tool for analyzing stock or cryptocurrency market trends.
It fetches historical price data, calculates technical indicators (SMA, EMA, RSI, MACD), detects bullish/bearish trends, 
and visualizes results with candlestick charts. 
The tool supports both stocks (via yfinance) and cryptocurrencies (via ccxt) and saves analysis results to a CSV file.

---

## Features
- Data Fetching: Retrieves historical price data for stocks or cryptocurrencies.
- Technical Indicators:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- Trend Detection: Identifies bullish, bearish, or neutral trends using SMA crossovers and RSI thresholds.
- Visualization: Candlestick charts with `matplotlib` and `mplfinance`
- Output: CSV with indicators and PNG chart
- Logging: All actions logged in `market_analyzer.log`

---

## Requirements
- Python 3.8+
- Dependencies:
  pip install yfinance ccxt pandas numpy matplotlib seaborn mplfinance

---

## Installation
1. Clone/download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install yfinance ccxt pandas numpy matplotlib seaborn mplfinance
```

---

## Usage
```bash
python market_trend_analyzer.py \
  --symbol <SYMBOL> \
  --market <MARKET> \
  --timeframe <TIMEFRAME> \
  --start-date <START_DATE> \
  --end-date <END_DATE> \
  --output-csv <CSV_FILE> \
  --output-plot <PLOT_FILE>
```

### Arguments
- `--symbol`: Market symbol (e.g., AAPL or BTC/USDT)
- `--market`: `stock` or `crypto` (default: `stock`)
- `--timeframe`: e.g., `1d`, `1h` (default: `1d`)
- `--start-date`: Format `YYYY-MM-DD`
- `--end-date`: Format `YYYY-MM-DD`
- `--output-csv`: Default `market_analysis.csv`
- `--output-plot`: Default `market_trend.png`

---

## Examples
### Apple Stock
```bash
python market_trend_analyzer.py --symbol AAPL --market stock --timeframe 1d \
--start-date 2024-05-27 --end-date 2025-05-27 \
--output-csv apple_analysis.csv --output-plot apple_trend.png
```

### Bitcoin
```bash
python market_trend_analyzer.py --symbol BTC/USDT --market crypto --timeframe 1h \
--start-date 2025-04-27 --end-date 2025-05-27 \
--output-csv btc_analysis.csv --output-plot btc_trend.png
```

---

## Output
- CSV File: Includes price data, SMA, EMA, RSI, MACD, Trend
- PNG File: Candlestick + moving averages and indicators
- Log File: `market_analyzer.log`

---

## 🔬 Technical Details
- Data Sources:
  - `yfinance` (stocks)
  - `ccxt` (crypto)
- Indicators:
  - SMA: 20 & 50-day
  - EMA: 20-day
  - RSI: 14-period
  - MACD: 12-26-9 (future extension)

---

## Limitations
- Internet required
- Crypto depends on exchange support in `ccxt`
- Historical only (no live feed)

---

## Troubleshooting
- Check symbols, timeframe, or internet connection
- Run: `pip install ...` for missing modules
- View logs in `market_analyzer.log`

---

## Contributing
Pull requests welcome! Consider adding:
- New indicators
- Web dashboard
- Real-time support

---

## License
MIT License

