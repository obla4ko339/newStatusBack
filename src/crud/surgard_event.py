from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM


from datetime import datetime, timezone

from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from datetime import datetime

async def create_surgard_event(data: SurgardEventCreate):
    # print(f"Creating SurgardEvent with data: {data}")
    try:
        event_data = data.dict() if hasattr(data, "dict") else data

        # Убираем tzinfo, если есть
        if event_data.get("datetime") and isinstance(event_data["datetime"], datetime):
            if event_data["datetime"].tzinfo is not None:
                print("🕓 Удаляю tzinfo у datetime")
                event_data["datetime"] = event_data["datetime"].replace(tzinfo=None)

        async with async_session_maker() as session:
            event = SurgardEventSA(**event_data)
            session.add(event)
            await session.commit()
            await session.refresh(event)

        # print(f"✅ SurgardEvent created with ID: {event.id}")
        return event

    except Exception as e:
        print(f"❌ Error creating SurgardEvent: {e}")
        raise
 

async def get_all_events():
    return await SurgardEvent.all().order_by("-created_at")


async def get_event_by_account(account_number: str):
    return await SurgardEvent.filter(account_number=account_number).all()