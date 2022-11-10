FROM python:3.9-alpine


RUN adduser -D telnetscp
USER telnetscp
WORKDIR /home/telnetscp

RUN python -m venv /home/telnetscp/.venv

ENV PATH="/home/telnetscp/.venv/bin:${PATH}"

RUN pip install --upgrade pip

COPY --chown=telnetscp:telnetscp requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY --chown=telnetscp:telnetscp main.py .
COPY --chown=telnetscp:telnetscp src ./src



CMD ["python", "-u", "main.py"]

EXPOSE 23