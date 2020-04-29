import logging

from {{ cookiecutter.project_slug }} import celery

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
