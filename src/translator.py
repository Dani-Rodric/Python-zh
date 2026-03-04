
import os
import re
import json
import logging
from typing import List

from src.qwen_api import QwenAPI

class Translator:
    """一个用于解析和翻译不同类型文件的类。"""

    def __init__(self, qwen_api: QwenAPI):
        self.qwen_api = qwen_api

    def translate_file(self, file_path: str) -> str:
        """根据文件类型翻译文件内容。"""
        _, extension = os.path.splitext(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if extension == ".py":
            return self._translate_python_file(content)
        elif extension == ".md":
            return self._translate_markdown_file(content)
        # 可以为其他文件类型添加更多的 elif 分支
        else:
            logging.warning(f"Unsupported file type: {extension}. Skipping translation.")
            return content

    def _translate_python_file(self, content: str) -> str:
        """翻译 Python 文件中的文档字符串和注释。"""
        # 翻译文档字符串 (docstrings)
        docstring_pattern = re.compile(r'("""[\s\S]*?""")')
        def translate_docstring(match):
            docstring = match.group(1)
            prompt = f"Translate the following Python docstring to Chinese, keeping the original format and technical terms. Provide a bilingual result with Chinese first, followed by the original English.\n\nOriginal docstring:\n{docstring}"
            translated = self.qwen_api.translate(docstring, prompt)
            return f'"""{translated}"""'
        content = docstring_pattern.sub(translate_docstring, content)

        # 翻译行内注释
        comment_pattern = re.compile(r'(#.*)')
        def translate_comment(match):
            comment = match.group(1)
            prompt = f"Translate the following English comment to Chinese. The result should be in the format '# 中文注释', followed by the original comment on the next line.\n\nOriginal comment:\n{comment}"
            translated = self.qwen_api.translate(comment, prompt)
            return f"# {translated}\n{comment}"
        content = comment_pattern.sub(translate_comment, content)
        
        return content

    def _translate_markdown_file(self, content: str) -> str:
        """翻译 Markdown 文件中的文本内容。"""
        # 简单的段落翻译，可以根据需要进行扩展
        paragraphs = content.split('\n\n')
        translated_paragraphs = []
        for p in paragraphs:
            if p.strip().startswith(("```", "#")):
                translated_paragraphs.append(p) # 不翻译代码块和标题
                continue
            
            prompt = f"Translate the following Markdown paragraph to Chinese. Keep the original formatting. Provide a bilingual result with Chinese first, followed by the original English paragraph.\n\nOriginal paragraph:\n{p}"
            translated = self.qwen_api.translate(p, prompt)
            translated_paragraphs.append(f"{translated}\n\n{p}")
            
        return "\n\n".join(translated_paragraphs)
