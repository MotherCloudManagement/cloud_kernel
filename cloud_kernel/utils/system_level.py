import os


# Apache Kafka Paths to check for installation
extended_path = [
    "/sbin",
    "/bin",
    "/usr/sbin",
    "/usr/bin",
    "/usr/local/sbin",
    "/usr/local/bin",
]


def is_kafka_installed():
    for path in extended_path:
        if os.path.exists('kafka-server-start.sh'):
            return True
        return False
