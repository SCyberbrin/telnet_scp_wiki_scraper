FROM python:3.8

WORKDIR /opt/telnet_scp

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY main.py .
COPY src ./src



CMD ["python", "-u", "./main.py"]

EXPOSE 23