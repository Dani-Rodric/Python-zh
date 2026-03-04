
# Python 中文镜像项目 (Python-zh)

这是一个自动化的翻译项目，旨在为 `Dani-Rodric/Python` 仓库创建一个完整的、持续同步的中文镜像。

## ✨ 功能

- **全量翻译**: 自动翻译上游仓库的所有文档、注释、说明等。
- **持续同步**: 每日自动检测上游仓库的更新，并进行增量翻译。
- **高质量翻译**: 基于 Qwen API，并遵循详细的翻译准则，保留技术术语，保证代码可读性。
- **保留提交历史**: 尽可能保留原始的 Git 提交历史和作者信息。

## 🚀 部署指南

要启动这个自动化翻译系统，请按照以下步骤进行一次性设置：

### 1. 创建新的 GitHub 仓库

在您的 GitHub 账户 (`Dani-Rodric`) 下，创建一个新的 **空** 仓库，并将其命名为 `Python-zh`。

**重要提示**: 请不要勾选 "Initialize this repository with a README" 或任何其他文件。我们需要一个完全空的仓库来开始。

### 2. 配置 API 密钥

进入您刚刚创建的 `Dani-Rodric/Python-zh` 仓库，然后导航到 `Settings > Secrets and variables > Actions`。

点击 `New repository secret`，并添加以下两个密钥：

- **`QWEN_API_KEY`**: 
  - **Value**: `sk-55394abb583f4f7bad8d4bee0795645f`

- **`GITHUB_API_KEY`**: 
  - **Value**: `YOUR_GITHUB_API_KEY` (请在此处填入您的 GitHub 令牌)

这些密钥将被 GitHub Actions 用来调用 Qwen API 和提交代码。

### 3. 推送项目文件

将本项目中的所有文件（`sync.py`, `src/`, `.github/`, `requirements.txt`, `README.md`, `TRANSLATION.md`）推送到您的 `Dani-Rodric/Python-zh` 仓库的主分支 (`main`)。

```bash
# 在您的本地项目目录中
git init
git add .
git commit -m "Initial commit of the translation system"
git branch -M main
git remote add origin https://github.com/Dani-Rodric/Python-zh.git
git push -u origin main
```

### 4. 手动触发首次运行

推送完成后，进入 `Dani-Rodric/Python-zh` 仓库的 `Actions` 页面。您会看到一个名为 "Sync with Upstream and Translate" 的工作流。

点击它，然后选择 `Run workflow` -> `Run workflow`。这将手动触发第一次的全量克隆和翻译。这个过程可能会持续较长时间，因为它需要处理整个上游仓库。

### 5. 完成！

首次运行成功后，GitHub Actions 将会按照计划，每日自动检查并同步上游仓库的更新。

## 📄 翻译规则

详细的翻译规则、API 使用情况统计和最后同步时间，请参见 [TRANSLATION.md](TRANSLATION.md)。
