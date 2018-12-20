from .base import *

PRODUCTION_JSON = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

ALLOWED_HOSTS = [
    '.elasticbeanstalk.com',
    '.ashe.kr',
]

# FOR AMAZONSETTINGS
DEFAULT_FILE_STORAGE = 'config.storages.MediaClass'
AWS_ACCESS_KEY_ID = SECRET_JSON['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRET_JSON['AWS_SECRET_ACCESS_KEY']
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-northeast-2'

WSGI_APPLICATION = 'config.wsgi.production.application'


# CORS ALLOW WHITELIST
CORS_ORIGIN_WHITELIST = (
    'ashe.kr',
    'ashe.kr.s3-website.ap-northeast-2.amazonaws.com',
)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = PRODUCTION_JSON['DATABASES']

AWS_STORAGE_BUCKET_NAME = PRODUCTION_JSON['AWS_STORAGE_BUCKET_NAME']

LOG_DIR = os.path.join(ROOT_DIR, '.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s',
        }
    },
    'handlers': {
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'default',
            # 최대 1MB를 넘게되면 새 파일을 만들어 저장
            'maxBytes': 1048576,
            # 최대 파일은 10개
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_error', 'console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}


def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)