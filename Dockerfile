FROM python:3.12-slim AS builder

WORKDIR /usr/src/app

COPY . .

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim

WORKDIR /usr/src/app

COPY --from=builder /opt/venv /opt/venv
COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["/opt/venv/bin/gunicorn", "--chdir", "src", "--bind", "0.0.0.0:5000", "--worker-class", "eventlet", "main:main()"]
