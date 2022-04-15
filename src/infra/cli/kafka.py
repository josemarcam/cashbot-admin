import typer
from src.config.containers import Container
from src.domain.users.models.user_model import KafkaUpdateQrcodeModel, RequestUserModel
from src.domain.users.services.user_service import UserService
from src.infra.orm.factories.user import UserFactory
from src.shared.services.lib.kafka.kafka_service import CoreKafka
app = typer.Typer()

container = Container()

@app.command()
def consume_kafka():
    kafka_service = CoreKafka()
    consumer = kafka_service.consumer(kafka_service.get_client_qrcode_topic(), mode='earliest')
    consumer.subscribe(kafka_service.get_client_qrcode_topic())
    print(f"Consumindo {kafka_service.get_client_qrcode_topic()}")
    for msg in consumer:
        # print(msg.value)
        payload_model = KafkaUpdateQrcodeModel(**msg.value.payload)
        service : UserService  = container.user_container.user_service()
        request_model = RequestUserModel(id = payload_model.user_id)
        user_model = service.find(request_model)
        print(f"usuario ANTIGO \n {user_model} \n")
        user_updated_model = service.update_qrcode(user_model.id,payload_model.qrcode)
        print(f"usuario NOVO \n {user_updated_model} \n")

@app.command()
def test_serv():
    print(UserFactory().__dict__)