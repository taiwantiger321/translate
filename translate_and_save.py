import os
from openai import OpenAI

# 初始化 OpenAI client
client = OpenAI()

# 1. 讀取翻譯文件.txt
with open("翻譯文件.txt", "r", encoding="utf-8") as f:
    original_text = f.read()

# 2. 呼叫 Codex/ChatGPT 模型，把文字翻成白話文
resp = client.chat.completions.create(
    model="gpt-4o-mini",  # 你在 Codex 環境能用的模型
    messages=[
        {"role": "system", "content": "你是一個中文翻譯助手，請把輸入文字轉成淺顯易懂的白話文。"},
        {"role": "user", "content": original_text}
    ]
)

translated_text = resp.choices[0].message.content

# 3. 存到 /mnt/data/，以便下載
output_path = "/mnt/data/翻譯文件_白話版.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(translated_text)

print(f"✅ 已輸出：{output_path}")
