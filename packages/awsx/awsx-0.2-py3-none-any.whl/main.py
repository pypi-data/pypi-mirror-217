import boto3
import click


@click.command()
def role_token():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    print(current_credentials)

    credential = {
        'access_key': current_credentials.get('access_key'),
        'secret_key': current_credentials.get('secret_key'),
        'token': current_credentials.get('token')
    }


if __name__ == "__main__":
    role_token()
