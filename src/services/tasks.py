from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.services.cnord import CnordClient
import asyncio

client = CnordClient()
scheduler = AsyncIOScheduler()

async def weekly_data_sync():
    results = await client.write_secure_objects()
    for id in results["ids"]:
        await client.write_customers(site_id=id)

# Планировщик: каждую неделю в понедельник в 03:00
scheduler.add_job(weekly_data_sync, CronTrigger(day_of_week='mon', hour=3, minute=0))

def start():
    scheduler.start()

def stop():
    scheduler.shutdown()