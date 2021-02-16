from decouple import config

IS_DEV_APP = config('IS_DEV_APP', cast=bool)  # Queues

QUEUE_HOST = config('RABBITMQ_HOST', cast=str)
QUEUE_PORT = config('RABBITMQ_PORT', cast=int, default=5672)
QUEUE_USER = config('RABBITMQ_USER', cast=str)
QUEUE_PASSWORD = config('RABBITMQ_PASSWORD', cast=str)
DEFAULT_QUEUE_NAME = config('RABBITMQ_DEFAULT_QUEUE', cast=str)
TASKS_QUEUES = {
    '{{ cookiecutter.project_slug }}.tasks.compute': {'queue': 'compute'},
    '{{ cookiecutter.project_slug }}.tasks.generate_random_string': {
        'queue': 'generate_random_string'
    },
}

# Logging configuration
LOG_LEVEL = config('LOG_LEVEL', default='INFO', cast=str)
LOG_VARS = config('LOG_VARS', cast=str).replace("'", '').replace('"', '')
JSON_LOGS = config('JSON_LOGS', default=False, cast=bool)
if JSON_LOGS:
    log_format = ' '.join(
        ['%({0:s})'.format(variable) for variable in LOG_VARS.split()]
    )
else:
    log_format = ''
    for index, variable in enumerate(LOG_VARS.split()):
        if variable != 'asctime':
            log_format += ' '
        log_format += f'%({variable})s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': LOG_LEVEL, 'handlers': ['console']},
    'formatters': {
        'default': {'format': log_format, 'datefmt': '%Y%m%d.%H%M%S'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
            'formatter': 'default',
        }
    },
    'loggers': {
        # default for all undefined Python modules
        '': {'level': 'WARNING', 'handlers': ['console']},
        'rose': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
    },
}
if JSON_LOGS:
    LOGGING['formatters']['default'][
        'class'
    ] = 'pythonjsonlogger.jsonlogger.JsonFormatter'

logging.config.dictConfig(LOGGING)

# database
DATABASE_USER = config('DATABASE_USER')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_HOST = config('DATABASE_HOST')
DATABASE_NAME = config('DATABASE_NAME')
DATABASE_URI = (
    f'postgresql+psycopg2://{DATABASE_USER}'
    f':{DATABASE_PASSWORD}'
    f'@{DATABASE_HOST}'
    f'/{DATABASE_NAME}'
)
SQLALCHEMY_DATABASE_URI = DATABASE_URI
