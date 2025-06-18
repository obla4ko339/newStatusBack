TORTOISE_ORM = {
    "connections": {
        "default": "postgres://user:password@localhost:5432/dbname"
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