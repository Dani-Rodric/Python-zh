
import os
import logging
import subprocess
from datetime import datetime

from src.qwen_api import QwenAPI
from src.translator import Translator

# --- 配置 ---
UPSTREAM_REPO_URL = "https://github.com/Dani-Rodric/Python.git"
TARGET_REPO_PATH = "Python-zh"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_changed_files(repo_path: str, last_sync_commit: str) -> list:
    """获取自上次同步以来发生变化的文件列表。"""
    cmd = f"git -C {repo_path} diff --name-only {last_sync_commit} HEAD"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error getting changed files: {result.stderr}")
        return []
    return result.stdout.strip().split('\n')

def main():
    qwen_api_key = os.getenv("QWEN_API_KEY")
    if not qwen_api_key:
        logging.error("QWEN_API_KEY environment variable not set.")
        return

    qwen_api = QwenAPI(api_key=qwen_api_key)
    translator = Translator(qwen_api)

    # 1. 克隆或更新仓库
    if not os.path.exists(TARGET_REPO_PATH):
        logging.info(f"Cloning upstream repository to {TARGET_REPO_PATH}...")
        subprocess.run(f"git clone {UPSTREAM_REPO_URL} {TARGET_REPO_PATH}", shell=True, check=True)
        last_sync_commit = "HEAD~1" # 假设我们翻译除最新提交外的所有内容
    else:
        logging.info(f"Pulling latest changes from upstream in {TARGET_REPO_PATH}...")
        last_sync_commit = subprocess.run(f"git -C {TARGET_REPO_PATH} rev-parse HEAD", shell=True, capture_output=True, text=True).stdout.strip()
        subprocess.run(f"git -C {TARGET_REPO_PATH} pull", shell=True, check=True)

    # 2. 获取变更的文件并翻译
    changed_files = get_changed_files(TARGET_REPO_PATH, last_sync_commit)
    if not changed_files or (len(changed_files) == 1 and not changed_files[0]):
        logging.info("No new changes to translate.")
        return

    logging.info(f"Found {len(changed_files)} changed files to translate.")

    for file_path in changed_files:
        full_path = os.path.join(TARGET_REPO_PATH, file_path)
        if not os.path.exists(full_path):
            continue
        
        logging.info(f"Translating {file_path}...")
        try:
            translated_content = translator.translate_file(full_path)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
        except Exception as e:
            logging.error(f"Error translating {file_path}: {e}")

    # 3. 提交和推送变更
    logging.info("Committing and pushing translated files...")
    commit_message = f"[zh-CN] Automated translation sync - {datetime.utcnow().isoformat()}"
    subprocess.run(f"git -C {TARGET_REPO_PATH} add .", shell=True, check=True)
    subprocess.run(f'git -C {TARGET_REPO_PATH} commit -m "{commit_message}"', shell=True, check=True)
    subprocess.run(f"git -C {TARGET_REPO_PATH} push", shell=True, check=True)

    logging.info("Synchronization complete.")

if __name__ == "__main__":
    main()
