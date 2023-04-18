#!/bin/bash

# 安装必要的 Python 模块
pip install notion-client

# 执行 Python 脚本
python hx_script.py $COOKIE $NOTION_TOKEN $DATABASE_ID
