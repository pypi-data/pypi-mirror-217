from kafka import KafkaProducer
from json import dumps as dumps_,loads as loads_
from klp_commons.utils.utils import CustomEncoder

class Producer:
    def __init__(
                self, 
                topic = None,
                kafka_brokers = None,
                acks = None,
                api_version = None,
                client_id = None
                 ):
        self.kafka_api_version = api_version
        self.topic = topic
        self.acks = acks
        self.client_id = client_id
        self.kafka_brokers = kafka_brokers
        
    def init_producer(self) -> None:

        self.producer = KafkaProducer(
            acks = self.acks,
            api_version=self.kafka_api_version,
            bootstrap_servers = self.kafka_brokers,
            value_serializer = lambda x: dumps_(x).encode('utf-8'),
        )

    def send_message(self, data: dict) -> None:
        data_dict = dumps_(data,cls=CustomEncoder)
        data_dict  = loads_(data_dict)
        self.producer.send(self.topic, value=data_dict)
        # block until all async messages are sent
        self.producer.flush()
