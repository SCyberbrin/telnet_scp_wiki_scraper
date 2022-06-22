FROM python:3.8

WORKDIR /telnet_scp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY src/ .

CMD ["python", "./main.py"]