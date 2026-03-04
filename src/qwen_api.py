
import re
import logging
from typing import List, Tuple, Dict

import requests

class QwenAPI:
    """一个用于处理文本翻译的 Qwen API 封装器。

    A wrapper for the Qwen API to handle text translation."""

    def __init__(self, api_key: str):
        """初始化 QwenAPI 客户端。

        Initializes the QwenAPI client.

        Args:
            api_key: 您的 Qwen API 密钥。
            api_key: Your Qwen API key.
        """
        self.api_key = api_key
        self.endpoint = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        # 更全面的保护模式，包括 YAML front matter, HTML/XML 标签等
        self.protected_patterns = re.compile(
            r"(---[\s\S]+?---|```[\s\S]*?```|`[^`]*?`|!?\[.*?\]\(.*?\)|<[^>]+?>|\w+=\"[^\"]*\"|\w+=\'[^\']*\')"
        )

    def _extract_and_protect_blocks(self, text: str) -> Tuple[str, Dict[str, str]]:
        """从文本中提取受保护的块，并用占位符替换它们。

        Extracts protected blocks from the text and replaces them with placeholders.

        Args:
            text: 原始文本。
            text: The original text.

        Returns:
            一个元组，包含带有占位符的文本和占位符到原始块的映射。
            A tuple containing the text with placeholders and a mapping from placeholders to original blocks.
        """
        placeholder_map = {}
        def replacer(match):
            block = match.group(0)
            placeholder = f"__BLOCK_{len(placeholder_map)}__"
            placeholder_map[placeholder] = block
            return placeholder
        
        processed_text = self.protected_patterns.sub(replacer, text)
        return processed_text, placeholder_map

    def _reinsert_blocks(self, text: str, placeholder_map: Dict[str, str]) -> str:
        """将受保护的块重新插入到翻译后的文本中。

        Reinserts the protected blocks back into the translated text.

        Args:
            text: 带有占位符的翻译后文本。
            text: The translated text with placeholders.
            placeholder_map: 占位符到原始块的映射。
            placeholder_map: A mapping from placeholders to original blocks.

        Returns:
            重新插入原始块后的最终文本。
            The final text with the original blocks reinserted.
        """
        for placeholder, original_block in placeholder_map.items():
            text = text.replace(placeholder, original_block, 1)
        return text

    def translate(self, text_to_translate: str, prompt: str, max_retries: int = 3) -> str:
        """使用给定的提示翻译文本。

        Translates text using the given prompt.

        Args:
            text_to_translate: 要翻译的文本。
            text_to_translate: The text to translate.
            prompt: 用于翻译的提示。
            prompt: The prompt to use for translation.
            max_retries: 失败时重试的次数。
            max_retries: The number of times to retry on failure.

        Returns:
            翻译后的文本。
            The translated text.
        """
        processed_text, placeholder_map = self._extract_and_protect_blocks(text_to_translate)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "qwen-plus",
            "input": {
                "prompt": prompt.format(text=processed_text)
            },
            "parameters": {}
        }

        for attempt in range(max_retries):
            try:
                response = requests.post(self.endpoint, headers=headers, json=payload)
                response.raise_for_status()  # 对错误的狀態碼抛出异常
                
                translated_text = response.json()["output"]["text"]
                final_text = self._reinsert_blocks(translated_text, placeholder_map)
                
                return final_text

            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                if attempt + 1 == max_retries:
                    logging.error("Translation failed after multiple retries.")
                    raise
        return ""  # 不应到达
