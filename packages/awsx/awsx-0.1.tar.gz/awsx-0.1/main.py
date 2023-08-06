import boto3
import click


@click.command()
def role_token():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()

    print(current_credentials.access_key)
    print(current_credentials.secret_key)
    print(current_credentials.token)
