FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /usr/src/app
COPY pyproject.toml uv.lock manage.py ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev
COPY scripts /usr/src/app/scripts
COPY infokala_tracon /usr/src/app/infokala_tracon
COPY kompassi_oauth2 /usr/src/app/kompassi_oauth2
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/usr/src/app/.venv/bin:$PATH"
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    chmod 755 manage.py scripts/*.sh


FROM python:3.14-slim-bookworm

RUN groupadd -g 998 -r kompassi && useradd -r -g kompassi -u 998 kompassi && \
    apt-get update && \
    apt-get -y install libpq5 && \
    rm -rf /var/lib/apt/lists
COPY --from=builder --chown=root:root /usr/src/app /usr/src/app
ENV PATH="/usr/src/app/.venv/bin:$PATH"

USER kompassi
WORKDIR /usr/src/app
ENV PATH="/usr/src/app/.venv/bin:$PATH"
# mount tmpfs at /tmp to silence "FontConfig: No writable cache directories" warnings
ENV HOME=/tmp

ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
