FROM python:3.9-alpine



WORKDIR /home/telnetscp


RUN pip install --upgrade pip


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt



COPY . .

CMD ["python", "-u", "main.py"]

EXPOSE 23