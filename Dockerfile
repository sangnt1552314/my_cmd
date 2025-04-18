ARG PYTHON_VERSION=3.13.3-bookworm

FROM python:${PYTHON_VERSION} as base
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

FROM base AS dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM base AS runtime
COPY --from=dependencies /app/wheels /wheels
COPY --from=dependencies /app/requirements.txt .

RUN pip install --no-cache /wheels/*

FROM base AS development
COPY --from=dependencies /app/wheels /wheels
COPY --from=dependencies /app/requirements.txt .

RUN pip install --no-cache /wheels/*