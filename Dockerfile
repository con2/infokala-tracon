FROM node:18
WORKDIR /usr/src/app
RUN git clone --depth=1 https://github.com/kcsry/infokala && \
    rm -rf infokala/.git && \
    cd infokala && \
    npm install && \
    NODE_ENV=production npm run prepublish && \
    rm -rf node_modules

FROM python:3.12
COPY --from=0 /usr/src/app/infokala /usr/src/app/infokala
RUN mkdir /usr/src/app/infokala-tracon && \
    groupadd -r infokala && useradd -r -g infokala infokala
WORKDIR /usr/src/app/infokala-tracon
COPY requirements.txt /usr/src/app/infokala-tracon/
RUN pip install --no-cache-dir -r requirements.txt -e ../infokala
COPY . /usr/src/app/infokala-tracon
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q .
USER infokala
EXPOSE 8000
ENTRYPOINT ["scripts/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind=0.0.0.0", "--workers=4", "--access-logfile=-", "--capture-output", "infokala_tracon.wsgi"]
