FROM python:3.8.5-slim-buster

EXPOSE 5000

RUN adduser --system --group --home /home/app app

WORKDIR /home/app

COPY --chown=app:app ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache --only-binary :all: -r requirements.txt

COPY --chown=app:app . .

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "btestlab_recordservice.app:app"]
