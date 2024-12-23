"""Constants for the SnapNews application."""

# Tag categories and their respective tags
TAGS = {
    "技术类": ["AI/ML", "LLM", "RAG", "Web3", "云计算", "网络安全"],
    "商业类": ["创业", "投资", "市场动态"],
    "科技类": ["硬件", "软件", "创新"],
    "行业类": ["金融", "医疗", "教育", "零售"],
    "地区类": ["国内", "国际", "地方新闻"]
}

# LLM system prompt
SYSTEM_PROMPT = """你是一个专业的新闻分析师，请对今日新闻进行简明扼要的总结。
关注以下几个方面：
1. 主要新闻事件
2. 重要趋势
3. 值得关注的发展

要求：
- 简明扼要
- 突出重点
- 客观中立
"""

# News API parameters
NEWS_PARAMS = {
    "language": "zh",
    "sort_by": "publishedAt",
    "page_size": 40
}
