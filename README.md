
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
python3.12 -m venv venv
source venv/bin/activate

# Windows
python3.12 -m venv venv
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

3. **Calculating Moving Averages**
   - **Description**: The `calculate_moving_averages` function calculates both short-term (5-day) and long-term (50-day) moving averages.
   - **Table**: `moving_average`

### Data Refresh and Update

**Daily Update**: The script can be configured to run daily, adding the latest EURUSD data and updating moving averages.

**Dash Refresh Button**: A refresh button in the Dash app allows users to update data and moving averages, adding interactivity without automated scheduling.

## LSTM Model for Time Series Forecasting

### Model Training and Evaluation

- **Description**: An LSTM model was trained to forecast EURUSD closing prices.
- **Data Preparation**: Data was prepared by scaling and reshaping to fit the LSTM’s expected input format.
- **Model Architecture**: The LSTM model was structured with layers to capture time-dependent patterns.
- **Evaluation Metrics**:
  - **RMSE** (Root Mean Squared Error): Measures average error magnitude.
  - **MAE** (Mean Absolute Error): Indicates average absolute error.

### Results

The LSTM model demonstrated effective learning with the following metrics:
- **RMSE**: 0.0111
- **MAE**: 0.0091

### Scripts for Model Workflow

1. **Data Preparation**: Prepares data for training.
2. **LSTM Model Definition**: Defines and compiles the LSTM model.
3. **Model Training and Evaluation**: Trains the model, evaluates, and saves it.

### Visualization of Training Progress

The model’s loss over training epochs was plotted, revealing convergence and generalization patterns.

## License

This project is licensed under the MIT License. For more details, see the [MIT License](https://opensource.org/licenses/MIT).
