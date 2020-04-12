import os
import time
import celery
from celery import group, chord, signals
from celery.utils.log import get_task_logger


app = celery.Celery(
    __name__,
    broker="amqp://guest@{host}".format(host=os.getenv("RABBIT", "localhost")),
    backend="db+postgresql+psycopg2://postgres:postgres@{host}/postgres".format(
        host=os.getenv("PGHOST", "localhost")
    ),
)

logger = get_task_logger(__name__)


@app.task()
def add(x, y):
    logger.info("Entering add")
    time.sleep(0.1)
    return x + y


@app.task()
def mul(x, y):
    logger.info("Entering mul")
    time.sleep(0.1)
    return x * y


@app.task()
def tsum(numbers):
    logger.info("Entering tsum")
    time.sleep(0.1)
    return sum(x for x in numbers)


@app.task()
def gen(n):
    logger.info("Entering gen")
    return range(n)


@app.task()
def process(n, ns=None):
    logger.info("Entering process")
    return n * 2


# gen -> chord(group(f(g) for g in gen), aggregate)


# @signals.task_success.connect()
@signals.task_postrun.connect()
def process_range(**kwargs):
    logger.info("Entering process_range")

    # for k, v in kwargs.items():
    # logger.info(f"-- {k}: {v}")

    # header = group(add.s(n, n) for n in gen.s(kwargs["ns"]))
    # callback = tsum.s()
    # chord(header)(callback)
