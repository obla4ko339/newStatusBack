from src.core.settings import settings

TORTOISE_ORM = {
    "connections": {
        "default": settings.db.connection_string
    },
    "apps": {
        "models": {
            "models": [
                "src.models.customers",
                "src.models.serure_objects", 
                "aerich.models"
                ],
            "default_connection": "default"
        }
    }
}