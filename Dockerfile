FROM python:2.7
WORKDIR /usr/src/app
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    apt-get -y install nodejs
RUN git clone --depth=1 https://github.com/kcsry/infokala && \
    rm -rf infokala/.git && \
    cd infokala && \
    npm install && \
    NODE_ENV=production npm run prepublish && \
    rm -rf node_modules && \
    mkdir /usr/src/app/infokala-tracon && \
    groupadd -r infokala && useradd -r -g infokala infokala
WORKDIR /usr/src/app/infokala-tracon
COPY requirements.txt requirements-production.txt /usr/src/app/infokala-tracon/
RUN pip install --no-cache-dir -r requirements.txt -r requirements-production.txt -e ../infokala
COPY . /usr/src/app/infokala-tracon
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q .
USER infokala
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
