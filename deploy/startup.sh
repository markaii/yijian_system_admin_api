#!/bin/bash
export  DJANGO_SETTINGS_MODULE=project.settings.$RUN_ENV
cd /code || exit

# collectstatics
python manage.py collectstatic --noinput

# shellcheck disable=SC2046
#python manage.py makemigrations $(sed -n '/^LOCAL_APPS = \[/,/\]$/p' project/settings/base.py | grep -Po "(?<=').*(?=')" | awk '{printf " " $1}') --noinput
#python manage.py migrate --noinput

# 定时任务不放在容器中执行
# python manage.py crontab add

uwsgi --ini deploy/uwsgi.ini
