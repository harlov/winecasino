FROM python:3.9.4-slim-buster as base
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.5
ENV PATH=${PATH}:/root/.poetry/bin
RUN apt-get update && \
    apt-get install -y \
    curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -o /tmp/get-poetry.py && \
    python /tmp/get-poetry.py --version $POETRY_VERSION && \
    poetry config virtualenvs.create false
WORKDIR /usr/src/app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install -v --no-dev


FROM base as dev
ENV PYTHONPATH=/usr/src/app
RUN poetry install -v
COPY . .


FROM dev as tests
CMD ./scripts/test.sh

FROM base as prod
COPY . .

FROM prod as telegram_bot
COPY scripts/run_telegram_bot.sh /bin/run_telegram_bot
ENTRYPOINT /bin/run_telegram_bot

CMD bash