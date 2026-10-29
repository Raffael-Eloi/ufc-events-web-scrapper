import os

import azure.functions as func
from azure.servicebus.aio import ServiceBusClient

from repositories.serviceBusQueueRepo import ServiceBusQueueRepo
from repositories.webScrapperRepo import WebScrapperRepo
from services.ufcEventsService import UfcEventsService

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 8 * * *", arg_name="timer", run_on_startup=False)
async def send_ufc_events(timer: func.TimerRequest) -> None:
    async with ServiceBusClient.from_connection_string(os.environ["SERVICEBUS_CONNECTION_STRING"]) as client:
        queueRepo = ServiceBusQueueRepo(client, os.environ["SERVICEBUS_QUEUE_NAME"])
        service = UfcEventsService(WebScrapperRepo(), queueRepo)
        await service.sendUfcEvents()
