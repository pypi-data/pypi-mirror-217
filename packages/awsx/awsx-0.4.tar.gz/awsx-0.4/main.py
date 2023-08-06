import boto3
import click


def identity_arn():
    sts_client = boto3.client('sts')

    # 使用 get_caller_identity 获取调用者的身份信息
    response = sts_client.get_caller_identity()

    return {
        'User ID': response.get('UserId'),
        'ARN': response.get('Arn')
    }
    # 打印结果
    # print("Account: ", response['Account'])
    # print("User ID: ", response['UserId'])
    # print("ARN: ", response['Arn'])


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

    print(identity_arn())
    print(credential)


if __name__ == "__main__":
    role_token()
