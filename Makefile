.PHONY: up down logs seed psql
up:
	docker compose up -d --build
down:
	docker compose down
logs:
	docker compose logs -f
psql:
	docker exec -it $$(docker ps -qf name=db) psql -U spend -d spenddb
