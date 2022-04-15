from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from src.config.containers import Container
from src.config.env import environment
from src.domain.users.models.user_model import RequestUserModel
from src.domain.users.services.user_service import UserService
from src.shared.services.lib.kafka.kafka_models import KafkaHeader, KafkaModel
from src.shared.services.lib.kafka.kafka_service import CoreKafka

# Entrypoint /user/
router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not found'}},
)

class HealthModel(BaseModel):
    status: str
    time: datetime



html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Qrcode Cashbot</h1>
        <button onclick="loginWP()">Iniciar robô</button>
        <canvas id="qr"></canvas>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                console.log("uma coisa aqui", event.data)
                if (event.data != ""){
                    var qr = new QRious({
                        element: document.getElementById("qr"),
                        value: event.data,
                        size:200
                    });
                }
            };
            function loginWP() {
                var count = 0
                var intervalId = null
                ws.send('{"action": "login"}')
                intervalId = setInterval(function () {
                    ws.send('{"action": "qrcode"}')
                    count += 1
                    if (count == 12){
                        clearInterval(intervalId);
                    }
                }, 10000);
            }
        </script>
    </body>
</html>
"""


@router.get("/front")
async def get():
    return HTMLResponse(html)

@router.get('', response_model=HealthModel)
def health():
    return HealthModel(status="ok", time=datetime.now())

container = Container()

@router.websocket_route('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data["action"] == "login":
            print("recebeu info")
            kafka_service = CoreKafka()
            kafka_header_model = KafkaHeader(
                id = "4",
                label_code = "3",
                application = "seila",
                type = "kkj"
            )
            kafka_model = KafkaModel(header=kafka_header_model,payload={"user_id": "1"})
            kafka_service.publish(environment.get_item("KAFKA_TOPIC_LOGIN", "SetupLogin"),kafka_model)
        
        if data["action"] == "qrcode":
            service : UserService  = container.user_container.user_service()
            request_model = RequestUserModel(id = 1)
            user_model = service.find(request_model)
            print("qrcode requisitadooo")
            print(user_model)
            await websocket.send_text(user_model.qrcode.qrcode)