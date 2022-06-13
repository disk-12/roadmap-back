.PHONY: ps up restart reup down logs api

ps:
	docker-compose ps

up:
	docker-compose up -d

restart:
	docker-compose restart

reup:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f

api:
	docker-compose exec api /bin/bash