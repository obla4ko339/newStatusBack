DOCKER_COMP = docker compose -f docker-compose.yaml
MANAGER = $(DOCKER_COMP) exec backend uv run
AERICH = $(MANAGER) aerich

up:
	@$(DOCKER_COMP) up --detach --wait

down:
	@$(DOCKER_COMP) down --remove-orphans

bash:
	@$(DOCKER_COMP) exec $(name) bash

migrations:
	@$(AERICH) migrate

migrate:
	@$(AERICH) upgrade

rollback:
	@$(AERICH) downgrade

init-db:
	@$(AERICH) init-db

init-aerich:
	@$(AERICH) init -t src.core.db.TORTOISE_ORM

logs:
	@$(DOCKER_COMP) logs $(name) --tail=0 --follow

linter:
	@uv run black .