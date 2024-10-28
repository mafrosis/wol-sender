FROM python:3.12-slim AS builder

WORKDIR /src

RUN pip install wheel

# Fetch/build wheels for dependencies
COPY pyproject.toml /src
COPY wol_sender /src/wol_sender

# Build application wheel
RUN python -m pip wheel --no-cache-dir --wheel-dir /dist .

# ---

FROM python:3.12-slim

WORKDIR /src

# Copy in the built wheels
COPY --from=builder /dist /dist

# Depend on nslookup & ping
RUN apt update && apt install -y dnsutils iputils-ping

# Install
RUN python -m pip install --no-index --find-links=/dist --no-cache wol_sender

ENTRYPOINT ["wol-sender"]
CMD ["start"]
