import logging
import os
import random
import string

from {{cookiecutter.project_slug}} import celery

logger = logging.getLogger(__name__)


@celery.task()
def compute(random_number: int, now_timestamp: str) -> None:
    logger.info(
        f'Received random_number={random_number}, '
        f'now_timestamp={now_timestamp}....'
    )
    random_number *= 2
    logger.info(
        f'Computation finished. random_number is now: {random_number}.'
    )

@celery.task()
def generate_random_string() -> None:
    logger.info('Generating random string...')
    random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
        string.ascii_lowercase + string.digits) for _ in
        range(random.randint(10, 20)))
    logger.info(f'Random string successfully generated: {random_string}')
