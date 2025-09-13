import os
import subprocess
from github import Github

# === 1. GitHub repo 設定 ===
GITHUB_USER = "taiwantiger321"
REPO_NAME = "translate"
BRANCH = "main"

# ⚠️ Codex Cloud 環境裡要先在 Secrets 設定 GITHUB_TOKEN
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("⚠️ 找不到 GITHUB_TOKEN，請在 Codex Environment → Secrets 設定")

# 建立 GitHub API 客戶端
g = Github(GITHUB_TOKEN)
repo = g.get_user(GITHUB_USER).get_repo(REPO_NAME)

# === 2. 要翻譯的檔案 ===
SOURCE_FILE = "翻譯文件.txt"
OUTPUT_FILE = "翻譯結果.txt"

print(f"🔎 正在讀取 {SOURCE_FILE} ...")
source_content = repo.get_contents(SOURCE_FILE, ref=BRANCH).decoded_content.decode("utf-8")

# === 3. 這裡模擬 Codex 翻譯（你可以改成真正呼叫 OpenAI API）===
translated_text = f"""【白話翻譯】

原始內容：
{source_content}

翻譯結果：
這裡是 Codex Cloud 幫你翻譯的內容...
"""

# === 4. 提交翻譯結果 ===
commit_msg = "Add Codex translation result"

try:
    # 如果檔案已存在 → 更新
    contents = repo.get_contents(OUTPUT_FILE, ref=BRANCH)
    repo.update_file(contents.path, commit_msg, translated_text, contents.sha, branch=BRANCH)
    print(f"✅ 已更新 {OUTPUT_FILE}")
except:
    # 檔案不存在 → 建立
    repo.create_file(OUTPUT_FILE, commit_msg, translated_text, branch=BRANCH)
    print(f"✅ 已新增 {OUTPUT_FILE}")
