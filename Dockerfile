FROM --platform=linux/amd64 python:3.8.12-slim AS runner
MAINTAINER jeyrce@gmail.com
WORKDIR /ishare
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/  \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir && \
    python /ishare/manage.py collectstatic

EXPOSE 7777
VOLUME /ishare/db.sqlite3 /ishare/media /ishare/STATIC
CMD ["python3", \
    "manage.py", \
    "runserver", \
    "--noreload", \
    "--insecure", \
    "--no-color", \
    "0.0.0.0:7777" \
]

