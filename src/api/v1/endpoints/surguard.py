from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
import re


from src.crud.surgard_event import create_surgard_event
from src.schemas.surgard_event import SurgardEventCreate
from datetime import datetime, timezone

router = APIRouter(prefix="/surguard", tags=["surguard"])


def parse_surgard(message: str):
    """
    Разбор строки формата Sur-Gard Contact ID, например:
    '5011 180003E1410000218:06:19-09/11'
    """

    msg = message.strip().replace('\x14', '').replace('\r', '').replace('\n', '').strip()

    # Обновленный шаблон (учитывает пробел между блоками)
    pattern = re.compile(
        r'(?P<header>\d)'               # тип данных
        r'(?P<line>\d)'                 # номер линии
        r'(?P<receiver>\d{2})\s*'       # приемный канал + возможный пробел
        r'(?P<format>\d{2})'            # идентификатор формата
        r'(?P<account>\d{4})'           # номер прибора
        r'(?P<classifier>[RE])'         # E или R
        r'(?P<event_code>\d{3})'        # код события
        r'(?P<group>\d{2})'             # код группы
        r'(?P<zone>\d{3})'              # номер шлейфа/зоны
        r'(?::?(?P<timestamp>\d{2}:\d{2}:\d{2}-\d{2}/\d{2}))?'  # время (опционально)
    )

    match = pattern.search(msg)
    if not match:
        return {"raw": message, "error": "Не удалось распарсить сообщение"}

    data = match.groupdict()

    ts = data.get("timestamp")
    dt = None
    if ts:
        try:
            dt = datetime.strptime(ts, "%H:%M:%S-%d/%m")
            # Добавляем год БЕЗ часового пояса
            dt = dt.replace(year=datetime.now().year)
            print(f"просто дата {dt}")
        except Exception:
            dt = None

    return {
        "type_code": data["header"],
        "line_number": data["line"],
        "receiver_number": data["receiver"],
        "format_id": data["format"],
        "account_number": data["account"],
        "event_type": "Restore" if data["classifier"] == "R" else "Event",
        "event_code": data["event_code"],
        "group_code": data["group"],
        "zone_or_user": data["zone"],
        "datetime": dt,
        "raw": message,
    }


class SurguardEvent(BaseModel):
    surgard: str

@router.post("/")
async def get_objects(event: SurguardEvent):
    """
    Получить список всех объектов
    """
    print(event)
    try:
        print(f"📨 Получено от listener: {event.surgard}")  # логируем то, что пришло
        parsed = parse_surgard(event.surgard)
        print(f"🔍 Распарсено: {parsed}")  # логируем расп

        obj = await create_surgard_event(SurgardEventCreate(**parsed))

        return {"status": "ok", "id": obj.id, "saved": parsed}
        # Здесь можно обработать данные, например сохранить в БД:
        # obj = await SecurityObject.create_from_event(event.surgard)
        # return {"status": "ok", "received": event.surgard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    