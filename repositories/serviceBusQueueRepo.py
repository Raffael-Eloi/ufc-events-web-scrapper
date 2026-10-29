from entities.ufcEvent import UfcEvent
from azure.servicebus.aio import ServiceBusClient 
from azure.servicebus import ServiceBusMessage
import json

class ServiceBusQueueRepo:
    serviceBusClient: ServiceBusClient
    queueName: str

    def __init__(self, serviceBusClient: ServiceBusClient, queueName: str):
        self.serviceBusClient = serviceBusClient
        self.queueName = queueName

    async def send(self, ufcEvents: list[UfcEvent])-> None:
        message: str = self.transformToJson(ufcEvents)
        serviceBusMessage = ServiceBusMessage(message)

        async with self.serviceBusClient.get_queue_sender(self.queueName) as sender:
            await sender.send_messages(serviceBusMessage)

    def transformToJson(self, ufcEvents: list[UfcEvent]) -> str:
        return json.dumps(
            [
                {
                    **vars(event),
                    "type": event.type.name,
                    "date": event.date.isoformat(),
                    "preliminaryCardStartTime": event.preliminaryCardStartTime.isoformat(),
                    "mainCardStartTime": event.mainCardStartTime.isoformat(),
                }
                for event in ufcEvents
            ]
        )