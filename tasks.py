import os
import time
import celery
from celery import group, chord
from celery.utils.log import get_task_logger


app = celery.Celery(
    __name__,
    broker="amqp://{user}:{password}@{host}".format(
        user="guest", password="guest", host=os.getenv("RABBIT", "localhost"), vhost=""
    ),
    backend="db+postgresql+psycopg2://{user}:{password}@{host}/{database}".format(
        user="postgres",
        password="postgres",
        host=os.getenv("PGHOST", "localhost"),
        database="postgres",
    ),
)

logger = get_task_logger(__name__)


@app.task()
def gen(n):
    """ Expensive generator function """
    time.sleep(10)
    return list(range(n))


@app.task()
def multiply(x):
    """ Function used by the mapper """
    return x * x


@app.task()
def reducer(numbers):
    """ Simple reduce function """
    time.sleep(10)
    return sum(numbers)


@app.task()
def map_reduce(n):
    """ Takes input that dynamically produces a generator that in turn, produce
    input to a map-reduce job """

    numbers = gen.s(n)
    my_chord = chord(group(multiply.s(n) for n in numbers()), reducer.s())
    result = my_chord()

    return result
