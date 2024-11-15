
# Financial Analytics System (FAS)

Welcome to the Financial Analytics System, a project designed to provide in-depth insights into financial markets, with a particular focus on forex markets. Initially, this project was built as an **Integrated Financial Analytics System (IFAS)**, leveraging AWS for data management and automation. As the project evolved, it transitioned to free cloud resources while retaining its analytical depth and functionality.

## Project Overview

This project blends quantitative financial analysis, machine learning, and data science techniques to predict forex market trends and deliver actionable insights, focusing on the EURUSD currency pair and exploring correlations with macroeconomic indicators.

## Project History: AWS Integration and Transition

Initially, the project utilised AWS RDS, EC2, and Lambda for data automation and management. As AWS free tier limits were reached, we migrated to **Neon** for cost-effective database management without sacrificing key features. Here’s a summary of AWS integration efforts:

1. **AWS RDS for PostgreSQL**: Configured a PostgreSQL instance to store forex data and analysis results securely.
2. **OpenVPN on AWS EC2**: Set up a secure OpenVPN server on EC2 for remote access to the RDS instance, managing TLS certificates, and firewall rules.
3. **AWS Lambda for Automated Data Fetching**: Developed a Lambda function to automate weekly EURUSD data fetches, though integration challenges with `psycopg2` led to a transition away from Lambda.

## Transition to Free Cloud Database Solution

To keep the project cost-effective, it transitioned to **Neon**, a free cloud-based PostgreSQL alternative, for efficient data storage and management without ongoing AWS costs. Automated data fetching will be replaced with a **refresh button** in the Dash app for user-controlled updates.

## Project Management and Workflow

- **Jira Integration**: This project uses **Jira** to manage tasks and track project progress. Tickets are created for each feature or bug fix, and branches, commits, and pull requests are managed directly through Jira’s integration with GitHub. This setup follows Agile practices, ensuring each project stage is well-documented, traceable, and efficient.
- **GitHub Integration**: With GitHub linked to Jira, each ticket is associated with specific GitHub branches, enabling seamless tracking of code changes related to Jira tasks.

## Project Structure

- `/database`: Database connection and schema for creating tables.
- `/docs`: Documentation and additional resources.
- `/scripts`: Scripts for data collection, processing, and model evaluation.

## Key Features (Planned)

1. **Time Series Analysis**: Forecasting forex rates with ARIMA and LSTM models.
2. **Sentiment Analysis**: Integrating sentiment from financial news.
3. **Economic Indicator Analysis**: Assessing impacts of key economic indicators.
4. **Data Visualisation**: Interactive dashboards for real-time analysis.

## Documentation

For details on AWS setup and configuration (historical):
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

To set up and run the Financial Analytics System, follow these steps:

1. **Step 1: Database Table Setup**
   - Run `migrate.py` to create the necessary tables in your PostgreSQL database. This step ensures all required tables are created before data insertion and analysis.
   ```bash
   python scripts/database/migrate.py
   ```

2. **Step 2: Data Fetching and Moving Average Calculation**
   - Run `fetch_insert_moving_avg.py` to:
     - Fetch the latest EURUSD data from the OANDA API.
     - Insert the raw data into the `currency_data` table.
     - Calculate both short-term (5-day) and long-term (50-day) moving averages.
     - Insert the calculated moving averages into the `moving_average` table.
   ```bash
   python scripts/fetch_insert_moving_avg.py
   ```

3. **Step 3: LSTM Model Training and Evaluation**
   - Run `train_and_evaluate.py` under `time_series_forecasting/` to train the LSTM model on the EURUSD data, evaluate its performance, and calculate key metrics like RMSE and MAE.
   - This script will use the data in the database, train the LSTM model, and output evaluation metrics for further analysis.
   ```bash
   python scripts/time_series_forecasting/d_train_and_evaluate.py
   ```

Following these steps will allow you to fully initialise the system, populate the database with historical forex data, calculate essential analytics, and train a time-series forecasting model.

## Data Pipeline: Fetching Forex Data and Calculating Moving Averages

### Steps in Data Pipeline

1. **Fetching EURUSD Data from OANDA API**
   - **Description**: `fetch_ohlc_data` connects to the OANDA API to retrieve daily OHLC (Open, High, Low, Close) data for EURUSD.
   - **Usage**: Fetches the latest data and integrates it with the historical dataset.

2. **Inserting Raw Data into Database**
   - **Table**: `currency_data`
   - **Process**: Inserts records into the `currency_data` table, capturing open, high, low, close, and volume data.

3. **Calculating Moving Averages**
   - **Description**: Calculates short-term (5-day) and long-term (50-day) moving averages, storing results in the `moving_average` table.

## LSTM Model for Time Series Forecasting

### Model Training and Evaluation

- **Description**: An LSTM model was trained to forecast EURUSD closing prices.
- **Evaluation Metrics**:
  - **RMSE** (Root Mean Squared Error)
  - **MAE** (Mean Absolute Error)

### Visualisation of Training Progress

The model’s training and validation loss curves provide insights into convergence and generalisation.

## Results

The LSTM model achieved promising accuracy with the following metrics:
- **RMSE**: 0.0111
- **MAE**: 0.0091

## Future Enhancements

- **Advanced Threshold and Hyperparameter Tuning**: For the Logistic Regression and LSTM models.
- **Distributed Machine Learning**: Extend to PySpark MLlib for training at scale.
- **Dashboard Visualisation**: A Tableau dashboard to visualise advanced analytics and insights.
- **A/B Testing**: Framework for real-world model performance testing.

## License

This project is licensed under the MIT License. For more details, see the [MIT License](https://opensource.org/licenses/MIT).