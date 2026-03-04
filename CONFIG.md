
# 配置指南

# Configuration Guide

This document explains how to set up the `config.ini` file required to run the translation script.

## 1. Create the `config.ini` File

Create a file named `config.ini` in the root directory of the project. This file will store your API keys and GitHub repository information.

## 2. Add Configuration Sections

Copy and paste the following template into your `config.ini` file:

```ini
[API_KEYS]
QWEN_API_KEY = YOUR_QWEN_API_KEY
GITHUB_API_KEY = YOUR_GITHUB_API_KEY

[GITHUB]
REPO_OWNER = YOUR_GITHUB_USERNAME
REPO_NAME = YOUR_REPOSITORY_NAME
```

## 3. 替换占位符值

## 3. Replace Placeholder Values

- `YOUR_QWEN_API_KEY`: Replace this with your actual API key for the Qwen (DashScope) service.
- `YOUR_GITHUB_API_KEY`: Replace this with your GitHub Personal Access Token. Ensure the token has `repo` scope to allow creating branches and pull requests.
- `YOUR_GITHUB_USERNAME`: 将此替换为拥有仓库的用户名或组织名。
- `YOUR_GITHUB_USERNAME`: Replace this with the username or organization name that owns the repository.
- `YOUR_REPOSITORY_NAME`: Replace this with the name of your GitHub repository.

## 安全说明

## Security Note

**Do not** commit the `config.ini` file to your version control system (e.g., Git). Add `config.ini` to your `.gitignore` file to prevent accidentally exposing your secret keys.

`.gitignore` 条目示例：

Example `.gitignore` entry:

```
# Configuration files
config.ini
```
