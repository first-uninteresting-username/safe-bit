FROM docker.io/library/python:3.15-slim@sha256:044d5bd747976e21f8bc4d746c3479b19a84bb8ae6261b802acdd26b29036c93 AS builder

WORKDIR /build
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN pip install --prefix=/install .

FROM docker.io/library/python:3.15-slim@sha256:044d5bd747976e21f8bc4d746c3479b19a84bb8ae6261b802acdd26b29036c93

COPY --from=builder /install /usr/local
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin safe-bit \
 && mkdir -p /var/lib/safe-bit \
 && chown safe-bit:safe-bit /var/lib/safe-bit
VOLUME ["/var/lib/safe-bit"]
USER 10001
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DB_PATH=/var/lib/safe-bit/app.sqlite3
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/health')"]

CMD ["safe-bit"]
