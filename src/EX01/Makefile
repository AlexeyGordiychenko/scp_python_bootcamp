all: run

build:
	docker build -t redis_ex01 .

run: build
	docker run -d -p 6379:6379 redis_ex01

stop:
	docker stop $$(docker ps -a -q --filter ancestor=redis_ex01)

clean: stop
	docker rm $$(docker ps -a -q --filter ancestor=redis_ex01)
