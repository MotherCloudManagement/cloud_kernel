import os
import json

'''

Get details of kafka environment

'''


def kafka_broker():
    if os.environ['KAFKA_BROKER'] is not None:
        return os.environ['KAFKA_BROKER']

    # Raising an exception is necessary because apscheduler will attempt
    # to make a connection to the broker, when the zookeeper jobstore is selected
    if not os.file.exists('settings_file.json'):
        print("Kafka Job Store selected, but no broker found!")
        raise ReferenceError("Please ensure a valid settings_file.json is included")

    with open('settings_file.json', 'r') as kafkasettings:
        settings = json.load(kafkasettings)

        kafkasettings.close()

    return (settings['KAFKA_BROKER'], settings['KAFA_CONSUMER'], settings['KAFKA_PRODUCER'])
