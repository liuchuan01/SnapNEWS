"""Main application file for SnapNews."""
import streamlit as st
import asyncio
import logging
from utils.news_fetcher import NewsFetcher
from utils.llm_helper import LLMHelper
from constants import TAGS

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="SnapNews - 智能新闻聚合平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    logger.debug("Initializing components...")
    return NewsFetcher(), LLMHelper()

news_fetcher, llm_helper = init_components()

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
        margin: 0;
    }
    .main > div {
        padding-left: 0;
        padding-right: 0;
    }
    section[data-testid="stSidebar"] {
        width: 300px;
        background-color: #f8f9fa;
    }
    .news-card {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        background-color: white;
    }
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .tag {
        background: #f0f0f0;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        margin-right: 0.5rem;
        font-size: 0.8rem;
    }
    div.block-container {
        padding-left: 0;
        padding-right: 0;
        max-width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("SnapNews - 智能新闻聚合平台")

# Sidebar
with st.sidebar:
    st.header("兴趣标签")
    selected_tags = []
    
    for category, tags in TAGS.items():
        with st.expander(category, expanded=True):
            for tag in tags:
                if st.checkbox(tag, key=f"tag_{tag}"):
                    selected_tags.append(tag)
    
    st.write(f"已选择 {len(selected_tags)} 个标签")
    
    if st.button("获取最新新闻", disabled=len(selected_tags) == 0):
        logger.debug(f"Fetching news for tags: {selected_tags}")
        if "news_list" not in st.session_state:
            st.session_state.news_list = []
        st.session_state.news_list = news_fetcher.fetch_news(selected_tags)
        st.session_state.refresh_summary = True
        logger.debug(f"Fetched {len(st.session_state.news_list)} news articles")

# Main content
col1, col2 = st.columns([2, 1])

# News cards
with col1:
    st.subheader("最新新闻")
    if "news_list" in st.session_state and st.session_state.news_list:
        for news in st.session_state.news_list[:8]:
            with st.container():
                st.markdown(f"""
                    <div class="news-card">
                        <h3>{news['title']}</h3>
                        <p>{news['description']}</p>
                        <div>
                            <span class="tag">{news['source']}</span>
                            <span class="tag">{news['published_at'][:10]}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# AI Summary
with col2:
    st.subheader("AI摘要")
    if "news_list" in st.session_state and st.session_state.news_list and st.session_state.get("refresh_summary", False):
        summary_placeholder = st.empty()
        
        async def update_summary():
            logger.debug("Starting summary generation...")
            summary_text = ""
            try:
                async for chunk in llm_helper.generate_summary(st.session_state.news_list[:8]):
                    summary_text += chunk
                    summary_placeholder.markdown(summary_text)
                    logger.debug(f"Updated summary with new chunk, total length: {len(summary_text)}")
            except Exception as e:
                logger.error(f"Error in update_summary: {str(e)}", exc_info=True)
                summary_placeholder.error(f"生成摘要时出错: {str(e)}")
            st.session_state.refresh_summary = False
        
        asyncio.run(update_summary())
