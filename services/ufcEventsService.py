from entities.ufcEvent import UfcEvent
from repositories.serviceBusQueueRepo import ServiceBusQueueRepo
from repositories.webScrapperRepo import WebScrapperRepo

class UfcEventsService:
    webScrapperRepo: WebScrapperRepo
    serviceBusQueueRepo: ServiceBusQueueRepo

    def __init__(self, webScrapperRepo: WebScrapperRepo, serviceBusQueueRepo: ServiceBusQueueRepo):
        self.webScrapperRepo = webScrapperRepo
        self.serviceBusQueueRepo = serviceBusQueueRepo

    async def sendUfcEvents(self)-> None:
        events: list[UfcEvent] = self.webScrapperRepo.getUfcEvents()
        await self.serviceBusQueueRepo.send(events)
