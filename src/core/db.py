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
                "aerich.models"
                ],
            "default_connection": "default"
        }
    }
}