include ./.env
export

all: run

pull:
	docker pull neo4j

run:
	docker run -d -p 7474:7474 -p 7687:7687 --env NEO4J_AUTH=neo4j/$(S21_NEO4J_PASS) neo4j

stop:
	docker stop $$(docker ps -a -q --filter ancestor=neo4j)

clean: stop
	docker rm $$(docker ps -a -q --filter ancestor=neo4j)