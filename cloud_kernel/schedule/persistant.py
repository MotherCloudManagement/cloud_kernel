from kafka import KafkaProducer, KafkaClient, KafkaConsumer
from kafka.errors import KafkaError, KafkaConnectionError, KafkaTimeoutError
from cloud_kernel.utils.kafkaenvironment import kafka_broker
from collections.abc import Mapping
import ast


class CloudKafkaBase(object):

    def __init__(self):
        """
        This class will manage all Apache Kafka related functions.  If there is an issue with
        queueing or reading data from an existing queue, or any difficulty surfaces that could
        lead to degraded performance, this class should send instructions to pause jobs and later
        resume them.

        """
        self.message_tracker = ''
        self.broker_server, self.consumer_topic, self.producer_topic, self.consumergroup = kafka_broker()
        self.consumer = KafkaConsumer(
            self.consumer_topic,
            group_id=self.consumergroup,
            bootstrap_servers=[self.broker_server]
        )
        self.c = KafkaConsumer()
        self.producer = ''
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[self.broker_server],
                retries=5
            )
        except Exception:
            raise ReferenceError('Unable to properly load settings of Kafka Broker, Consumer, or Producer')


class CloudKafkaContainer(CloudKafkaBase):

    def __call__(cls, *args, **kwargs):
        pass

    def __init__(self):
        super(CloudKafkaContainer, self).__init__()


class CloudKafkaProduce(CloudKafkaContainer):

    """
    The reason for specificity here is that the various cloud proivders and local onpremise platforms
    may return 'data' with different formats.

    JSON can be quite tricky, so it's best to handle it properly here and store it in a queue using a
    standard format.

    """
    def __init__(self):
        super(CloudKafkaProduce, self).__init__()

    def ProduceMessage(self, topic, data):
        # Reformatt the data to create a valid Mapping
        if not isinstance(data, Mapping) and isinstance(data, str):
            try:
                data_reformatted = ast.literal_eval(data)
            except Exception:
                print('Unable to properly format data, please ensure valid json has been submitted.')
                return

        while self.producer.bootstrap_connected():

            for key, value in data_reformatted.iteritems():
                self.message_tracker = self.producer.send(
                    topic, {key: value}
                ).add_callback(
                    self.ProduceSuccess, key
                ).add_errback(
                    self.ProduceFailure, pair={key, value}
                )

                self.producer.flush()

                try:
                    self.message_tracker.future.get(timeout=10)
                except KafkaError:
                    print("Not sure what to do yet with"+\
                          " Failed Messages.  For now, just print!")
                    self.ProduceFailure(topic, key)

                self.ProduceSuccess(topic, key)

            print('Producer disconnected from Broker, This may not be a problem! ')
            print('The connections are designed to be short-lived!')

    def ProduceSuccess(self, topic, key):
        print('Successfully Produced Topic: {}'.format(topic))
        print('Successfully Produced Key: {}'.format(key))

    def ProduceFailure(self, topic, key):
        print('Failed to Produce topic {} to Broker'.format(topic))
        print('Failed part'.format(key))


class CloudKafkaConsume(CloudKafkaContainer):

    def __init__(self):
        super(CloudKafkaConsume, self).__init__()

