import boto3
import click


@click.command()
def role_token():
    session = boto3.Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()

    credential = {
        'access_key': current_credentials.access_key,
        'secret_key': current_credentials.secret_key,
        'token': current_credentials.token
    }

    print(credential)


if __name__ == "__main__":
    role_token()
