FROM python:3.8

WORKDIR /opt/telnet_scp

COPY requirements.txt .
COPY main.py .
COPY src .


RUN pip install -r requirements.txt



CMD ["python", "./main.py"]