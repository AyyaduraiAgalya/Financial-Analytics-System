
# Advanced Financial Analytics System

Welcome to the Advanced Financial Analytics System, designed to provide deep insights into financial markets, with a particular focus on forex markets. This project leverages historical data and economic indicators to forecast movements in forex rates, especially the EURUSD pair, and integrates financial news sentiment to enhance predictions.

## Project Overview

This project aims to blend quantitative financial analysis with machine learning and data science techniques to predict forex market trends and provide actionable insights. The system focuses on the EURUSD currency pair, exploring correlations between macroeconomic indicators and market movements.

## Transition to Free Cloud Database Solution

Originally, this project used Amazon RDS for PostgreSQL, but to minimize costs, it was transitioned to **Neon**, a free cloud-based PostgreSQL alternative. This change ensures accessibility without compromising on features or data integrity.

## Project Structure

- `/database` - Database connection and schema for creating tables.
- `/docs` - Documentation and additional resources.
- `/scripts` - Scripts for data collection, processing, and model evaluation.
  
## Key Features (Planned)

1. **Time Series Analysis**: Forecasting forex rates with ARIMA and LSTM models.
2. **Sentiment Analysis**: Integrating sentiment from financial news.
3. **Economic Indicator Analysis**: Assessing impacts of key economic indicators.
4. **Data Visualisation**: Interactive dashboards for real-time analysis.

These features may evolve as the project progresses.

## Documentation

For additional details on setup and configuration:
- [AWS RDS Setup Guide](docs/AWS-RDS-Setup.md)
- [AWS S3 Setup Guide](docs/AWS-S3-Setup.md)
- [AWS Lambda Data Fetching Documentation](docs/AWS-Lambda-Automate-Data-Fetching.md)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/yourusername/Financial-Analytics-System.git
cd Financial-Analytics-System
```

### Set Up Python Environment

```bash
# Unix/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

1. Create a `.env` file in the project root:
   ```plaintext
   touch .env  # Unix/macOS
   type nul > .env  # Windows
   ```

2. Add the following to the `.env` file:
   ```plaintext
   OANDA_API_KEY=your_actual_api_key_here
   DB_HOST=your_neon_host
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASS=your_db_password
   DB_PORT=5432  # Default for PostgreSQL
   ```

### Running the Application

```bash
python scripts/fetch_insert_moving_avg.py
```

## Data Pipeline: Fetching Forex Data and Calculating Moving Averages

### Steps in Data Pipeline

1. **Fetching EURUSD Data from OANDA API**
   - **Description**: `fetch_ohlc_data` connects to the OANDA API to retrieve daily OHLC (Open, High, Low, Close) data for EURUSD.
   - **Parameters**:
     - `currency_pair`: EURUSD.
     - `count`: Number of historical data points.
     - `from_time`: Fetches data from this timestamp onward, if provided.
   - **Usage**: On the first run, fetches the last 100 days. On subsequent runs, only new data is fetched.

2. **Inserting Raw Data into Database**
   - **Table**: `currency_data`
   - **Process**: `insert_currency_data` function inserts records into the `currency_data` table with a structure that includes currency pair, timestamp, open, high, low, close, and volume.
   - **Schema**:
     ```python
     class CurrencyData(Base):
         id = Column(Integer, primary_key=True)
         currency_pair = Column(String, nullable=False)
         timestamp = Column(DateTime, nullable=False)
         open = Column(Float, nullable=False)
         high = Column(Float, nullable=False)
         low = Column(Float, nullable=False)
         close = Column(Float, nullable=False)
         volume = Column(Float, nullable=False)
     ```

3. **Calculating Moving Averages**
   - **Description**: The `calculate_moving_averages` function calculates both short-term (5-day) and long-term (50-day) moving averages.
   - **Schema**:
     ```python
     class MovingAverage(Base):
         id = Column(Integer, primary_key=True)
         currency_data_id = Column(Integer, ForeignKey('currency_data.id'), nullable=False)
         timestamp = Column(DateTime, nullable=False)
         window_size = Column(Integer, nullable=False)
         moving_average = Column(Float, nullable=False)
     ```

### Data Refresh and Update

**Daily Update**: The script can be configured to run daily, adding the latest EURUSD data and updating moving averages.

**Dash Refresh Button**: A refresh button in the Dash app allows users to update data and moving averages, adding interactivity without automated scheduling.

## Summary

This pipeline handles data retrieval, moving average calculation, and storage in a streamlined, efficient workflow. Data is stored in a PostgreSQL database, making it readily available for visualisation in the Dash app.

## License

This project is licensed under the MIT License. For more details, see the [MIT License](https://opensource.org/licenses/MIT).
