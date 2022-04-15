from typing import List
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient, producer
from kafka.admin import NewTopic
from .kafka_models import KafkaModel
from src.config.env import environment
import json

class CoreKafka:

    def __init__(self):
        self._bootstrap_servers = environment.get_item("KAFKA_BOOTSTRAP_SERVER", None)
        self._kafka_admin = KafkaAdminClient(bootstrap_servers=self._bootstrap_servers)
        self._partitions = int(environment.get_item("KAFKA_TOPIC_PARTITIONS", "4"))
        self._replication_factor = int(environment.get_item("KAFKA_TOPIC_REPLICATION_FACTOR", "1"))
        self._group_id = environment.get_item("KAFKA_GROUP_ID", False)
        
        self._topic_client_qrcode = environment.get_item("KAFKA_TOPIC_CLIENT_QRCODE", "SetupClientQrcode")
        self._topic_login = environment.get_item("KAFKA_TOPIC_LOGIN", "SetupLogin")

    
    def get_client_topic(self):
        return self._topic_login
    
    def get_client_qrcode_topic(self):
        return self._topic_client_qrcode

    def create_topic_client_qrcode(self) -> bool:
        if self._topic_client_qrcode in self.list_topics():
            return True

        max_replication_factor = len(self.list_brokers())

        rep_factor = self._replication_factor

        if self._replication_factor > max_replication_factor:
            rep_factor = max_replication_factor

        topic = NewTopic(self._topic_client_qrcode, self._partitions, rep_factor)

        create_topic_response = self._kafka_admin.create_topics([topic])
        return create_topic_response.topic_errors[0][1] == 0

    def consumer(self, topic, mode='latest') -> KafkaConsumer:
        consumer = KafkaConsumer(
            bootstrap_servers=self._bootstrap_servers, 
            group_id= self._group_id,
            auto_offset_reset=mode,
            value_deserializer=lambda v: KafkaModel(**json.loads(v))
            # value_deserializer=lambda v: v
        )
        consumer.subscribe(topic)
        return consumer

    def producer(self) -> KafkaProducer:

        producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_servers, 
            value_serializer=lambda v: v.to_json.encode('utf-8')
        )

        return producer

    def publish(self, topic:str, kafka_model:KafkaModel) -> bool:
        producer = self.producer()
        producer.send(topic, kafka_model, bytes(kafka_model.header.id.encode('utf-8')))
        return True

    def list_topics(self) -> List:
        return self._kafka_admin.list_topics()

    def list_brokers(self):
        metadata = self._kafka_admin.describe_cluster()
        return metadata['brokers']