#!/bin/bash

# codingSpace 后端启动脚本
set -euo pipefail
cd "$(dirname "$0")"

# 选择 Python 解释器（必须使用 python3.10）
if ! command -v python3.10 >/dev/null 2>&1; then
  echo "未检测到 python3.10，请先安装："
  echo "  macOS（Homebrew）：brew install python@3.10"
  echo "安装完成后重试：bash backend/run.sh"
  exit 1
fi
PY_BIN="python3.10"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    "$PY_BIN" -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.installed" ]; then
    echo "安装依赖..."
    python -m pip install --upgrade pip setuptools wheel
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
