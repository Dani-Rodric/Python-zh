
# 翻译规则与状态说明 (Translation Rules & Status)

本文档详细说明了本中文镜像项目的翻译准则、API 使用情况以及当前的同步状态。

## 1. 翻译准则 (Translation Guidelines)

为了保证翻译质量和代码可读性，所有自动化翻译均遵循以下准则：

- **技术术语保持原文**: 所有已知的技术术语（如 `Python`, `pip`, `asyncio`, `Git`, `API`, `JSON`, `YAML` 等）将保持原文，不进行翻译。

- **代码元素保持原文**: 代码示例中的所有元素，包括变量名、函数名、路径、输出信息和提示符，都将保持原文。

- **行内注释格式**: 对于单行注释 (`#`)，翻译将以 `# 中文注释` 的格式添加在原注释的上方。
  ```python
  # 这是一个中文注释
  # This is an English comment
  x = 1
  ```

- **文档字符串 (Docstrings) 格式**: 对于函数和类的文档字符串，将采用 Google Python Style Guide 的格式，生成中英双语对照的文档字符串。

- **Markdown 文档格式**: 对于 `.md` 等文档文件，翻译后的中文段落将添加在对应的英文段落上方。

## 2. API 使用情况统计 (API Usage Statistics)

*(此部分将由 GitHub Actions 在每次同步后自动更新)*

- **最后同步时间 (Last Sync Time)**: `N/A`
- **本次翻译字数 (Characters Translated in Last Sync)**: `N/A`
- **累计翻译字数 (Total Characters Translated)**: `N/A`
- **API 调用次数 (API Calls in Last Sync)**: `N/A`

## 3. 同步状态 (Sync Status)

*(您可以在项目主页看到由 GitHub Actions 提供的实时状态徽章)*

[![Sync and Translate](https://github.com/Dani-Rodric/Python-zh/actions/workflows/sync.yml/badge.svg)](https://github.com/Dani-Rodric/Python-zh/actions/workflows/sync.yml)
