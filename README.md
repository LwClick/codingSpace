# 算法刷题日历

一个基于 Vue3 的算法刷题展示系统，通过日历形式管理每天的刷题记录。

## 功能特性

- 📅 **日历视图**：直观展示每天的刷题情况
- ➕ **题目管理**：轻松添加、编辑和查看题目
- 💻 **代码编辑器**：支持 Python 代码编辑，带语法高亮
- ▶️ **代码运行**：直接在浏览器中运行 Python 代码（基于 Pyodide）
- 📝 **题目解析**：记录每道题的解题思路和解析
- 💾 **本地存储**：使用 localStorage 保存数据

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **CodeMirror 6** - 代码编辑器
- **Pyodide** - 在浏览器中运行 Python

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

### 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录

### 预览生产版本

```bash
npm run preview
```

## 使用说明

1. **查看日历**：主页面显示当前月份的日历，有题目的日期会显示题目数量
2. **添加题目**：
   - 点击日历上任意日期的 "+" 按钮
   - 或点击日期单元格，然后在下方列表点击添加
3. **编辑题目**：点击题目列表中的"编辑"按钮
4. **运行代码**：在题目编辑弹窗中，点击"运行代码"按钮即可在浏览器中执行 Python 代码
5. **查看题目**：点击日历上的日期或题目列表中的题目项即可查看详情

## 项目结构

```
├── src/
│   ├── components/          # Vue 组件
│   │   ├── Calendar.vue      # 日历组件
│   │   ├── ProblemModal.vue  # 题目弹窗组件
│   │   └── CodeEditor.vue    # 代码编辑器组件
│   ├── utils/                # 工具函数
│   │   ├── storage.js        # 数据存储
│   │   └── pythonRunner.js   # Python 代码运行器
│   ├── styles/               # 样式文件
│   │   └── main.css          # 主样式
│   ├── App.vue               # 根组件
│   └── main.js               # 入口文件
├── index.html                # HTML 模板
├── package.json              # 项目配置
└── vite.config.js            # Vite 配置
```

## 注意事项

- 代码运行功能需要加载 Pyodide，首次运行可能需要一些时间
- 数据存储在浏览器的 localStorage 中，清除浏览器数据会丢失所有题目
- Python 代码运行环境有限制，某些系统级操作可能无法执行

## License

MIT

