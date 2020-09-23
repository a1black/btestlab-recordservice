FROM python:3.8.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN adduser --system --group --home /home/app app

WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache --only-binary :all: -r requirements.txt

COPY . .

RUN chown -R app:app .

USER app

EXPOSE 5000/tcp

CMD ["python", "-m btestlab_recordservice", "run"]
