# LLM Wiki — 个人知识库

**简体中文** | [English](README.en.md)

一个基于 Obsidian + LLM Wiki 持续维护的个人知识库。灵感来自 [Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

核心理念：知识不是每次查询时从零推导，而是被**编译一次、持续积累**。人类负责策展素材和提出问题，LLM 负责所有繁琐的整理工作——摘要、交叉引用、归档、一致性维护。

## 与传统 RAG 的区别

| | 传统 RAG | LLM Wiki |
|---|---|---|
| 知识存储 | 原始文档 + 向量索引 | 结构化、互相链接的 Markdown 页面 |
| 查询方式 | 每次从零检索、拼凑 | 基于已编译的知识综合回答 |
| 知识积累 | 无——每次重新推导 | 有——每次操作都让 wiki 更丰富 |
| 交叉引用 | 无 | 自动维护的 `[[双链]]` 网络 |
| 矛盾处理 | 不感知 | 主动标注、注明来源 |

## 架构

```
├── AGENTS.md          # Schema 规范（OpenAI Codex 等通用 Agent）
├── CLAUDE.md          # Schema 规范（Claude Code 适配）
├── GEMINI.md          # Schema 规范（Gemini CLI 适配）
├── raw/               # 原始素材（人类策展，LLM 只读）
│   ├── articles/      # 网络文章、博客
│   ├── papers/        # 学术论文、白皮书
│   ├── docs/          # 官方文档摘录
│   ├── transcripts/   # 会议记录、演讲稿、播客笔记
│   └── assets/        # 图片、图表、数据文件
├── wiki/              # LLM 编译产物（LLM 读写，人类只读）
│   ├── index.md       # 全局索引
│   ├── log.md         # 操作日志
│   ├── entities/      # 实体页（工具、框架、人物）
│   ├── concepts/      # 概念页（模式、方法论）
│   ├── summaries/     # 素材摘要页
│   ├── comparisons/   # 对比分析页
│   └── synthesis/     # 综合分析页
└── output/            # 成品输出（LLM 生成，人类审核定稿）
    ├── posts/         # 博客文章、公众号文章
    ├── reports/       # 研究报告、技术调研报告
    ├── slides/        # 演示文稿（Marp 格式）
    ├── tutorials/     # 教程、手把手指南
    └── newsletters/   # 周报、月报、知识简报
```

## 工作流

| 操作 | 触发方式 | 说明 |
|---|---|---|
| Ingest | 新素材放入 `raw/`，告诉 LLM 处理 | LLM 读取素材 → 提取要点 → 创建/更新 Wiki 页面 → 维护交叉引用 |
| Query | 向 LLM 提问 | LLM 基于 Wiki 已编译知识回答，有价值的回答可存回 Wiki |
| Lint | 定期要求 LLM 检查 | 检查矛盾、孤立页面、缺失引用、过时内容，保持 Wiki 健康 |
| Publish | 要求 LLM 从`wiki`提炼成品输出 | LLM 生成，人类审核定稿 |

## 核心原则

- **Schema 层**（`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`）：告诉 LLM 如何维护 wiki
- **Raw 层**（`raw/`）：不可变的原始素材，是事实来源
- **Wiki 层**（`wiki/`）：LLM 的编译产物，所有知识的结构化呈现
- **Output 层**（`output/`）：从 wiki 提炼的成品，面向外部受众，独立可读
- 知识复利：每次操作都让 Wiki 更丰富
- 详细规范见 [AGENTS.md](AGENTS.md)

## 快速开始

### 1. 选择你的 LLM Agent

本项目提供三份等价的 Schema 文件，选择你使用的工具对应的即可：

| 工具 | Schema 文件 | 说明 |
|------|-----------|------|
| OpenAI Codex / 通用 | `AGENTS.md` | 通用规范 |
| Claude Code | `CLAUDE.md` | 适配 Claude 的工具调用方式 |
| Gemini CLI | `GEMINI.md` | 适配 Gemini 的工具和上下文窗口 |
| Kiro | `AGENTS.md` | Kiro 自动读取 AGENTS.md |

### 2. 添加素材

将你要消化的素材放入 `raw/` 对应子目录：

```bash
# 网络文章（推荐用 Obsidian Web Clipper 保存为 Markdown）
raw/articles/2026-04-13-some-article.md

# 学术论文
raw/papers/2026-04-13-some-paper.pdf

# 会议记录、读书笔记
raw/transcripts/2026-04-13-meeting-notes.md
```

建议在文件开头注明来源 URL、作者、日期。

### 3. 让 LLM 消化

告诉你的 LLM Agent：

```
消化 raw/articles/2026-04-13-some-article.md
```

LLM 会：
1. 阅读素材，与你讨论关键要点
2. 创建素材摘要页（`wiki/summaries/`）
3. 创建或更新相关实体页和概念页
4. 维护所有交叉引用
5. 更新全局索引和操作日志

### 4. 提问

直接向 LLM 提问，它会基于 wiki 中已编译的知识回答：

```
对比 Playwright 和 Cypress 的优劣
```

有价值的回答可以归档为 wiki 页面（对比分析或综合分析）。

### 5. 发布成品

从 wiki 中提炼面向外部的成品输出：

```
把 wiki 中关于 Playwright vs Cypress 的知识整理成一篇博客
```

LLM 会从 wiki 提炼内容、转换为独立可读的标准 Markdown、存入 `output/posts/`，你审核定稿。

支持的输出类型：博客文章、研究报告、Marp 幻灯片、教程、知识简报。

### 6. 巡检

定期让 LLM 检查 wiki 健康状况：

```
巡检一下 wiki
```

LLM 会检查矛盾、孤立页面、缺失概念页、过时信息等。

## Obsidian 配置指南

本项目的 wiki 层完全兼容 [Obsidian](https://obsidian.md/)，推荐用 Obsidian 作为浏览器。LLM 在一侧编辑，你在 Obsidian 中实时浏览。

### 基础配置

1. 用 Obsidian 打开本项目根目录作为 Vault

2. 进入 **Settings → Files and links**，做以下调整：

   | 设置项 | 推荐值 | 说明 |
   |--------|--------|------|
   | Default location for new notes | `raw/articles` | 新笔记默认存入 raw 目录 |
   | New link format | Shortest path when possible | 链接格式简洁 |
   | Use `[[Wikilinks]]` | 开启 | 启用双链语法 |
   | Attachment folder path | `raw/assets/` | 附件统一存放 |
   | Detect all file extensions | 开启 | 识别 PDF 等非 md 文件 |

3. 进入 **Settings → Editor**：

   | 设置项 | 推荐值 | 说明 |
   |--------|--------|------|
   | Show frontmatter | 开启 | 显示 YAML 元数据 |
   | Readable line length | 开启 | 提升阅读体验 |

### 推荐插件

#### Obsidian 社区插件

在 **Settings → Community plugins** 中搜索安装：

| 插件 | 用途 | 配置要点 |
|------|------|---------|
| **Dataview** | 动态查询页面元数据 | 用 `dataview` 代码块查询 frontmatter 中的 tags、sources 等字段，生成动态表格 |
| **Excalidraw** | 手绘风格白板与图表 | 可在 wiki 页面中嵌入架构图、流程图、概念关系图。文件存入 `raw/assets/`，通过 `![[文件名.excalidraw]]` 嵌入 |
| **Local Images Plus** | 自动下载远程图片到本地 | 设置下载路径为 `raw/assets/`。粘贴或导入含远程图片的文章时，自动将图片下载到本地并替换链接，防止外链失效 |

#### 浏览器扩展

| 扩展 | 浏览器 | 用途 | 配置要点 |
|------|--------|------|---------|
| **Obsidian Web Clipper** | Chrome / Firefox / Safari | 一键将网页文章保存为 Markdown | 安装后设置保存路径为 `raw/articles/`，配合 Local Images Plus 自动下载文章中的图片 |

### 图谱视图配置

Obsidian 的图谱视图（Graph View）是浏览知识结构的最佳方式：

1. 打开图谱视图（`Ctrl/Cmd + G`）
2. 推荐过滤设置：
   - **Filters → Search files**：输入 `path:wiki/` 只显示 wiki 页面
   - **Groups**：按目录着色区分实体、概念、摘要等类型
     - `path:wiki/entities` → 蓝色
     - `path:wiki/concepts` → 绿色
     - `path:wiki/summaries` → 黄色
     - `path:wiki/comparisons` → 橙色
     - `path:wiki/synthesis` → 紫色
3. 观察：
   - 连接最多的节点是知识枢纽
   - 孤立节点可能需要补充交叉引用
   - 聚类揭示知识领域的自然分组

### Dataview 查询示例

安装 Dataview 插件后，可以在任意 Markdown 文件中使用以下查询：

**按标签列出所有页面**：

````markdown
```dataview
TABLE tags, description, updated
FROM "wiki"
WHERE contains(tags, "测试")
SORT updated DESC
```
````

**列出最近更新的页面**：

````markdown
```dataview
TABLE category, description, updated
FROM "wiki"
SORT updated DESC
LIMIT 10
```
````

**列出所有素材摘要及其来源**：

````markdown
```dataview
TABLE sources, description, created
FROM "wiki/summaries"
SORT created DESC
```
````

### 下载图片到本地

为防止外部图片链接失效，建议将文章中的图片下载到本地：

- **推荐方式**：安装 **Local Images Plus** 插件（见上方推荐插件），它会在你粘贴或导入文章时自动下载远程图片到 `raw/assets/` 并替换链接，全自动。
- **手动方式**：**Settings → Hotkeys** 搜索 "Download"，为 "Download attachments for current file" 绑定快捷键（如 `Ctrl+Shift+D`）。用 Web Clipper 保存文章后按快捷键即可。

## 许可

> 本项目结构和 Schema 设计基于 [Karpathy 的 LLM Wiki 理念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

MIT License — 详见 [LICENSE](LICENSE)。
