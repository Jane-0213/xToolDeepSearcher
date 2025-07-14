# xToolDeepSearcher 

一个智能问答系统，聚焦 xTool 产品，支持多轮语义检索、精确功能解析和结构化 JSON 输出。

> 本项目基于 Milvus 向量数据库 + DeepSearcher 框架 + DeepSeek LLM 打造，可通过本地运行实现对 xTool 官网数据的智能查询。

---

## 项目亮点

- ✅ **自动爬取官网信息**：支持通过 Firecrawl 自动抓取 xTool 官网内容，构建私有知识库。
- ✅ **语义理解 + LLM 推理**：使用 DeepSeek Chat 模型进行自然语言问答。
- ✅ **本地向量搜索**：使用 Milvus 高效管理和检索文本片段。
- ✅ **支持 JSON 格式输出**：适用于对结构化结果有强需求的系统对接场景。
- ✅ **自动清洗和容错机制**：具备 JSON 格式容错恢复能力。

---
## 展示
<img width="1839" height="1885" alt="83aa5cd9613ec09af4188f5c659bee8b" src="https://github.com/user-attachments/assets/998ed2d4-13b0-4c6d-a87c-4955b13f41f7" />
<img width="1311" height="1180" alt="327380292ffbc371c2a45b0e32d89e31" src="https://github.com/user-attachments/assets/22e71f48-1d95-4a10-bb9d-ba4943a97091" />
<img width="949" height="1681" alt="0c23c98a376bed8e21d483b62f514a0e" src="https://github.com/user-attachments/assets/57597411-4951-4e20-b129-ee17b965de14" />

## 安装与运行

### 1. 安装依赖
创建并激活虚拟环境（建议使用Python 3.10版本）。
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. 安装DeepSearcher
```bash
pip install deepsearcher
```

### 3. 本地部署 Milvus（需安装 Docker）
确保docker running，启动
```bash
docker-compose up -d
```

### 4. 设置环境变量与配置代码
运行——编辑配置——环境变量——添加键值对

#### LLM配置
确保您已经准备好了DEEPSEEK API KEY作为环境变量DEEPSEEK API KEY。
```python
config.set_provider_config("llm", "DeepSeek", {"model": "deepseek-chat"})
```

#### 爬虫配置
如需爬取官网数据，请配置，以fire crawl为例：
```python
config.set_provider_config("web_crawler", "FireCrawlCrawler", {})
```
### 5.启动问答 Agent
输入问题如：
1. xTool P2S 的独特功能是什么？
2. F 系列和 P 系列产品之间有什么主要区别？
3. xTool F1 Ultra 可以加工哪些材料？




