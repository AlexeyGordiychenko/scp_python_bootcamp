all: run

build:
	docker build -t redis_ex01 .

run: build
	docker run -d -p 6379:6379 redis_ex01

stop:
	docker stop redis_ex01

clean: stop
	docker rmi redis_ex01
