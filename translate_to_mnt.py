# save as translate_to_mnt.py
# 作用：
# 1) 先嘗試從本地檔案 ./翻譯文件.txt 讀內容
# 2) 若找不到，改用 GitHub API 讀 (public repo 可不帶 token)
# 3) 做一個簡單的「白話化」處理（規則式替換，避免卡在模型不可用）
# 4) 輸出到 /mnt/data/翻譯文件_白話版.txt

import os
import sys
import json
import base64
from urllib.parse import quote
from urllib.request import Request, urlopen, URLError

OWNER  = os.getenv("GITHUB_USER", "taiwantiger321")
REPO   = os.getenv("REPO_NAME", "translate")
BRANCH = os.getenv("BRANCH", "main")
SRC_FN = "翻譯文件.txt"
OUT_FN = "/mnt/data/翻譯文件_白話版.txt"

def read_local(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def read_github(owner: str, repo: str, branch: str, path: str) -> str:
    # 走 GitHub Contents API；public repo 可不帶 token
    token = os.getenv("GITHUBTOKEN") or os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{quote(path)}?ref={quote(branch)}"
    headers = {
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "codex-downloader"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    req = Request(url, headers=headers)
    try:
        with urlopen(req) as resp:
            data = resp.read()
            # 因為 Accept: raw，這裡直接是檔案內容
            return data.decode("utf-8", errors="replace")
    except URLError as e:
        raise RuntimeError(f"讀取 GitHub 檔案失敗：{e}")

def to_plain_zh(text: str) -> str:
    # 輕量白話化（規則式）：模型不可用時的保底方案
    # 你之後可換成真正的翻譯/潤飾模型輸出
    replacements = {
        "之": "的", "及": "和", "與": "和", "於": "在", "亦": "也", "並": "而且",
        "即可": "就可以", "即可 ": "就可以 ", "需": "需要", "能夠": "能", "無法": "不能",
        "僅": "只", "將": "會", "進行": "做", "透過": "用", "提供": "給", "使用者": "你",
        "因此": "所以", "此外": "另外", "若": "如果", "即可": "就可以"
    }
    out = text
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out

def main():
    # 1) 優先讀本地 ./翻譯文件.txt
    original = read_local(SRC_FN)

    # 2) 若本地沒有，改用 GitHub API 讀
    if original is None:
        original = read_github(OWNER, REPO, BRANCH, SRC_FN)

    if not original or original.strip() == "":
        raise RuntimeError(f"讀不到內容：{SRC_FN}")

    # 3) 白話化處理（可替換成真正模型）
    translated = to_plain_zh(original)

    # 4) 輸出到 /mnt/data/
    os.makedirs(os.path.dirname(OUT_FN), exist_ok=True)
    with open(OUT_FN, "w", encoding="utf-8") as f:
        f.write(translated)

    print(f"✅ 已輸出：{OUT_FN}")

if __name__ == "__main__":
    main()
