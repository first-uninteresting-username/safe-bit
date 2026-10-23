FROM docker.io/library/python:3.14-slim as builder

COPY pyproject.toml, README.md, LICENSE, src/ ./
RUN pip install --prefix=/install .

FROM docker.io/library/python:3.14-slim

COPY --from=builder /install /usr/local
RUN useradd --system --uid 10001 --no-create-home safebit \
 && mkdir -p /var/lib/safe-bit \
 && chown safebit:safebit /var/lib/safe-bit
VOLUME ["/var/lib/safe-bit"]
USER safe-bit-user
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DB_PATH=/var/lib/safe-bit
EXPOSE 8000


CMD ["safe-bit"]
