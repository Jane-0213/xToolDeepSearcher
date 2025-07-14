# run_xtool_agent.py

# 导入操作系统模块，用于检查环境变量
import os
import json
import re

# 导入 deepsearcher 库的配置类，用于设置LLM、Embedding、VectorDB等
from deepsearcher.configuration import Configuration, init_config
# 导入 deepsearcher 库的在线查询函数，用于向Agent提问
from deepsearcher.online_query import query
# 导入 deepsearcher 库的离线数据加载函数 (本地文件和网页爬取)
from deepsearcher.offline_loading import load_from_local_files, load_from_website


# --- JSON 响应清洗函数 ---
def clean_json_response(raw_response: str) -> dict:
    """
    清洗JSON响应，提取有效JSON对象
    三层清洗策略：
    1. 尝试直接解析为JSON
    2. 提取可能的JSON部分
    3. 手动构建基本结构
    """
    # 尝试直接解析
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        pass

    # 尝试提取JSON部分
    json_match = re.search(r'\{[\s\S]*\}', raw_response)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass

    # 终极方案：提取键值对
    result = {}
    key_value_pairs = re.findall(r'\"([^\"]+)\"\s*:\s*\"([^\"]*)\"', raw_response)
    for key, value in key_value_pairs:
        result[key] = value

    # 如果没有任何键值对，返回原始响应前100字符
    return result if result else {"错误": "格式解析失败", "原始响应": raw_response[:100] + "..."}


# --- 1. Agent 配置 ---
# 创建 Configuration 类的实例，用于管理DeepSearcher的所有设置
config = Configuration()

# 配置大语言模型 (LLM)，用的chat速度更快
config.set_provider_config("llm", "DeepSeek", {"model": "deepseek-chat"})

# 配置 Embedding 模型 (将文本转换为向量的模型)
config.set_provider_config("embedding", "FastEmbedEmbedding", {"model": "intfloat/multilingual-e5-large"})

# 配置向量数据库 (存储文本向量的数据库)
config.set_provider_config("vector_db", "Milvus", {
    "uri": "http://localhost:19530",  # Docker 容器地址
    "token": ""
})

# 配置网页爬虫
config.set_provider_config("web_crawler", "FireCrawlCrawler", {
    "enable_javascript": True
})
# 初始化 DeepSearcher 的配置
init_config(config=config)

# --- 2. 数据加载 (构建 xTool 知识库) ---

# 选项 A: 从 xTool 官网加载数据
print("--- 正在加载 AtomM 博客数据 ---")
# xtool_website_urls = [
#     # 商品，可以用P和F系列的商品进行测试
#     # P系列
#     "https://www.xtool.com/products/xtool-p2-55w-co2-laser-cutter",
#     "https://www.xtool.com/products/ultimate-productive-business-duo",
#     "https://www.xtool.com/products/refurbished-xtool-p2-55w-desktop-co2-laser-cutter",
#     # F系列
#     "https://www.xtool.com/products/xtool-f2-ultra-60w-mopa-40w-diode-dual-laser-engraver",
#     "https://www.xtool.com/products/xtool-f1",
#     "https://www.xtool.com/products/xtool-f1-ultra-20w-fiber-diode-dual-laser-engraver",
#     "https://www.xtool.com/products/ultimate-productive-business-duo"
# ]
atomm_blog_urls = [
    "https://www.atomm.com/blog/1966--atomm-ama-is-here-ask-us-anything-and-win-rewards",
    "https://www.atomm.com/blog/1969-ama-recap-your-questions-answered",
    "https://www.atomm.com/blog/1963-it-starts-with-an-atomm-the-story-behind-the-transformation"
]

if os.getenv("FIRECRAWL_API_KEY"):
    print(f"检测到 FIRECRAWL_API_KEY。正在使用 FireCrawl 爬取以下网站：{atomm_blog_urls}")
    load_from_website(urls=atomm_blog_urls)
    print("Atomm 官网数据加载完成。")
else:
    print("警告：未检测到 FIRECRAWL_API_KEY。跳过网站爬取。")
    print("如果您想从官网获取最新信息，请设置 FIRECRAWL_API_KEY。")

# embedding 分块时间太长，省略
# # 选项 B: 从本地文件加载数据 (加载你的 xTool 品牌手册 PDF 或其他本地文档)
# print("\n--- 正在加载本地文件数据 ---")
# # 确保 'xTool品牌手册.pdf' 文件放在你的 PyCharm 项目的根目录下
# # 或者指定包含该文件的目录路径，例如：
# # xtool_local_docs_path = "C:/Users/YourUser/Documents/xTool_Docs/"
# # load_from_local_files(paths_or_directory=xtool_local_docs_path)
#
# # 假设你的 PDF 在当前项目根目录
# xtool_local_data_path = "./"
# print(f"正在从本地路径 '{xtool_local_data_path}' 加载文件。请确保 'xTool品牌手册.pdf' 在此目录下。")
# # 调用 load_from_local_files 函数加载指定路径下的所有文件（包括PDF）。
# # deepsearcher 会自动使用其内置的 FileLoader（如 PDFLoader）来处理不同类型的文件。
# load_from_local_files(paths_or_directory=xtool_local_data_path)
# print("本地文件数据加载完成。")


print("\n所有数据加载已完成。知识库已构建完毕。")
print("现在可以向 xTool Agent 提问了！")

# --- 3. Agent 查询与交互 ---
while True:
    user_question = input("\n请提出你对 xTool 内容站atomm相关的问题 (输入 '退出' 结束): ")
    # 示例问题：1.xTool P2S 有什么独特的功能？；2.xTool F1 Ultra 可以加工哪些材料？；3.F 系列和 P 系列产品之间有什么主要区别？

    if user_question.lower() == '退出':
        print("程序结束。感谢使用！")
        break

    print("正在查询中...")

    try:
        # 添加重试机制
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # 构建带JSON格式要求的提示
                json_prompt = f"""
                你是一个只能输出 JSON 的助手，并且是中文。如果输出任何非 JSON 内容将会导致程序崩溃。

                请严格按照以下格式回答用户问题，内容数量不限制（不要加```json、不要加解释、不要换行说明）：

                {{
                  "评价1": "内容",
                  "评价2": "内容"
                }}
                请分析 AtomM 博客评论中的功能建议与用户期待，提取清晰表达的观点。

                问题：{user_question}

                """

                # 执行查询
                raw_result = query(json_prompt)
                if isinstance(raw_result, tuple):
                    raw_result = raw_result[0]

                # 清洗和解析JSON响应
                cleaned_json = clean_json_response(raw_result)

                # 打印结构化结果
                print("\n=== AI Agent 的回答 ===")
                for key, value in cleaned_json.items():
                    print(f"- {key}: {value}")

                # 成功则跳出重试循环
                break

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"查询出错，重试中 ({attempt + 1}/{max_retries}): {str(e)[:100]}...")
                else:
                    # 最后一次重试仍然失败
                    print(f"\n查询最终失败: {e}")
                    print("原始响应内容:")
                    print(raw_result[:500] + "...")  # 打印部分原始响应以便调试

    except Exception as e:
        print(f"严重错误: {e}")
        print("请检查您的网络连接或系统配置。")