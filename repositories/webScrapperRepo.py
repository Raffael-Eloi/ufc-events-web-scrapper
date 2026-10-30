from datetime import datetime, timezone
import re

import httpx
from bs4 import BeautifulSoup, Tag

from entities.ufcEvent import UfcEvent
from enums.ufcEventType import UfcEventType

class WebScrapperRepo:
    url = "https://www.ufc.com/events"

    def getUfcEvents(self)-> list[UfcEvent]:
        response = httpx.get(
            self.url,
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        upcomingList = soup.select_one("#events-list-upcoming")
        if upcomingList is None:
            return []

        return [
            self._toUfcEvent(card)
            for card in upcomingList.select("article.c-card-event--result")
        ]

    def _toUfcEvent(self, card: Tag)-> UfcEvent:
        link = card.select_one(".c-card-event--result__headline a")
        href = link["href"]
        dateInfo = card.select_one(".c-card-event--result__date")
        numberMatch = re.search(r"/event/ufc-(\d+)$", href)

        ufcEvent = UfcEvent()
        ufcEvent.name = link.get_text(strip=True)
        ufcEvent.type = UfcEventType.NumberedEvent if numberMatch else UfcEventType.FightNight
        ufcEvent.number = int(numberMatch.group(1)) if numberMatch else None
        ufcEvent.mainCardStartTime = self._toDatetime(dateInfo["data-main-card-timestamp"])
        ufcEvent.preliminaryCardStartTime = self._toDatetime(dateInfo["data-prelims-card-timestamp"])
        ufcEvent.date = ufcEvent.mainCardStartTime.date()
        ufcEvent.arena = card.select_one(".c-card-event--result__location h5").get_text(strip=True)
        ufcEvent.city = card.select_one(".c-card-event--result__location .locality").get_text(strip=True)
        ufcEvent.country = card.select_one(".c-card-event--result__location .country").get_text(strip=True)
        return ufcEvent

    def _toDatetime(self, timestamp: str)-> datetime:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
