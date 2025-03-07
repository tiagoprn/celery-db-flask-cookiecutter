import logging
import string
from random import SystemRandom, randint

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task()
def compute(random_number: int, now_timestamp: str) -> None:
    logger.info(
        f'Received random_number={random_number}, '
        f'now_timestamp={now_timestamp}....'
    )
    random_number *= 2
    logger.info(
        f'Computation finished. random_number is now: {random_number}.'
    )


@shared_task()
def generate_random_string() -> None:
    logger.info('Generating random string...')
    random_string = ''.join(SystemRandom().choice(string.ascii_uppercase +
        string.ascii_lowercase + string.digits) for _ in
        range(randint(10, 20)))
    logger.info(f'Random string successfully generated: {random_string}')
