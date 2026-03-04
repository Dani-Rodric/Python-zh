
import os
import base64
import requests
import logging

# --- 配置 ---
GITHUB_TOKEN = os.getenv("GITHUB_API_KEY", "YOUR_GITHUB_API_KEY_FALLBACK")
REPO_OWNER = "Dani-Rodric"
REPO_NAME = "Python-zh"
BRANCH = "main"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_file_to_github(file_path, repo_path):
    """通过 GitHub API 上传单个文件。"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{repo_path}"
    
    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")
        
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 检查文件是否已存在以获取其 SHA (用于更新)
    res = requests.get(url, headers=headers)
    sha = res.json().get("sha") if res.status_code == 200 else None
    
    data = {
        "message": f"Deploy: {repo_path}",
        "content": content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
        
    res = requests.put(url, headers=headers, json=data)
    if res.status_code in [200, 201]:
        logging.info(f"Successfully uploaded: {repo_path}")
    else:
        logging.error(f"Failed to upload {repo_path}: {res.json()}")

def deploy_project():
    """遍历项目文件并逐个上传。"""
    # 需要上传的白名单文件和目录
    upload_list = [
        ".github/workflows/sync.yml",
        "src/qwen_api.py",
        "src/translator.py",
        "src/utils.py",
        "sync.py",
        "requirements.txt",
        "README.md",
        "TRANSLATION.md",
        "CHANGELOG.md",
        "FILE_TREE.md"
    ]
    
    for item in upload_list:
        if os.path.isfile(item):
            upload_file_to_github(item, item)
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                for file in files:
                    file_path = os.path.join(root, file)
                    repo_path = file_path.replace("\\", "/") # 确保路径格式正确
                    upload_file_to_github(file_path, repo_path)

if __name__ == "__main__":
    deploy_project()
