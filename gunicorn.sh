#!/bin/bash

# 激活虚拟环境
source /data/sarah/Flask-English-word/.venv/bin/activate

# 停止现有的 gunicorn 进程
pkill -f gunicorn || true

# 启动 gunicorn
nohup gunicorn -w 1 -b 0.0.0.0:8089 app:app --log-level debug --access-logfile - --error-logfile - > /data/sarah/Flask-English-word/gunicorn.log 2>&1 &
