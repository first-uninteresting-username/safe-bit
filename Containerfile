FROM docker.io/library/python:3.15-slim@sha256:e97b88e416c3c01eb427b21fd8cd3ebf006e6ee38afcfcc3cae1c54ee2ab0a75 AS builder

WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN pip install --prefix=/install .

FROM docker.io/library/python:3.15-slim@sha256:e97b88e416c3c01eb427b21fd8cd3ebf006e6ee38afcfcc3cae1c54ee2ab0a75

COPY --from=builder /install /usr/local
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin safe-bit \
 && mkdir -p /var/lib/safe-bit \
 && chown safe-bit:safe-bit /var/lib/safe-bit
VOLUME ["/var/lib/safe-bit"]
USER 10001
ENV PYTHONDONTWRITEBYTECODE=1
ENV SAFE_BIT_HOST=0.0.0.0
ENV SAFE_BIT_PORT=8000
ENV DB_PATH=/var/lib/safe-bit/app.sqlite3
EXPOSE 8000

CMD ["safe-bit"]
