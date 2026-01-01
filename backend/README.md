# codingSpace 后端API

基于 FastAPI 框架的后端服务，为 codingSpace 个人网站平台提供 RESTful API。

## 🚀 技术栈

- **FastAPI** - 现代、快速的 Web 框架
- **SQLAlchemy** - ORM 框架
- **Pydantic** - 数据验证
- **JWT** - 身份认证
- **Bcrypt** - 密码加密
- **Uvicorn** - ASGI 服务器
- **aiofiles** - 异步文件操作
- **Pillow** - 图像处理
- **httpx** - 异步 HTTP 客户端（用于与其他服务通信）

## 📦 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   └── v1/
│   │       ├── auth.py   # 认证相关API
│   │       └── problems.py # 题目相关API
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── security.py   # 安全工具
│   ├── db/               # 数据库
│   │   └── database.py     # 数据库连接
│   ├── models/           # 数据模型
│   │   ├── user.py       # 用户模型
│   │   ├── problem.py    # 题目模型
│   │   ├── blog.py       # 博客模型
│   │   ├── ebook.py      # 电子书模型
│   │   ├── file.py       # 文件模型
│   │   └── news.py       # 新闻模型
│   └── schemas/          # Pydantic模式
│       ├── user.py       # 用户模式
│       ├── problem.py    # 题目模式
│       ├── blog.py       # 博客模式
│       ├── ebook.py      # 电子书模式
│       ├── file.py       # 文件模式
│       └── news.py       # 新闻模式
├── main.py               # 应用入口
├── requirements.txt      # 依赖列表
├── Dockerfile            # Docker 镜像构建文件
└── env.example           # 环境变量示例
```

## 🛠️ 安装和运行

### 环境要求

- Python >= 3.8
- pip

### 本地开发

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，修改以下配置：
- `SECRET_KEY`: 用于JWT签名的密钥（生产环境请使用强随机字符串）
- `DATABASE_URL`: 数据库连接URL
- `CORS_ORIGINS`: 允许的前端域名
- `UPLOAD_DIR`: 文件上传目录
- `MAX_UPLOAD_SIZE`: 最大上传文件大小（字节）
- `NEWS_CRAWLER_URL`: 新闻爬虫服务地址（可选）

### 运行服务

```bash
# 开发模式（自动重载）
python main.py

# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动。

### Docker 部署

```bash
# 构建镜像
docker build -t codingspace-backend .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/.env:/app/.env \
  codingspace-backend
```

或使用 Docker Compose（推荐）：

```bash
# 在项目根目录
docker-compose up -d backend
```

## 📡 API端点

### 认证相关

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录（OAuth2格式）
- `POST /api/v1/auth/login-json` - 用户登录（JSON格式）
- `GET /api/v1/auth/me` - 获取当前用户信息

### 题目相关

- `POST /api/v1/problems` - 创建题目
- `GET /api/v1/problems` - 获取题目列表
- `GET /api/v1/problems/{problem_id}` - 获取单个题目
- `PUT /api/v1/problems/{problem_id}` - 更新题目
- `DELETE /api/v1/problems/{problem_id}` - 删除题目
- `GET /api/v1/problems/date/{date}` - 根据日期获取题目

### 博客相关（待实现）

- `POST /api/v1/blogs` - 创建博客
- `GET /api/v1/blogs` - 获取博客列表
- `GET /api/v1/blogs/{blog_id}` - 获取单个博客
- `PUT /api/v1/blogs/{blog_id}` - 更新博客
- `DELETE /api/v1/blogs/{blog_id}` - 删除博客

### 电子书相关（待实现）

- `POST /api/v1/ebooks` - 上传电子书
- `GET /api/v1/ebooks` - 获取电子书列表
- `GET /api/v1/ebooks/{ebook_id}` - 获取单个电子书
- `PUT /api/v1/ebooks/{ebook_id}` - 更新电子书信息
- `DELETE /api/v1/ebooks/{ebook_id}` - 删除电子书

### 文件相关（待实现）

- `POST /api/v1/files` - 上传文件
- `GET /api/v1/files` - 获取文件列表
- `GET /api/v1/files/{file_id}` - 获取文件信息
- `GET /api/v1/files/{file_id}/download` - 下载文件
- `DELETE /api/v1/files/{file_id}` - 删除文件

### 新闻相关（待实现）

- `GET /api/v1/news` - 获取新闻列表
- `GET /api/v1/news/{news_id}` - 获取单个新闻
- `POST /api/v1/news/sync` - 从爬虫服务同步新闻
- `GET /api/v1/news/categories` - 获取新闻分类

## 🔐 认证方式

API使用JWT（JSON Web Token）进行身份认证。

1. 用户登录后，服务器返回 `access_token`
2. 在后续请求中，需要在请求头中添加：
   ```
   Authorization: Bearer <access_token>
   ```

## 📝 数据模型

### User（用户）
- 用户基本信息
- 认证信息

### Problem（题目）
- 刷题记录
- 题目信息、代码、解析等

### Blog（博客）
- 博客文章
- 标题、内容、标签、分类等

### Ebook（电子书）
- 电子书文件
- 元数据、阅读进度等

### File（文件）
- 上传的文件
- 文件信息、分类、标签等

### News（新闻）
- 新闻内容
- 来源、分类、标签等

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t codingspace-backend .
```

### 运行容器

```bash
docker run -d \
  --name codingspace-backend \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/.env:/app/.env \
  codingspace-backend
```

### 使用 Docker Compose

在项目根目录运行：

```bash
docker-compose up -d backend
```

详细部署说明请参考 [DOCKER.md](../DOCKER.md)。

## 🔧 开发说明

### 数据库迁移

当前使用SQLite作为默认数据库，表结构会在首次运行时自动创建。

如需使用其他数据库（如PostgreSQL、MySQL），修改 `.env` 中的 `DATABASE_URL` 即可。

### 添加新功能

1. 在 `app/models/` 中定义数据模型
2. 在 `app/schemas/` 中定义Pydantic模式
3. 在 `app/api/v1/` 中创建API路由
4. 在 `app/api/v1/__init__.py` 中注册路由

### 文件上传

文件上传功能使用 FastAPI 的 `File` 和 `UploadFile`：

```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 处理文件上传
    pass
```

### 与外部服务集成

使用 `httpx` 异步客户端与其他 Docker 服务通信：

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://news-crawler:8080/api/news")
```

## 📄 License

MIT
