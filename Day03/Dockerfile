FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y ansible sshpass
WORKDIR /hack
COPY EX00/exploit.py .
COPY EX01/consumer.py .
COPY EX02/deploy.yml ./EX02/
COPY EX00/evilcorp.html ./EX02/

CMD [ "ansible-playbook", "EX02/deploy.yml"]
