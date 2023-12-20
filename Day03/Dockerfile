FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y ansible sshpass
WORKDIR /hack
COPY materials ./materials
COPY src/EX00/exploit.py .
COPY src/EX01/consumer.py .
COPY src/EX02/deploy.yml ./src/EX02/deploy.yml

CMD [ "ansible-playbook", "src/EX02/deploy.yml"]
