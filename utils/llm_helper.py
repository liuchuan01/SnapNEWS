"""LLM helper utility for SnapNews."""
import os
import logging
from typing import List, Dict, AsyncGenerator
from openai import AsyncOpenAI
from dotenv import load_dotenv
from constants import SYSTEM_PROMPT

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMHelper:
    """Class to handle interactions with OpenAI API."""
    
    def __init__(self):
        """Initialize the LLMHelper with API key."""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = "https://yunwu.ai/v1"  # 修改为v1路径
        
        logger.debug(f"Initializing LLMHelper with base_url: {base_url}")
        logger.debug(f"API Key (first 8 chars): {api_key[:8]}...")
        
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            default_headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
    
    async def generate_summary(self, news_list: List[Dict]) -> AsyncGenerator[str, None]:
        """Generate a summary of news articles using Claude.
        
        Args:
            news_list: List of news articles to summarize
            
        Yields:
            Chunks of generated summary
        """
        prompt = self._build_summary_prompt(news_list)
        logger.debug(f"Generated prompt length: {len(prompt)}")
        
        try:
            logger.debug("Attempting to create chat completion...")
            response = await self.client.chat.completions.create(
                model="claude-3-5-sonnet-20240620",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
                temperature=0.7,
                max_tokens=2000
            )
            logger.debug("Successfully created chat completion")
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    logger.debug(f"Received chunk: {chunk.choices[0].delta.content[:50]}...")
                    yield chunk.choices[0].delta.content
                
        except Exception as e:
            error_msg = f"Error generating summary: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield error_msg
    
    def _build_summary_prompt(self, news_list: List[Dict]) -> str:
        """Build prompt for news summarization.
        
        Args:
            news_list: List of news articles
            
        Returns:
            Formatted prompt string
        """
        news_text = "\n\n".join([
            f"标题: {article['title']}\n"
            f"描述: {article['description']}\n"
            f"来源: {article['source']}"
            for article in news_list
        ])
        
        return f"""请对以下{len(news_list)}条新闻进行总结：

{news_text}"""
