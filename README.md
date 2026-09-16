# xToolDeepSearcher 

一个面向 xTool内容站 [Atomm.com](https://www.atomm.com/) 的智能语义问答系统，聚焦创作者社区内容、用户评论与平台功能提取，支持多轮语义检索、评论解析和结构化 JSON 输出。

> 项目基于 Milvus 向量数据库 + DeepSearcher 框架 + DeepSeek LLM，可本地运行，对 Atomm 平台内容及评论进行深入理解与问答支持。

---

## 项目亮点

- ✅ **支持多页面评论爬取**：基于 Firecrawl，可自动抓取 Atomm Blog 页面下的正文和评论内容。
- ✅ **多轮语义理解 + 评论提炼**：支持对用户评论中的功能建议、使用反馈进行语义抽取。
- ✅ **LLM 智能问答引擎**：结合 DeepSeek-Chat 模型进行多轮推理，精准回答产品、用户需求等问题。
- ✅ **本地私有向量检索**：通过 Milvus 管理向量化内容，实现高效文本检索与多轮上下文理解。
- ✅ **结构化 JSON 输出**：适合用作系统对接、二次分析等结构化任务场景。
- ✅ **异常容错机制**：支持 JSON 响应异常清洗与恢复，增强鲁棒性。

---
## 展示
<img width="1849" height="1549" alt="d1d2a06c582e13be1a062193ab037b00" src="https://github.com/user-attachments/assets/d21b015d-d1ae-40a6-adda-b2cb00e36fb3" />
<img width="936" height="1824" alt="0a4ab3b0afee25a9d54dc5835d1c376f" src="https://github.com/user-attachments/assets/891ed01f-a80c-4f6e-a5a1-28fa33a19072" />
<img width="1840" height="1652" alt="99af0cca3a16fb5e1cdf0dc6674071fe" src="https://github.com/user-attachments/assets/6a17d90f-4ae9-499e-b5b9-db4811d664dd" />

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

#### 爬虫配置（支持评论抓取）
如需爬取官网数据，请配置，以fire crawl为例：
```python
config.set_provider_config("web_crawler", "FireCrawlCrawler", {
    "enable_javascript": True
})
```
### 5.启动问答 Agent
运行主程序后，输入你的自然语言问题，例如：

- “用户期待atomm未来有什么功能？”

- “AMA 活动中用户都问了什么？”

- “有没有用户反馈目前平台使用过程中有哪些不方便的地方”

- “有没有用户反馈目前平台使用过程中有哪些不方便的地方？
- 用户对 AtomM 目前的体验满意吗？有没有正向或负面评价？”


