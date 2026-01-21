from src.core.settings import settings

print("DB Connection String:", settings.db.connection_string)

TORTOISE_ORM = {
    "connections": {
        "default": settings.db.connection_string
    },
    "apps": {
        "models": {
            "models": [
                "src.models.list_events",
                "src.models.list_objects",
                "src.models.customers", 
                "src.models.serure_objects",
                "src.models.user", 
                "src.models.sites_user", 
                "src.models.surgard_event", 
                "src.models.sites", 
                "src.models.group_user", 
                "aerich.models"
                ],
            "default_connection": "default"
        }
    },
    "use_tz": True,
    "timezone": "UTC",
}