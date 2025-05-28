import yfinance as yf
import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import argparse
import logging
import sys
import os
from datetime import datetime, timedelta
import warnings
from typing import Tuple, Optional, Dict
from mplfinance.original_flavor import candlestick_ohlc

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('market_analyzer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MarketTrendAnalyzer:
    """Class to analyze market trends for stocks or cryptocurrencies."""
    
    def __init__(self, symbol: str, market_type: str = 'stock', timeframe: str = '1d'):
        """
        Initialize the analyzer with symbol and market type.
        
        Args:
            symbol (str): Trading symbol (e.g., 'AAPL' for stock, 'BTC/USDT' for crypto)
            market_type (str): 'stock' or 'crypto'
            timeframe (str): Data timeframe (e.g., '1d', '1h')
        """
        self.symbol = symbol
        self.market_type = market_type.lower()
        self.timeframe = timeframe
        self.data = None
        self.indicators = {}
        self.validate_inputs()

    def validate_inputs(self) -> None:
        """Validate input parameters."""
        valid_market_types = ['stock', 'crypto']
        if self.market_type not in valid_market_types:
            logger.error(f"Invalid market type. Choose from {valid_market_types}")
            raise ValueError(f"Invalid market type: {self.market_type}")
        
        if not self.symbol:
            logger.error("Symbol cannot be empty")
            raise ValueError("Symbol cannot be empty")

    def fetch_data(self, start_date: str, end_date: str) -> None:
        """Fetch historical market data."""
        try:
            logger.info(f"Fetching data for {self.symbol} from {start_date} to {end_date}")
            
            if self.market_type == 'stock':
                ticker = yf.Ticker(self.symbol)
                self.data = ticker.history(start=start_date, end=end_date, interval=self.timeframe)
                if self.data.empty:
                    logger.error("No data retrieved from yfinance")
                    raise ValueError("No data retrieved for the given symbol and date range")
                
                # Standardize column names
                self.data = self.data[['Open', 'High', 'Low', 'Close', 'Volume']]
                self.data.reset_index(inplace=True)
                self.data['Date'] = pd.to_datetime(self.data['Date'])
            
            elif self.market_type == 'crypto':
                exchange = ccxt.binance()
                symbol = self.symbol.replace('/', '')  # e.g., 'BTC/USDT' -> 'BTCUSDT'
                timeframe_map = {'1h': '1h', '1d': '1d', '1w': '1w'}
                if self.timeframe not in timeframe_map:
                    logger.error(f"Unsupported timeframe: {self.timeframe}")
                    raise ValueError(f"Unsupported timeframe: {self.timeframe}")
                
                start_ts = int(pd.to_datetime(start_date).timestamp() * 1000)
                end_ts = int(pd.to_datetime(end_date).timestamp() * 1000)
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe_map[self.timeframe], since=start_ts)
                
                self.data = pd.DataFrame(
                    ohlcv,
                    columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                )
                self.data['Date'] = pd.to_datetime(self.data['Date'], unit='ms')
                self.data = self.data[self.data['Date'] <= pd.to_datetime(end_date)]
            
            logger.info(f"Data fetched successfully: {len(self.data)} rows")
        
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise

    def calculate_sma(self, window: int = 20) -> pd.Series:
        """Calculate Simple Moving Average."""
        try:
            sma = self.data['Close'].rolling(window=window).mean()
            self.indicators[f'SMA_{window}'] = sma
            logger.info(f"Calculated SMA with window {window}")
            return sma
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            raise

    def calculate_ema(self, window: int = 20) -> pd.Series:
        """Calculate Exponential Moving Average."""
        try:
            ema = self.data['Close'].ewm(span=window, adjust=False).mean()
            self.indicators[f'EMA_{window}'] = ema
            logger.info(f"Calculated EMA with window {window}")
            return ema
        except Exception as e:
            logger.error(f"Error calculating EMA: {str(e)}")
            raise

    def calculate_rsi(self, periods: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        try:
            delta = self.data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            self.indicators['RSI'] = rsi
            logger.info(f"Calculated RSI with periods {periods}")
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            raise

    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD and Signal Line."""
        try:
            ema_fast = self.data['Close'].ewm(span=fast, adjust=False).mean()
            ema_slow = self.data['Close'].ewm(span=slow, adjust=False).mean()
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal, adjust=False).mean()
            histogram = macd - signal_line
            self.indicators['MACD'] = macd
            self.indicators['Signal'] = signal_line
            self.indicators['Histogram'] = histogram
            logger.info("Calculated MACD")
            return macd, signal_line, histogram
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            raise

    def detect_trend(self) -> pd.Series:
        """Detect market trend based on moving averages and RSI."""
        try:
            sma_short = self.calculate_sma(window=20)
            sma_long = self.calculate_sma(window=50)
            rsi = self.calculate_rsi()
            
            trend = pd.Series('Neutral', index=self.data.index)
            for i in range(len(self.data)):
                if (sma_short.iloc[i] > sma_long.iloc[i]) and (rsi.iloc[i] > 50):
                    trend.iloc[i] = 'Bullish'
                elif (sma_short.iloc[i] < sma_long.iloc[i]) and (rsi.iloc[i] < 50):
                    trend.iloc[i] = 'Bearish'
            
            self.indicators['Trend'] = trend
            logger.info("Detected market trends")
            return trend
        except Exception as e:
            logger.error(f"Error detecting trend: {str(e)}")
            raise

    def save_analysis(self, output_file: str = 'market_analysis.csv') -> None:
        """Save analysis results to a CSV file."""
        try:
            analysis_df = self.data.copy()
            for indicator, values in self.indicators.items():
                analysis_df[indicator] = values
            
            analysis_df.to_csv(output_file, index=False)
            logger.info(f"Analysis saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving analysis: {str(e)}")
            raise

    def plot_candlestick(self, output_file: str = 'market_trend.png') -> None:
        """Plot candlestick chart with indicators."""
        try:
            # Prepare data for candlestick
            plot_data = self.data[['Date', 'Open', 'High', 'Low', 'Close']].copy()
            plot_data['Date'] = plot_data['Date'].map(mdates.date2num)
            
            # Create figure with subplots
            fig = plt.figure(figsize=(15, 10))
            gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 1])
            
            # Candlestick plot
            ax1 = fig.add_subplot(gs[0])
            candlestick_ohlc(ax1, plot_data[['Date', 'Open', 'High', 'Low', 'Close']].values,
                           width=0.4, colorup='g', colordown='r')
            
            # Plot moving averages
            ax1.plot(self.data['Date'], self.indicators.get('SMA_20', []), label='SMA 20', color='blue')
            ax1.plot(self.data['Date'], self.indicators.get('SMA_50', []), label='SMA 50', color='orange')
            
            ax1.set_title(f'{self.symbol} Price Chart')
            ax1.set_ylabel('Price')
            ax1.legend()
            ax1.xaxis_date()
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(ax1.get_xticklabels(), rotation=45)
            
            # RSI plot
            ax2 = fig.add_subplot(gs[1], sharex=ax1)
            ax2.plot(self.data['Date'], self.indicators.get('RSI', []), label='RSI', color='purple')
            ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
            ax2.axhline(30, linestyle='--', alpha=0.5, color='green')
            ax2.set_ylabel('RSI')
            ax2.legend()
            
            # MACD plot
            ax3 = fig.add_subplot(gs[2], sharex=ax1)
            ax3.plot(self.data['Date'], self.indicators.get('MACD', []), label='MACD', color='blue')
            ax3.plot(self.data['Date'], self.indicators.get('Signal', []), label='Signal', color='orange')
            ax3.bar(self.data['Date'], self.indicators.get('Histogram', []), label='Histogram', color='gray', alpha=0.5)
            ax3.set_ylabel('MACD')
            ax3.legend()
            
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            logger.info(f"Chart saved to {output_file}")
        except Exception as e:
            logger.error(f"Error plotting chart: {str(e)}")
            raise

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Market Trend Analyzer")
    parser.add_argument('--symbol', type=str, required=True, help='Market symbol (e.g., AAPL, BTC/USDT)')
    parser.add_argument('--market', type=str, default='stock', choices=['stock', 'crypto'],
                        help='Market type: stock or crypto')
    parser.add_argument('--timeframe', type=str, default='1d', help='Data timeframe (e.g., 1d, 1h)')
    parser.add_argument('--start-date', type=str, default=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                        help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                        help='End date (YYYY-MM-DD)')
    parser.add_argument('--output-csv', type=str, default='market_analysis.csv',
                        help='Output CSV file path')
    parser.add_argument('--output-plot', type=str, default='market_trend.png',
                        help='Output plot file path')
    return parser.parse_args()

def main():
    """Main function to run the market trend analyzer."""
    try:
        args = parse_arguments()
        logger.info(f"Starting analysis for {args.symbol} ({args.market})")
        
        # Initialize analyzer
        analyzer = MarketTrendAnalyzer(
            symbol=args.symbol,
            market_type=args.market,
            timeframe=args.timeframe
        )
        
        # Fetch data
        analyzer.fetch_data(args.start_date, args.end_date)
        
        # Calculate indicators
        analyzer.calculate_sma(window=20)
        analyzer.calculate_sma(window=50)
        analyzer.calculate_ema(window=20)
        analyzer.calculate_rsi()
        analyzer.calculate_macd()
        analyzer.detect_trend()
        
        # Save and visualize results
        analyzer.save_analysis(args.output_csv)
        analyzer.plot_candlestick(args.output_plot)
        
        logger.info("Analysis completed successfully")
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()