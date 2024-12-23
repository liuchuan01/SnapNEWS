# SnapNews

SnapNews是一个智能新闻聚合平台，为用户提供个性化的新闻资讯服务。使用NewsAPI获取最新新闻，并通过OpenAI的GPT-4模型提供智能化的新闻摘要。

## 功能特点

- 多标签选择：支持技术、商业、科技等多个领域的标签组合
- 实时新闻：获取最新40条相关新闻
- 智能摘要：使用GPT-4对新闻进行分析总结
- 流式显示：实时展示AI生成的摘要内容
- 响应式设计：适配不同设备的显示需求

## 安装说明

1. 克隆项目并安装依赖：
```bash
git clone [repository_url]
cd SnapNews
pip install -r requirements.txt
```

2. 配置环境变量：
创建`.env`文件并添加以下内容：
```
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
```

3. 运行应用：
```bash
streamlit run app.py
```

## 使用说明

1. 在侧边栏选择感兴趣的标签
2. 点击"获取最新新闻"按钮
3. 查看新闻卡片和AI生成的摘要
4. 可以随时更改标签选择，重新获取新闻

## 技术栈

- Frontend: Streamlit
- News API: NewsAPI
- AI Model: OpenAI GPT-4
- Language: Python 3.8+

## 项目结构

```
SnapNews/
├── app.py              # 主应用入口
├── constants.py        # 常量定义
├── utils/
│   ├── news_fetcher.py # NewsAPI调用
│   └── llm_helper.py   # OpenAI接口封装
├── requirements.txt    # 依赖管理
└── README.md          # 项目文档
```

## 注意事项

- 需要有效的OpenAI API密钥和NewsAPI密钥
- 建议使用Python 3.8或更高版本
- 确保良好的网络连接以获取新闻和进行AI处理
# SnapNEWS
# SnapNEWS
