import time
import random

# Sleep random time between [a, b]
def sleep_interval(a, b):
    time.sleep(random.randint(a, b))