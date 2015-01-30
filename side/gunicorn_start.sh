#!/bin/bash
NAME='epm'
DJANGODIR=/home/jasonsun/git_repo/side
SOCKFILE=/home/jasonsun/git_repo/side/run/gunicorn.sock
USER=jasonsun
GROUP=jasonsun
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=side.settings
DJANGO_WSGI_MODULE=side.wsgi

echo "starting $NAME as `whoami` "
#激活python虚拟运行环境
cd $DJANGODIR
# source ../bin/activate
# export $DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
# export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER \
    --group=$GROUP \
    --log-level=debug \
    --bind=unix:$SOCKFILE
