import os
import multiprocessing
from utils.system_level import which


def platform_environment():

    cores = multiprocessing.cpu_count()
    kafka_installed = is_kafka_installed('kafka')

    return (cores, kafka_installed)
