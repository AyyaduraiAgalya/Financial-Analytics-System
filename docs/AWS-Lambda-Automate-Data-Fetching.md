# Automate Data Fetching with AWS Lambda

## Objectives
- Automate real-time data fetching from the OANDA API using AWS Lambda.
- Store fetched data in AWS RDS (PostgreSQL).

## Setup
- Created a Lambda function to fetch and process data.
- Configured AWS RDS for PostgreSQL.
- Managed secrets with AWS Secrets Manager.

## Challenges and Issues
### psycopg2 Import Error
- **Issue**: Encountered `ModuleNotFoundError: No module named 'psycopg2._psycopg'` error when running the Lambda function.
- **Analysis**: The error is related to the Lambda environment not having the correct precompiled `psycopg2` library.
- **Attempts to Resolve**:
  - Used `aws-psycopg2` package as a drop-in replacement for `psycopg2`.
  - Created a wrapper module to force the use of `aws-psycopg2`.
  - Despite these efforts, the issue persisted.
- **Outcome**: Unable to fully resolve the issue within the constraints of the free tier and time available.

## Reusable Code and Configurations
- Lambda function code for fetching data from the OANDA API.
- Database connection setup using SQLAlchemy.
- Environment variable management using AWS Secrets Manager.

## Transition to Local and Free Resources
- Switching to local PostgreSQL/ElephantSQL for database management.
- Using `cron` jobs or a local scheduler for data fetching.

## Future Use
- The code and configurations can be revisited if transitioning back to AWS services in a larger project with a budget.
- Potentially resolve the `psycopg2` issue with more time and resources.
