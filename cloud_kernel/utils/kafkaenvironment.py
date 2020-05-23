import os
import json

'''

Get details of kafka environment

'''


def kafka_broker():

    # Raising an exception is necessary because apscheduler will attempt
    # to make a connection to the broker, when the zookeeper jobstore is selected
    settings = None
    if os.path.exists('settings_file.json'):
        print("Kafka Job Store selected, Located Settings File")

        with open('settings_file.json', 'r') as kafkasettings:
            try:
                settings = json.load(kafkasettings)
            except PermissionError:
                settings = None

            kafkasettings.close()

    final_configuration = {'KAFKA_BROKER': 'localhost:1234', 'KAFKA_CONSUMER': 'topic_main',
                           'KAFKA_PRODUCER': 'producer_main', 'KAFKA_GROUP': 'main_group'}
    if settings is not None:
        final_configuration = settings

    return (final_configuration['KAFKA_BROKER'], final_configuration['KAFKA_CONSUMER'],
            final_configuration['KAFKA_PRODUCER'], final_configuration['KAFKA_GROUP'])
