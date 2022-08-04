import boto3


def get_parameter_value(parameter):

    ssm = boto3.client("ssm", "us-east-1")
    param = ssm.get_parameter(Name=parameter, WithDecryption=True)
    return param['Parameter']['Value']


