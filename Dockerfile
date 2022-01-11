FROM python:3.8.12 AS runner
MAINTAINER jeyrce@gmail.com
WORKDIR /ishare
ADD . .
RUN pip install -r requirements.txt \
    -i https://mirrors.aliyun.com/pypi/simple/  \
    --trusted-host mirrors.aliyun.com \
    --no-cache-dir && python manager.py collectstatic

EXPOSE 7777:7777
CMD ["/usr/local/bin/uwsgi", "--ini", "/ishare/confs/uwsgi/uwsgi-docker.ini"]

