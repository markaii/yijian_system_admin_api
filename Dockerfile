
# 构建 基础镜像
FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD ./requirements.txt .
RUN set -ex \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone \
    && mkdir -p /code /logs \
    && pip3 install --no-cache-dir uwsgi -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/ \
    && sed -i "s/^if version < (1, 3, 13):/# &/" /usr/local/lib/python3.7/site-packages/django/db/backends/mysql/base.py \
    && sed -i "s/^    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)/# &/" /usr/local/lib/python3.7/site-packages/django/db/backends/mysql/base.py \
    && sed -i "s/^        if query is not None:/# &/" /usr/local/lib/python3.7/site-packages/django/db/backends/mysql/operations.py \
    && sed -i "s/^            query = query.decode(errors='replace')/# &/" /usr/local/lib/python3.7/site-packages/django/db/backends/mysql/operations.py
COPY . /code
WORKDIR /code
CMD ["/bin/bash", "-c", "source /code/deploy/startup.sh"]