# codingSpace

一个基于 Vue 3 + FastAPI 的个人网站平台，集成了多种实用工具、新闻热点和内容管理功能。

## 📁 项目结构

```
codingSpace/
├── frontend/          # 前端项目（Vue 3 + Vite）
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/           # 后端项目（FastAPI）
│   ├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml  # Docker Compose 配置
└── README.md
```

## ✨ 功能特性

### 🛠️ 实用工具集
- **代码格式化**：支持多种编程语言的代码格式化
- **文本比对**：对比两个文本文件的差异
- **自动生成密码**：生成安全、复杂的密码
- **编解码工具**：Base64、URL、HTML 等编解码
- **更多工具**：持续添加中...

### 📰 新闻热点
- **新闻聚合**：展示各类新闻内容
- **Docker 服务集成**：支持从其他 Docker 服务（如爬虫服务）获取新闻数据
- **分类浏览**：按类别查看不同新闻
- **搜索功能**：快速搜索感兴趣的新闻

### 📝 内容记录
- **博客管理**：发布和管理个人博客文章
- **电子书管理**：上传和管理电子书文件
- **刷题记录**：记录算法刷题进度和笔记
- **文件上传**：支持多种文件格式上传
- **在线预览**：支持文档、图片等文件的在线预览
- **分类标签**：灵活的内容分类和标签系统

### 🔐 用户系统
- **用户注册/登录**：安全的用户认证系统
- **个人中心**：管理个人信息和内容
- **数据同步**：多设备数据同步

## 🛠️ 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架（Composition API）
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Axios** - HTTP 客户端

### 后端
- **FastAPI** - 现代、快速的 Python Web 框架
- **SQLAlchemy** - Python ORM 框架
- **Pydantic** - 数据验证
- **JWT** - 身份认证
- **Uvicorn** - ASGI 服务器
- **Pillow** - 图像处理（用于文件预览）
- **aiofiles** - 异步文件操作

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理（可选）

## 🚀 快速开始

### 使用 Docker Compose（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd codingSpace

# 配置环境变量
cp backend/env.example backend/.env
# 编辑 backend/.env 文件，修改配置

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

服务将在以下地址启动：
- 前端：`http://localhost:3000`
- 后端：`http://localhost:8000`
- API 文档：`http://localhost:8000/docs`

### 本地开发

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动。

#### 后端开发

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，修改配置

# 运行服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

### API文档

启动后端服务后，可以访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐳 Docker 部署

### 构建镜像

```bash
# 构建后端镜像
docker build -t codingspace-backend ./backend

# 构建前端镜像（如果需要）
docker build -t codingspace-frontend ./frontend
```

### 使用 Docker Compose

项目提供了 `docker-compose.yml` 文件，可以一键启动所有服务：

```bash
docker-compose up -d
```

### 环境变量配置

在 `backend/.env` 文件中配置以下变量：

```env
# 应用配置
APP_NAME=codingSpace Backend
APP_VERSION=1.0.0
DEBUG=False

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=postgresql://user:password@db:5432/codingspace

# JWT配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS配置
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 文件存储配置
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760  # 10MB
```

## 📖 使用说明

### 工具使用

1. **代码格式化**：选择语言，粘贴代码，一键格式化
2. **文本比对**：上传或粘贴两个文本，查看差异
3. **密码生成**：设置长度和复杂度，生成安全密码
4. **编解码**：选择编码类型，输入内容进行编解码

### 新闻热点

1. **浏览新闻**：在新闻页面查看最新热点
2. **分类筛选**：按类别查看不同新闻
3. **搜索新闻**：使用搜索功能查找感兴趣的内容
4. **Docker 服务集成**：配置爬虫服务地址，自动获取新闻

### 内容管理

1. **发布博客**：创建和编辑博客文章
2. **上传文件**：上传电子书、文档等文件
3. **在线预览**：直接在线预览上传的文件
4. **刷题记录**：记录算法刷题进度和笔记
5. **分类管理**：使用标签和分类组织内容

## 🎨 界面特色

- **科幻风格**：采用深色主题，配合青色和紫色渐变
- **动态效果**：流畅的动画和过渡效果
- **响应式设计**：适配不同屏幕尺寸
- **现代化 UI**：毛玻璃效果、渐变文字、发光边框等

## 🔐 后端框架选择说明

本项目后端选择了 **FastAPI** 框架。详细对比分析请查看 [FRAMEWORK_COMPARISON.md](./FRAMEWORK_COMPARISON.md)。

### 选择 FastAPI 的理由

1. **文件上传支持**：原生支持文件上传，适合内容管理需求
2. **异步处理**：支持异步操作，适合与 Docker 服务集成
3. **Docker 友好**：轻量级，易于容器化部署
4. **高性能**：适合处理多种工具和内容管理的高并发需求
5. **自动文档**：自动生成 API 文档，方便前后端协作
6. **类型安全**：基于类型提示，减少 bug

## ⚠️ 注意事项

- 生产环境部署前，请修改 `.env` 中的 `SECRET_KEY` 为强随机字符串
- 文件上传大小限制可在配置中调整
- 建议使用 PostgreSQL 作为生产环境数据库
- Docker 部署时注意数据持久化（使用 volumes）
- 与外部 Docker 服务集成时，注意网络配置和安全性

## 📝 开发计划

- [x] 实现前后端分离架构
- [x] 实现用户认证系统
- [x] Docker 部署配置
- [ ] 实现工具集 API（代码格式化、文本比对等）
- [ ] 实现新闻热点 API（支持 Docker 服务集成）
- [ ] 实现内容管理 API（博客、电子书、文件上传）
- [ ] 实现文件在线预览功能
- [ ] 前端集成后端 API
- [ ] 添加更多实用工具
- [ ] 实现数据统计功能
- [ ] 优化 Docker 部署流程

## 📄 License

MIT

## 👤 作者

codingSpace

---

© 2024 codingSpace. All rights reserved.
