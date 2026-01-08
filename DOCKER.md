# Docker 部署指南

本文档介绍如何使用 Docker 部署 codingSpace 项目。

## 📋 前置要求

- Docker >= 20.10
- Docker Compose >= 2.0

## 🚀 快速开始

### 1. 生产环境部署

```bash
# 克隆项目
git clone <repository-url>
cd codingSpace

# 配置环境变量
cp backend/env.example backend/.env
# 编辑 backend/.env 文件，修改配置（特别是 SECRET_KEY）

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. 开发环境部署

```bash
# 使用开发配置启动
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f backend
```

## 🏗️ 服务说明

### 数据库服务 (db)

- **镜像**: postgres:15-alpine
- **端口**: 5432
- **数据持久化**: `postgres_data` volume
- **健康检查**: 自动检查数据库就绪状态

### 后端服务 (backend)

- **端口**: 8000
- **API 文档**: http://localhost:8000/docs
- **文件上传目录**: `/app/uploads` (持久化到 `backend_uploads` volume)
- **环境变量**: 从 `backend/.env` 读取

### 前端服务 (frontend)

- **端口**: 80
- **访问地址**: http://localhost
- **构建**: 使用多阶段构建，最终使用 nginx 提供静态文件

## 🔧 环境变量配置

在 `backend/.env` 文件中配置以下变量：

```env
# 应用配置
APP_NAME=codingSpace Backend
APP_VERSION=1.0.0
DEBUG=False

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置（Docker Compose 会自动设置）
DATABASE_URL=postgresql://codingspace:codingspace_password@db:5432/codingspace

# JWT配置
SECRET_KEY=your-strong-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:80

# 文件存储配置
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
```

## 📦 常用命令

### 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 启动特定服务
docker-compose up -d backend

# 前台运行（查看日志）
docker-compose up
```

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除 volumes（注意：会删除数据）
docker-compose down -v
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend

# 查看最近 100 行日志
docker-compose logs --tail=100 backend
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec db psql -U codingspace -d codingspace
```

### 构建镜像

```bash
# 构建所有服务镜像
docker-compose build

# 构建特定服务镜像
docker-compose build backend

# 强制重新构建（不使用缓存）
docker-compose build --no-cache backend
```

## 🔄 更新服务

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 或者只更新特定服务
docker-compose up -d --build backend
```

## 🗄️ 数据管理

### 备份数据库

```bash
# 创建备份
docker-compose exec db pg_dump -U codingspace codingspace > backup.sql

# 或者使用 volume 备份
docker run --rm -v codingspace_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

### 恢复数据库

```bash
# 从 SQL 文件恢复
docker-compose exec -T db psql -U codingspace codingspace < backup.sql
```

### 查看数据卷

```bash
# 列出所有 volumes
docker volume ls

# 查看特定 volume 信息
docker volume inspect codingspace_postgres_data
```

## 🔍 故障排查

### 服务无法启动

```bash
# 查看服务状态
docker-compose ps

# 查看详细日志
docker-compose logs backend

# 检查容器健康状态
docker-compose ps --format json | jq '.[] | {name: .Name, health: .Health}'
```

### 数据库连接问题

```bash
# 检查数据库是否就绪
docker-compose exec db pg_isready -U codingspace

# 测试连接
docker-compose exec backend python -c "from app.db.database import engine; engine.connect()"
```

### 端口冲突

如果端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 改为其他端口
```

## 🌐 与外部服务集成

### 连接其他 Docker 服务

如果需要在同一网络中连接其他 Docker 服务（如新闻爬虫服务），可以：

1. 将服务添加到 `docker-compose.yml` 的 `networks` 中
2. 使用服务名作为主机名访问（如 `http://news-crawler:8080`）

### 示例：添加新闻爬虫服务

```yaml
services:
  news-crawler:
    image: your-news-crawler-image:latest
    container_name: codingspace-news-crawler
    environment:
      - API_URL=http://backend:8000/api/v1/news
    networks:
      - codingspace-network
    restart: unless-stopped
```

## 🔒 生产环境建议

1. **修改默认密码**：更改数据库和应用的默认密码
2. **使用强密钥**：设置强随机 `SECRET_KEY`
3. **启用 HTTPS**：使用 Nginx 反向代理并配置 SSL
4. **限制资源**：为容器设置 CPU 和内存限制
5. **定期备份**：设置数据库自动备份
6. **监控日志**：使用日志收集工具（如 ELK）
7. **安全扫描**：定期扫描镜像漏洞

## 📊 资源使用

典型资源使用情况：

- **数据库**: ~100MB 内存
- **后端**: ~150MB 内存
- **前端**: ~50MB 内存
- **总计**: ~300MB 内存

## 📝 注意事项

- 首次启动可能需要一些时间来下载镜像
- 数据库初始化需要几秒钟
- 文件上传目录会自动创建并持久化
- 开发环境使用 `docker-compose.dev.yml` 支持热重载

## 🆘 获取帮助

如果遇到问题，可以：

1. 查看服务日志：`docker-compose logs`
2. 检查容器状态：`docker-compose ps`
3. 查看 Docker 文档：https://docs.docker.com/


