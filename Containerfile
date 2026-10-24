FROM docker.io/library/python:3.15-slim@sha256:044d5bd747976e21f8bc4d746c3479b19a84bb8ae6261b802acdd26b29036c93 as builder

COPY pyproject.toml, README.md, LICENSE, src/ ./
RUN pip install --prefix=/install .

FROM docker.io/library/python:3.15-slim@sha256:044d5bd747976e21f8bc4d746c3479b19a84bb8ae6261b802acdd26b29036c93

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
