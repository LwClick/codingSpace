@echo off
REM codingSpace 后端启动脚本 (Windows)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
if not exist "venv\.installed" (
    echo 安装依赖...
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM 检查环境变量文件
if not exist ".env" (
    echo 创建 .env 文件...
    copy env.example .env
    echo 请编辑 .env 文件，修改配置（特别是 SECRET_KEY）
)

REM 运行服务
echo 启动后端服务...
python main.py

