FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN useradd --uid 1001 --system --no-create-home quantee \
    && apt-get update \
    && apt-get install -yqq --no-install-recommends \
        curl \
        git \
        iputils-ping \
        netcat-openbsd \
        telnet \
        vim \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /dispatcher

COPY pyproject.toml .
COPY poetry.lock .
COPY .env .

RUN pip install poetry==2.1.3
RUN poetry config virtualenvs.create false
RUN poetry config installer.parallel false
RUN poetry config installer.parallel false
RUN poetry install --only prod

COPY dispatcher/ .

ENV PYTHONPATH=/dispatcher
RUN chmod a+x /dispatcher/start.sh \
    && chown -R quantee:quantee /dispatcher

USER quantee:quantee
ENTRYPOINT ["/bin/sh", "/dispatcher/start.sh"]
EXPOSE 8080/tcp
