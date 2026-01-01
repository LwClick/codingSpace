#!/bin/bash

# codingSpace 后端启动脚本

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.installed" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件..."
    cp env.example .env
    echo "请编辑 .env 文件，修改配置（特别是 SECRET_KEY）"
fi

# 运行服务
echo "启动后端服务..."
python main.py

