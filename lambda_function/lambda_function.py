import boto3
import os
import json
from database.fetch_data import fetch_data
from database.insert_data import insert_currency_data


def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret = response['SecretString']
    return json.loads(secret)


def lambda_handler(event, context):
    secret_name = "fin_analytics_sys"  # Replace with your actual secret name
    secrets = get_secret(secret_name)

    os.environ['OANDA_API_KEY'] = secrets['OANDA_API_KEY']
    os.environ['DB_HOST'] = secrets['DB_HOST']
    os.environ['DB_NAME'] = secrets['DB_NAME']
    os.environ['DB_USER'] = secrets['DB_USER']
    os.environ['DB_PASS'] = secrets['DB_PASS']
    os.environ['DB_PORT'] = secrets['DB_PORT']

    currency_pair = event.get('currency_pair', 'EUR_USD') # 'currency_pair' parameter will be used when this project in future takes an input from the user
    data = fetch_data()
    insert_currency_data(data)

    return {
        'statusCode': 200,
        'body': f'Data fetched and stored successfully for {currency_pair}.'
    }
