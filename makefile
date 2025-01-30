####################################################################################################################
# Setup containers to run Airflow

docker-spin-up:
	docker compose build && docker compose up airflow-init && docker compose up --build -d 

perms:
	sudo mkdir -p logs plugins dags && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins dags

do-sleep:
	sleep 30

up: perms docker-spin-up do-sleep

down:
	docker compose down

restart: down up

sh:
	docker exec -ti webserver bash

####################################################################################################################