import boto3
from pydantic import BaseModel, ConfigDict


class Conf(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    AWS_ASSUME_ROLE: bool = False
    AWS_REGION: str = None
    AWS_PROFILE_NAME: str = None
    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    session: boto3.Session = None


def get_aws_conf(assume_role=None,
                 region=None,
                 profile_name=None,
                 access_key_id=None,
                 secret_access_key=None):
    aws_conf = Conf()
    if assume_role is not None:
        aws_conf.AWS_ASSUME_ROLE = assume_role
    if region is not None:
        aws_conf.AWS_REGION = region
    if profile_name is not None:
        aws_conf.AWS_PROFILE_NAME = profile_name
    if access_key_id is not None:
        aws_conf.AWS_ACCESS_KEY_ID = access_key_id
    if secret_access_key is not None:
        aws_conf.AWS_SECRET_ACCESS_KEY = secret_access_key
    return aws_conf


def setup_aws_conf(assume_role=None,
                   region=None,
                   profile_name=None,
                   access_key_id=None,
                   secret_access_key=None):
    if assume_role is not None:
        conf.AWS_ASSUME_ROLE = assume_role
    if region is not None:
        conf.AWS_REGION = region
    if profile_name is not None:
        conf.AWS_PROFILE_NAME = profile_name
    if access_key_id is not None:
        conf.AWS_ACCESS_KEY_ID = access_key_id
    if secret_access_key is not None:
        conf.AWS_SECRET_ACCESS_KEY = secret_access_key


def get_aws_session(aws_conf=None) -> boto3.Session:
    aws_conf = conf if aws_conf is None else aws_conf
    if aws_conf.AWS_ASSUME_ROLE:
        session_root_account = boto3.client('sts',
                                            aws_access_key_id=aws_conf.AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=aws_conf.AWS_SECRET_ACCESS_KEY)
        assume_role_response = session_root_account.assume_role(
            RoleArn=aws_conf.AWS_ASSUME_ROLE,
            RoleSessionName='AssumeRoleSession')['Credentials']

        session = boto3.Session(aws_access_key_id=assume_role_response['AccessKeyId'],
                                aws_secret_access_key=assume_role_response['SecretAccessKey'],
                                aws_session_token=assume_role_response['SessionToken'],
                                region_name=aws_conf.AWS_REGION)
    elif aws_conf.AWS_PROFILE_NAME:
        session = boto3.Session(profile_name=aws_conf.AWS_PROFILE_NAME, region_name=aws_conf.AWS_REGION)
    else:
        session = boto3.Session(
            aws_access_key_id=aws_conf.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=aws_conf.AWS_SECRET_ACCESS_KEY,
            region_name=aws_conf.AWS_REGION)
    return session


conf = Conf()


def get_conf():
    return conf


def aws_get_service(service_name, aws_conf=None):
    session = get_aws_session(conf if aws_conf is None else aws_conf)
    return session.client(service_name)
