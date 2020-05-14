import os
import multiprocessing
from cloud_kernel.utils.system_level import is_kafka_installed


def platform_environment():

    cores = multiprocessing.cpu_count()
    kafka_installed = is_kafka_installed()

    return (cores, kafka_installed)
